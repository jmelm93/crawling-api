from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from src.crawl_page import crawl_page

router = APIRouter(
    prefix="/crawl",
    tags=["crawl"],
    responses={404: {"description": "Not found"}},
)


class CrawlRequest(BaseModel):
    url: str
    render_js: bool

@router.post("", response_model=dict)
async def crawl(request: Request, body: CrawlRequest):
    try:
        sdk_client = getattr(request.app.state, "sdk_client", None)
        response = await crawl_page(body.url, render_js=body.render_js, sdk_client=sdk_client)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
