import asyncio
import json
from typing import List
from httpx import AsyncClient, Response
from parsel import Selector

client = AsyncClient(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
    },
    follow_redirects=True,
    # http2=True,  # enable http2 to reduce block chance
    timeout=30,
)


def parse_property(data):
    """parse rightmove property data to only necessary fields"""
    return data


def find_json_objects(text: str, decoder=json.JSONDecoder()):
    """Find JSON objects in text, and generate decoded JSON data"""
    pos = 0
    while True:
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1


# This function will find the PAGE_MODEL javascript variable and extract it 
def extract_property(response: Response) -> dict:
    """extract property data from rightmove PAGE_MODEL javascript variable"""
    selector = Selector(response.text)
    data = selector.xpath("//script[contains(.,'PAGE_MODEL = ')]/text()").get()
    if not data:
        print(f"page {response.url} is not a property listing page")
        return
    json_data = list(find_json_objects(data))[0]
    return json_data["propertyData"]


# this is our main scraping function that takes urls and returns the data
async def scrape_properties(urls: List[str]) -> List[dict]:
    """Scrape Rightmove property listings for property data"""
    to_scrape = [client.get(url) for url in urls]
    properties = []
    for response in asyncio.as_completed(to_scrape):
        response = await response
        properties.append(parse_property(extract_property(response)))
    return properties


async def get_floorplan(urls: List[str]) -> List[str]:
    """Get floorplan image url from property page"""
    res = await scrape_properties(urls)
    return [r['floorplans'][0]['url'] for r in res]