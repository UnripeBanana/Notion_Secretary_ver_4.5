import requests
import pandas as pd

def stock_and_bond_data_reader(ticker):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = (
        f"https://polling.finance.naver.com/api/realtime"
        f"?query=SERVICE_ITEM:{ticker}"
    )

    data = requests.get(
        url,
        headers=headers,
        timeout=10
    ).json()

    krx_item = data["result"]["areas"][0]["datas"][0]

    if krx_item["ms"] == "OPEN" or krx_item["nxtOverMarketPriceInfo"] is None:
        nv = krx_item["nv"]
        cv = krx_item["cv"]
        cr = krx_item["cr"]
        ov = krx_item["ov"]
        hv = krx_item["hv"]
        lv = krx_item["lv"]

        # 하락이면 음수로 변경
        if krx_item["rf"] == "5":
            cv *= -1
            cr *= -1

    else:

        nv = float(
            krx_item["nxtOverMarketPriceInfo"]["overPrice"].replace(",", "")
        )
        cv = float(
            krx_item["nxtOverMarketPriceInfo"]["compareToPreviousClosePrice"].replace(",", "")
        )
        cr = float(
            krx_item["nxtOverMarketPriceInfo"]["fluctuationsRatio"]
        )
        ov = float(
            krx_item["nxtOverMarketPriceInfo"]["openPrice"].replace(",", "")
        )
        hv = float(
            krx_item["nxtOverMarketPriceInfo"]["highPrice"].replace(",", "")
        )
        lv = float(
            krx_item["nxtOverMarketPriceInfo"]["lowPrice"].replace(",", "")
        )
        
        
    return {
        "cd": krx_item["cd"],      # 티커
        "nm": krx_item["nm"],      # 종목명
        "nv": nv,      # 현재가
        "cv": cv,                  # 전일 대비 가격 변화(원)
        "cr": cr,                  # 등락률(%)
        "pcv": krx_item["pcv"],    # Previous Close Value, 전일종가
        "ov": ov,      # 시가
        "hv": hv,      # 고가
        "lv": lv,      # 저가
        "aq": krx_item["aq"],      # 거래량
        "aa": krx_item["aa"],      # 거래대금 : 하루동안 얼마가 거래되었는가 (평균 거래대금보다 많은 양이 거래될 시 신뢰도 있는 등락이라고 판단)
        "countOfListedStock": krx_item["countOfListedStock"]  # 상장주식수
    }

def gold_data_reader(code):

    if code in ["M04020000"]:
        category = "metals"
        name = "KRX 금현물"


    url = (
        "https://m.stock.naver.com/front-api/marketIndex/prices"
        f"?category={category}"
        f"&reutersCode={code}"
        f"&page=1"
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://m.stock.naver.com/"
    }

    response = requests.get(url, headers=headers)

    price_data = response.json()

    # 네이버 증권에서 받은 오리지널 데이터
    price_df = pd.DataFrame(price_data["result"])

    # 오리지널 데이터에서 불필요한 부분 제거
    price_df = price_df[["localTradedAt", "closePrice", "fluctuations", "fluctuationsRatio"]]

    # 기존에 사용 중인 명칭으로 변경
    price_df = price_df.rename(columns={
        "localTradedAt": "date",
        "closePrice": "close",
        "fluctuations": "change",
        "fluctuationsRatio": "rate"
    })

    # str -> int
    price_df["close"] = (
        price_df["close"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -. int
    price_df["change"] = (
        price_df["change"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -> float
    price_df["rate"] = (
        price_df["rate"]
        .astype(float)
    )

    # 사용자로부터 입력받은 데이터 입력
    price_df["code"] = code

    # 데이터프레임 컬럼 순서 설정
    price_df = price_df[
        ["date", "code", "close", "change", "rate"]
    ]

    return {
        "cd": str(price_df["code"][0]),      # 티커
        "nm": str(name),      # 종목명
        "nv": float(price_df["close"][0]),      # 현재가
        "cv": float(price_df["change"][0]),      # 전일 대비 가격 변화(원)
        "cr": float(price_df["rate"][0])      # 등락률(%)
    }

def asset_reader(ticker):

    if ticker in ["M04020000"]:
        data = gold_data_reader(ticker)

    else:
        data = stock_and_bond_data_reader(ticker)

    return data
