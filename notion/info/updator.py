from notion.rich_text import rich_text
from utils.day_log import today_and_time_is

def info_updator(page, properties):

    updated_properties = {
        "현재가_깃허브": {"number": properties["nv"]},
        "전일대비_깃허브": {"number": properties["cv"]},
        "등락률_깃허브": {"number": properties["cr"]},
        "마지막 업데이트": rich_text(today_and_time_is())
    }

    notion.pages.update(
        page_id = page["id"],
        properties = updated_properties
    )
