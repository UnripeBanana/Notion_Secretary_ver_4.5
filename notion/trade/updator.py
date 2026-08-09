from notion.client import notion 
from notion.trade.net_profit import net_profit
from notion.rich_text import rich_text
from utils.day_log import today_and_time_is

def trade_updator(results):
    for id, raw_prop in results.items():
        properties = {
            "잔량": {"number": raw_prop["remaining"]},
            "실현수익": {"number": raw_prop["profit"]},
            "마지막 업데이트": rich_text(today_and_time_is())
        }

        if raw_prop["profit"] and not raw_prop["profit_saved"]: 
            net_profit("trade", raw_prop["profit"])
            properties["순수익 반영"] = {
                "checkbox": True
            }

        notion.pages.update(
            page_id = id,
            properties = properties
        )
