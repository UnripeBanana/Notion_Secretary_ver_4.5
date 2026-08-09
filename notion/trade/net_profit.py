from notion.config import NOTION_NET_PROFIT_DB_ID
from notion.client import notion
from notion.rich_text import rich_text
from utils.day_log import today_and_time_is

def net_profit(prop, profit):

    trade_profit = profit if prop == "trade" else 0
    dividend_profit = profit if prop == "dividend" else 0
    
    notion.pages.create(
        parent={
            "database_id": NOTION_NET_PROFIT_DB_ID
        },
        
        properties={
            "시세차익": {"number": trade_profit},
            "배당이익": {"number": dividend_profit},
            "마지막 업데이트": rich_text(today_and_time_is())
        }
    )
