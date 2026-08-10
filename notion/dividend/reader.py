from notion.client import notion

def dividend_reader(page):
	props = page["properties"]

	properties = {
		"page_id": page["id"],
		"dividend": props["배당금"]["formula"]["number"],
		"profit_saved": props["순수익 반영"]["checkbox"]
	}

	return properties
