from notion.client import notion
from notion.trade.net_profit import net_profit

def update_dividend(properties):
	if properties["dividend"] and not properties["profit_saved"]: 
		net_profit("dividend", properties["dividend"])
		new_properties = {"순수익 반영": {"checkbox": True}}

		notion.pages.update(
			page_id = properties["page_id"],
			properties = new_properties
		)
