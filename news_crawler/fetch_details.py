import ray
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def clean_text(text):
    return text.replace('\xa0', ' ').strip() if text else ""

@ray.remote
def fetch_article_details(article_link):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(article_link)
            page.wait_for_load_state('networkidle')

            soup = BeautifulSoup(page.content(), 'html.parser')
            title = soup.select_one("div.media_end_head_title")
            publish_date = soup.select_one("span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME")
            article = soup.select_one('div#newsct_article')
            image = soup.select_one('meta[property="og:image"]')

            browser.close()

            return {
                "title": clean_text(title.text),
                "date": clean_text(publish_date.text),
                "content": clean_text(article.text),
                "image_link": image['content'] if image else "",
                "article_link": article_link,
                "summarize": ""
            }
    except Exception as e:
        print(f"Error fetching article details: {e}")
        return None
