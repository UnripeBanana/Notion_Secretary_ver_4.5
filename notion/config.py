# 환경변수 모으기

import os

# 노션에 연결중인 현재가 DB의 토큰값.
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# 자산 보유현황 DB
NOTION_INFO_DB_ID = os.environ["NOTION_INFO_DB_ID"]

# 통합 거래내역 DB
NOTION_TRADE_DB_ID = os.environ["NOTION_TRADE_DB_ID"]

# 배당금 DB
NOTION_DIVIDEND_DB_ID = os.environ["NOTION_DIVIDEND_DB_ID"]

# 순수익 DB 링크
NOTION_NET_PROFIT_DB_ID = os.environ["NOTION_NET_PROFIT_DB_ID"]
