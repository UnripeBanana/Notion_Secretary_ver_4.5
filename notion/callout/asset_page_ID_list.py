from notion.client import notion

def asset_page_ID_list(page):

    page_info = notion.pages.retrieve(page_id=page["id"])
    column_list = notion.blocks.children.list(block_id=page["id"])

    callout_ID_list = list()

    for i in range(len(column_list["results"])):
        if column_list["results"][i]["type"] == "column_list":
            column = notion.blocks.children.list(block_id=column_list["results"][i]["id"])
            for j in range(len(column["results"])):
                callout = notion.blocks.children.list(block_id=column["results"][j]["id"])
                for k in range(len(callout["results"])):
                    callout_ID_list.append({
                        "callout_ID": callout["results"][k]["id"],
                        "name": page["properties"]["종목"]["title"][0]["plain_text"]
                    })

    return callout_ID_list
