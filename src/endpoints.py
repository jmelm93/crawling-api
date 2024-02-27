from fastapi import APIRouter, HTTPException
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
async def crawl(request: CrawlRequest):
    try:
        response = await crawl_page(request.url, render_js=request.render_js)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
