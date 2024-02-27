import os
import aiohttp  
import logging
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# chrome user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'


def get_proxy(
    host=os.getenv("PROXY_HOST"),
    username=os.getenv("PROXY_USERNAME"), 
    password=os.getenv("PROXY_PASSWORD")
):
    return {
        'server': f'http://{host}',
        'username': username,
        'password': password
    }


async def fetch_with_aiohttp(url, user_agent=user_agent, use_proxy=False):
    headers = { "User-Agent": user_agent }
    proxy = None
    
    if use_proxy:
        proxy_details = get_proxy()
        proxy = f"http://{proxy_details['username']}:{proxy_details['password']}@{proxy_details['server']}"
        
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy, headers=headers) as response:
                html = await response.text()
                return {'url': url, 'content': html, 'status_code': 200}
        except Exception as e:
            if not use_proxy:
                logging.info("Retrying non-JS fetch with proxy...")
                return await fetch_with_aiohttp(url, use_proxy=True)
            else:
                logging.info("Failed non-JS fetch even with proxy. Giving up.")
                return {'url': url, 'content': None, 'status_code': 422}


async def fetch_with_playwright(url, user_agent=user_agent, use_proxy=False):
    try:
        async with async_playwright() as p:
            browser_type = p.chromium  # You can choose chromium, firefox, or webkit
            launch_options = {}

            if use_proxy:
                proxy = get_proxy()
                launch_options['proxy'] = {
                    'server': proxy['server'],
                    'username': proxy['username'],
                    'password': proxy['password'],
                }

            browser = await browser_type.launch(**launch_options)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()
            response = await page.goto(url)
            content = await page.content()  
            status_code = response.status
            await browser.close()
            return {'url': url, 'content': content, 'status_code': status_code}
    
    except Exception as e:
        logging.info(f"An error occurred during JS fetch: {e}")
        if not use_proxy:
            logging.info("Retrying JS fetch with proxy...")
            return await fetch_with_playwright(url, use_proxy=True)
        else:
            logging.info("Failed JS fetch even with proxy. Giving up.")
            return {'url': url, 'content': None, 'status_code': 422}


async def crawl_page(url, render_js=True):
    logging.info(f"Crawling {url} with {'JS rendering' if render_js else 'no JS rendering'}")
    
    try:
        if not render_js:
            page_object = await fetch_with_aiohttp(url)
        else:
            page_object = await fetch_with_playwright(url)
        return page_object
    
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return {'url': url, 'content': None, 'status_code': 500}