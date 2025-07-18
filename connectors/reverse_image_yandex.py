import requests
from bs4 import BeautifulSoup

def yandex_reverse_image_search(image_bytes: bytes) -> dict:
    files = {'upfile': ('image.jpg', image_bytes, 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.post(
        'https://yandex.com/images/search',
        params=params,
        files=files,
        headers=headers,
        allow_redirects=False
    )
    if 'Location' not in response.headers:
        return {"error": "Yandex did not return a result URL"}
    result_url = "https://yandex.com" + response.headers['Location']

    page = requests.get(result_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    results = []
    for item in soup.select('.CbirSites-Item'):
        title = item.select_one('.CbirSites-ItemTitle')
        link = item.select_one('.CbirSites-ItemTitle a')
        img = item.select_one('img')
        results.append({
            "title": title.text.strip() if title else "",
            "url": link['href'] if link else "",
            "thumbnail": img['src'] if img else ""
        })
    best_guess = soup.select_one('.CbirItemTitle')
    return {
        "best_guess": best_guess.text.strip() if best_guess else "",
        "matches": results,
        "yandex_url": result_url
    }