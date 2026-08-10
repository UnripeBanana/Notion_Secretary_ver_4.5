from notion.config import NOTION_DIVIDEND_DB_ID
from notion.get_all_pages import get_all_pages

#-----------------------------------------
# 배당금 DB 업데이트
#-----------------------------------------
from notion.dividend.reader import dividend_reader
from notion.dividend.updator import dividend_updator

for page in get_all_pages(NOTION_DIVIDEND_DB_ID):
    # 각 페이지별로 데이터 읽기
    properties = dividend_reader(page)
    
    # 노션에 데이터 업데이트
    dividend_updator(properties)
