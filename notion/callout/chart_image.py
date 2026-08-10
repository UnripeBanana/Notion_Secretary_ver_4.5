def chart_image(page):
    # 1. 기간별 텍스트 매핑 테이블 사전 정의
    PERIOD_MAP = {
        "3개월 차트": "90days",
        "1년 차트": "365days",
        "5년 차트": "1825days"
    }

    callout_data = callout_ID_list(page)

    for callout in callout_data:
        callout_id = callout["callout_ID"]
        callout_name = callout["name"]

        # 2. 자식 블록 목록 단 1회 조회
        blocks = notion.blocks.children.list(block_id=callout_id)
        results = blocks.get("results", [])

        # 3. 자산 이름 및 필드 설정 (티커 안전 검사)
        if callout_name == "KRX 금현물":
            name = "KRX_Gold"
            field = "price"
        else:
            ticker_list = page["properties"].get("티커", {}).get("rich_text", [])
            ticker = ticker_list[0]["plain_text"] if ticker_list else "UNKNOWN"
            name = f"{callout_name}_{ticker}"
            field = "domestic_stock"

        # 4. 기존 블록 순회: period 추출 및 기존 블록 삭제
        p_text = "90days"       # 기본값 설정
        period_title = "3개월 차트"

        for block in results:
            # heading_2 타입 블록에서 period 추출
            if block["type"] == "heading_2":
                rich_text = block["heading_2"].get("rich_text", [])
                if rich_text:
                    content = rich_text[0]["text"]["content"].strip()
                    if content in PERIOD_MAP:
                        period_title = content
                        p_text = PERIOD_MAP[content]

            # 기존 블록 삭제
            notion.blocks.delete(block_id=block["id"])

        # 5. 차트 URL 생성
        chart_url = f"https://raw.githubusercontent.com/UnripeBanana/Image_Secretary_ver_4.5/main/data/image/{field}/{name}_{p_text}_chart.png"
        candle_chart_url = f"https://raw.githubusercontent.com/UnripeBanana/Image_Secretary_ver_4.5/main/data/image/{field}/{name}_{p_text}_day_candle_chart.png"

        # 6. 추가할 노션 블록 데이터 동적 생성
        new_children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": period_title}}],
                    "is_toggleable": False,
                    "color": "default",
                },
            },
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block",
                "type": "image",
                "image": {"caption": [], "type": "external", "external": {"url": chart_url}},
            },
            {"object": "block", "type": "divider", "divider": {}},
        ]

        # KRX 금현물이 아닌 일반 주식일 경우 선형 차트 및 구분선 추가
        if callout_name != "KRX 금현물":
            new_children.extend([
                {
                    "object": "block",
                    "type": "image",
                    "image": {"caption": [], "type": "external", "external": {"url": candle_chart_url}},
                },
                {"object": "block", "type": "divider", "divider": {}},
            ])

        # 7. 새 블록 일괄 추가 (1회 호출)
        notion.blocks.children.append(
            block_id=callout_id,
            children=new_children,
        )
