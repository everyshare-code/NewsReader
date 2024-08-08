import ray
from news_crawler.url_constructor import construct_url
from news_crawler.fetch_details import fetch_article_details
from core.config import settings
from core.redis_client import redis_client
from playwright.sync_api import sync_playwright
import json
from typing import List, Dict, Any
from chat.chat_model import news_bot

@ray.remote
def fetch_article_links(base_url: str, category_info: Dict[str, Any], category: str) -> List[str]:
    url = construct_url(base_url, category_info)
    article_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to URL: {url}")
        page.goto(url)
        page.wait_for_load_state('networkidle')
        print("Page loaded and network is idle")

        try:
            if category == 'flash':
                locator = page.locator("xpath=//*[@id='main_content']/div[2]/ul[1]/li")
            else:
                locator = page.locator("xpath=//*[contains(@id, 'SECTION_HEADLINE_LIST')]/li")

            elements = locator.all()
            print(f"Number of elements found: {len(elements)}")

            for element in elements:
                link_element = element.locator("a").first
                link = link_element.get_attribute("href")
                article_links.append(link)
        except Exception as e:
            print(f"An error occurred: {e}")

        browser.close()

    return article_links


def filter_new_links(article_links: List[str]) -> List[str]:
    new_links = []
    for link in article_links:
        if not redis_client.exists(link):
            new_links.append(link)
    return new_links


def save_article_to_redis(link: str, article_details: Dict[str, Any]) -> None:
    redis_client.set(link, json.dumps(article_details))


def get_article_from_redis(link: str) -> Dict[str, Any]:
    article_data = redis_client.get(link)
    return json.loads(article_data) if article_data else {}

def summarize_articles(article_details_list:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    contents = [{"article": article['content']}for article in article_details_list]
    summarizes = news_bot.summarize_contents(contents)
    for idx in range(len(article_details_list)):
        if not article_details_list[idx]['summarize']:
            article_details_list[idx]['summarize'] = summarizes[idx]
    return article_details_list


def crawl_naver_news(category: str, base_url: str = None, categories: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    config = settings.DEFAULT_CONFIG
    if base_url:
        config['urls']['base'] = base_url
    if categories:
        config['urls']['categories'].update(categories)

    ray.init(num_cpus=10)

    category_info = config['urls']['categories'][category]
    future_links = fetch_article_links.remote(config['urls']['base'], category_info, category)
    article_links = ray.get(future_links)

    new_article_links = filter_new_links(article_links)
    article_details_list = []

    # Fetch new articles and store in Redis
    futures_details = [fetch_article_details.remote(link) for link in new_article_links[:5]]
    new_article_details = ray.get(futures_details)

    for link, details in zip(new_article_links, new_article_details):
        save_article_to_redis(link, details)
        article_details_list.append(details)



    # Fetch cached articles from Redis
    cached_article_details = [get_article_from_redis(link) for link in article_links if link not in new_article_links]
    article_details_list.extend(cached_article_details)

    # Sort articles by the most recent and take the top 5
    article_details_list.sort(key=lambda x: x.get('date', ''), reverse=True)

    article_details_list = summarize_articles(article_details_list[:5])

    return article_details_list[:5]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Crawl Naver News")
    parser.add_argument('category', type=str, help='News category to crawl')

    args = parser.parse_args()
    news_data = crawl_naver_news(args.category)
    print(news_data)