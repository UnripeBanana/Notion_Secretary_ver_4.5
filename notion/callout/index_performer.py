from collector.data_reader.index_data_reader import index_data_reader
from collector.data_reader.price_data_reader import price_data_reader
from datetime import datetime, timedelta
from notion.client import notion
from notion.callout.index_updator import index_updator

def index_performer():
    #-----------------------------------------------------------------------------------
    # 1. 지표 데이터 일괄 수집 및 데이터 세팅
    #-----------------------------------------------------------------------------------
    today = datetime.now()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    targets = [
        {
            "call_out_ID": "a086e5aee08382cba0fc01fb0c3cc4e1",
            "title": "KOSPI",
            "df": index_data_reader(5, "KOSPI"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Image_Secretary_ver_4.5/main/data/image/market_index/KOSPI_1825days_chart.png"
        },
        {
            "call_out_ID": "8be6e5aee083836680c401a038d0b91e",
            "title": "달러/원 환율",
            "df": price_data_reader(5, "USD-KRW"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Image_Secretary_ver_4.5/main/data/image/price/USD-KRW_1825days_chart.png"
        },
        {
            "call_out_ID": "7076e5aee08382a69a1901781f0d29f5",
            "title": "국제금 / 달러 인덱스",
            "df": price_data_reader(5, "International_Gold"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Image_Secretary_ver_4.5/main/data/image/price/International_Gold_X_Dolar_Index_1825days_chart.png"
        }
    ]
    
    for target in targets:
        index_updator(target)
