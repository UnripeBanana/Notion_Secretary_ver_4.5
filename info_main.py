from notion.config import 
from notion.info.reader import info_reader
from notion.info.updator import info_updator
from notion.get_all_pages import get_all_pages

for page in get_all_pages(NOTION_ASSET_DB_ID):
    # 티커 데이터 추출
    #print(page["properties"]["티커"]["rich_text"][0]["plain_text"])

    ticker = page["properties"]["티커"]["rich_text"][0]["text"]["content"]
    if not ticker:
        continue

    properties = asset_reader(ticker)

    asset_updator(page, properties)

    """

    # 네이버증권에서 데이터 받아오기
    domestic_stock_info = get_domestic_stock_info(ticker) # dictionary

    # 노션에 데이터 업로드
    asset_updator(page, domestic_stock_info)
    """
