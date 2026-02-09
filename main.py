import yfinance as yf
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from datetime import datetime

console = Console()

def get_stock_data(ticker_symbol):
    """주가 데이터 및 보조지표 계산"""
    ticker = yf.Ticker(ticker_symbol)
    
    # 1년치 데이터 가져오기
    df = ticker.history(period="1y")
    if df.empty:
        return None, None
    
    info = ticker.info
    
    # --- 보조지표 계산 (Engineering Logic) ---
    
    # 1. 이동평균선 (MA)
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # 2. 볼린저 밴드 (Bollinger Bands)
    std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['MA20'] + (std * 2)
    df['BB_Lower'] = df['MA20'] - (std * 2)
    
    # 3. RSI (상대강도지수)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df, info

def format_price(price):
    return f"{price:,.2f}"

def get_color(val):
    if val > 0: return "red" # 한국은 상승이 빨강
    elif val < 0: return "blue" # 하락이 파랑
    return "yellow"

def display_dashboard(symbol):
    df, info = get_stock_data(symbol)
    if df is None:
        console.print(f"[bold red]Error:[/bold red] {symbol} 데이터를 찾을 수 없습니다.")
        return

    # 최신 데이터
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    change = latest['Close'] - prev['Close']
    pct_change = (change / prev['Close']) * 100
    
    color = get_color(change)
    arrow = "▲" if change > 0 else "▼" if change < 0 else "-"
    
    # === 1. 헤더 (종목명 및 현재가) ===
    header_text = Text()
    header_text.append(f"{info.get('shortName', symbol)} [{symbol}] : ", style="bold white")
    header_text.append(arrow, style=color)
    
    console.print(Panel(header_text, style=color))

    # === 2. 가격 변동 히스토리 (Recent History) ===
    table = Table(title="일자별 가격 변동 (최근 10일)", box=None)
    table.add_column("일자", justify="left", style="cyan", no_wrap=True)
    table.add_column("가격", justify="right")
    table.add_column("변동", justify="right")
    table.add_column("비고", justify="left")

    recent_df = df.tail(10).iloc[::-1] # 최근 10일 역순
    
    # 10일 고점/저점 계산
    ten_day_high = recent_df['Close'].max()
    ten_day_low = recent_df['Close'].min()

    for date, row in recent_df.iterrows():
        day_change = row['Close'] - row['Open'] # 시가 대비 종가 등락으로 단순화
        day_pct = (day_change / row['Open']) * 100
        c_code = get_color(day_change)
        
        note = ""
        if row['Close'] == ten_day_high: note = "🔴 10일 고점"
        elif row['Close'] == ten_day_low: note = "🔵 10일 저점"
        
        table.add_row(
            date.strftime("%Y-%m-%d"),
            format_price(row['Close']),
            f"[{c_code}]{day_pct:+.2f}%[/{c_code}]",
            note
        )
    
    console.print(table)
    console.print("\n")

    # === 3. 종목 분석 (Technical Analysis) ===
    analysis_panel = Text()
    
    # 기본 정보
    mkt_cap = info.get('marketCap', 0) / 1000000000000 # 조 단위
    analysis_panel.append(f"기본 정보\n", style="bold underline white")
    analysis_panel.append(f" 시가총액: {mkt_cap:.2f}조 달러\n")
    analysis_panel.append(f" 상장위치: {info.get('exchange', 'N/A')}\n\n")
    
    # 52주 정보
    high_52 = df['Close'].tail(252).max()
    low_52 = df['Close'].tail(252).min()
    cur_price = latest['Close']
    
    # 위치 계산 (저점 대비 얼마나 올랐나)
    pos_52 = (cur_price - low_52) / (high_52 - low_52) * 100
    
    analysis_panel.append(f"종목 분석 (Technical)\n", style="bold underline white")
    analysis_panel.append(f" 52주 최저/최고: {format_price(low_52)} ~ {format_price(high_52)}\n")
    analysis_panel.append(f" 현재 위치: 바닥에서 {pos_52:.1f}% 지점\n")
    
    analysis_panel.append(f" 볼린저 밴드: [상단:{format_price(latest['BB_Upper'])}] [하단:{format_price(latest['BB_Lower'])}]\n")
    analysis_panel.append(f" 이동평균선: [5일:{format_price(latest['MA5'])}] [20일:{format_price(latest['MA20'])}]\n")
    
    rsi_val = latest['RSI']
    rsi_status = "과매수(Sell)" if rsi_val >= 70 else "과매도(Buy)" if rsi_val <= 30 else "중립"
    analysis_panel.append(f" RSI(14): {rsi_val:.2f} - {rsi_status}\n")
    
    # 지지/저항선 (피벗 포인트 약식 계산)
    pivot = (latest['High'] + latest['Low'] + latest['Close']) / 3
    r1 = (2 * pivot) - latest['Low']
    s1 = (2 * pivot) - latest['High']
    
    analysis_panel.append(f" 지지선(S1): 💀 {format_price(s1)}\n")
    analysis_panel.append(f" 저항선(R1): 🧱 {format_price(r1)}\n")
    
    console.print(Panel(analysis_panel, title="Deep Dive Analysis", border_style="green"))
    
    # 면책 조항
    console.print(Text("본 정보는 참고용이며, 판단의 책임은 본인에게 있음을 유의하시기 바랍니다.", style="dim italic justify_center"))

if __name__ == "__main__":
    # 서지님 관심사인 AI 반도체 대장주 엔비디아(NVDA)나 구글(GOOGL) 등을 넣어보세요
    display_dashboard("GOOGL")