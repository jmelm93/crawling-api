import aiohttp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'


async def fetch_with_aiohttp(url, user_agent=USER_AGENT):
    """Fetch URL directly with aiohttp (no proxy, free)."""
    headers = {"User-Agent": user_agent}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            return {'url': url, 'content': html, 'status_code': response.status}


async def fetch_with_sdk(url, sdk_client):
    """Fetch URL using BrightData Web Unlocker SDK (handles JS rendering, bot bypass)."""
    if sdk_client is None:
        return {'url': url, 'content': None, 'status_code': 503}

    try:
        result = await sdk_client.scrape_url(url, timeout=120)
        if not result.success:
            raise ValueError(result.error or "Scrape returned unsuccessful")
        if not result.data:
            raise ValueError("No content received from BrightData")
        return {'url': url, 'content': result.data, 'status_code': 200}
    except Exception as e:
        logger.error(f"BrightData SDK error for {url}: {e}")
        return {'url': url, 'content': None, 'status_code': 422}


async def crawl_page(url, render_js=True, sdk_client=None):
    """Crawl a URL with optional JS rendering.

    - render_js=False: aiohttp direct (free) with SDK fallback on failure/non-2xx
    - render_js=True: SDK directly (handles JS rendering server-side)
    """
    logger.info(f"Crawling {url} with {'JS rendering (SDK)' if render_js else 'no JS rendering (aiohttp)'}")

    if render_js:
        return await fetch_with_sdk(url, sdk_client)

    try:
        result = await fetch_with_aiohttp(url)
        if 200 <= result['status_code'] < 300:
            return result
        logger.info(f"aiohttp returned {result['status_code']} for {url}, falling back to SDK")
        return await fetch_with_sdk(url, sdk_client)
    except Exception as e:
        logger.info(f"aiohttp failed for {url}: {e}, falling back to SDK")
        return await fetch_with_sdk(url, sdk_client)
