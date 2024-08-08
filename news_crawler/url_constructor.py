from urllib.parse import urlencode

def construct_url(base_url: str, category_info: dict) -> str:
    url = category_info['url']
    if 'params' in category_info:
        params = category_info['params']
        query_string = urlencode(params)
        full_url = f"{base_url}{url}?{query_string}"
    else:
        full_url = f"{base_url}{url}"
    print(f"Constructed URL: {full_url}")
    return full_url
