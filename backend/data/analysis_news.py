import os
from openai import OpenAI

def get_company_news_summary(company: str, top_k: int = 10):
    # 실제로는 DB/벡터DB에서 해당 기업 관련 summary top_k개 추출
    # 예시 데이터
    return [
        {"date": "2024-06-01", "headline": "2분기 실적 발표", "summary": "삼성전자는 2분기 영업이익이 20% 증가했다고 발표했다. 반도체 부문이 실적을 견인했다."},
        {"date": "2024-05-28", "headline": "차세대 반도체 투자", "summary": "삼성전자는 차세대 반도체 생산라인에 10조원을 투자할 계획을 밝혔다."},
        # ... 최대 top_k개
    ]

def generate_analysis_report(news_list, company: str):
    news_str = "\n".join(
        [f"{i+1}. [{n['date']}] {n['headline']}: {n['summary']}" for i, n in enumerate(news_list)]
    )
    prompt = f"""
아래는 {company}의 최근 주요 뉴스 요약입니다.

{news_str}

위 뉴스 요약을 바탕으로, 투자자 관점에서 {company}의 최근 동향, 실적, 성장성, 리스크, 향후 전망 등을 최대한 길고 깊이 있게, 구체적인 근거와 함께 분석 리포트를 작성해줘.
- 반드시 20문장 이상, 1000자 이상으로 써줘.
- 각 문단마다 뉴스 요약의 내용을 근거로 삼아, 구체적인 수치, 날짜, 이슈를 언급해줘.
- 마지막에는 투자자에게 도움이 될 만한 조언/인사이트도 포함해줘.
"""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

# 예시 실행
if __name__ == "__main__":
    company = "삼성전자"
    news_list = get_company_news_summary(company, top_k=10)
    report = generate_analysis_report(news_list, company)
    print(report)
