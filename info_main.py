from notion.config import NOTION_INFO_DB_ID
from notion.info.reader import info_reader
from notion.info.updator import info_updator
from notion.get_all_pages import get_all_pages
from notion.callout.chart_image import chart_image

for page in get_all_pages(NOTION_INFO_DB_ID):

    ticker = page["properties"]["티커"]["rich_text"][0]["text"]["content"]
    if not ticker:
        continue

    properties = info_reader(ticker)
    info_updator(page, properties)

    chart_image(page)
