import ray
from bs4 import BeautifulSoup

@ray.remote
def extract_info(element_html, category):
    try:
        soup = BeautifulSoup(element_html, 'html.parser')

        if category == 'flash':
            title_element = soup.select_one("dt.photo a")
            image_element = soup.select_one("dt.photo a img")
            description_element = soup.select_one("dd span.lede")
            source_element = soup.select_one("dd span.writing")
            date_element = soup.select_one("dd span.date")
        else:
            title_element = soup.select_one("a.sa_text_title")
            image_element = soup.select_one("img")
            description_element = soup.select_one("div.sa_text_lede")

        title = title_element.get_text(strip=True) if title_element else ""
        link = title_element['href'] if title_element else ""
        image_link = image_element['src'] if image_element else ""
        description = description_element.get_text(strip=True) if description_element else ""

        if category == 'flash':
            source = source_element.get_text(strip=True) if source_element else ""
            date = date_element.get_text(strip=True) if date_element else ""
            return {
                "title": title,
                "article_link": link,
                "image_link": image_link,
                "description": description,
                "date": date
            }
        else:
            return {
                "title": title,
                "article_link": link,
                "image_link": image_link,
                "description": description
            }
    except Exception as e:
        print(f"Error extracting info: {e}")
        return None
