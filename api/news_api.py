from fastapi import APIRouter, Query
from news_crawler.crawler import crawl_naver_news

router = APIRouter()

# Query 사용시 parameter가 없을 경우 자동으로 400에러 발생)
@router.get("")
async def read_root(category: str = Query(..., description="News category")):
    return crawl_naver_news(category)