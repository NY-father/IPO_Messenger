from pykrx import stock
import FinanceDataReader as fdr
import datetime
import pandas as pd
from kakao_message import *
import time
import traceback

# ----------------------------------------------------------------------------------
# HDI, HKI 종가 피드 보내기
def get_st_info(st_type = ['DJI','INDEX','HDI', 'HKI']):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 주가 정보 전송 -')
    today = datetime.datetime.today().strftime('%Y%m%d')
    s_date = datetime.datetime.today() - datetime.timedelta(days=7)
    s_date = s_date.strftime('%Y%m%d')
    e_date = datetime.datetime.today()
    e_date = e_date.strftime('%Y%m%d')
    
    
    #다우지수
    st_DJI = fdr.DataReader('DJI', s_date, e_date)
    st_DJI['당일_변화율'] = st_DJI.loc[:,['Close']].pct_change() * 100
    
    
    #KOSPI, KODAQ
    st_KOSPI = stock.get_index_ohlcv_by_date(s_date,e_date,"1001",name_display=True)
    st_KOSPI['당일_변화율'] = st_KOSPI.loc[:,['종가']].pct_change() * 100
    
    st_KOSDAQ = stock.get_index_ohlcv_by_date(s_date,e_date,"2001",name_display=True)
    st_KOSDAQ['당일_변화율'] = st_KOSDAQ.loc[:,['종가']].pct_change() * 100
    
        
    #현대두산인프라코어
    st_HDI = stock.get_market_ohlcv_by_date(s_date,e_date,"042670",name_display=True)
    st_HDI['당일_변화율'] = st_HDI.loc[:,['종가']].pct_change() * 100
    st_HDI['수익률'] = st_HDI.loc[:,['종가']] / 5930 * 100 - 100
    st_HDI['수익금'] = (st_HDI.loc[:,['종가']] / 5930 - 1) * 8650
    st_HDI = st_HDI.loc[:,['종가','당일_변화율','수익률','수익금']]
    #print(st_HDI.iloc[-1:,:],'\n')
    
    
    #HK inno.N
    st_HKinnoN = stock.get_market_ohlcv_by_date(s_date,e_date,"195940",name_display=True)
    st_HKinnoN['당일_변화율'] = st_HKinnoN.loc[:,['종가']].pct_change() * 100
    st_HKinnoN['수익률'] = st_HKinnoN.loc[:,['종가']] / 59000 * 100 - 100
    st_HKinnoN['수익금'] = (st_HKinnoN.loc[:,['종가']] / 59000 - 1) * 13500
    st_HKinnoN = st_HKinnoN.loc[:,['종가','당일_변화율','수익률','수익금']]
    #print(st_HKinnoN.iloc[-1:,:],'\n')
    
    text = '오늘의 주가({})'.format(datetime.datetime.today().strftime('%Y-%m-%d'))
    text = text + '\n\n현대두산인프라코어'
    text = text + '\n 종가 : {}원'.format(st_HDI.iloc[-1,0])
    text = text + '\n 변화율: {:0.1f}%'.format(st_HDI.iloc[-1,1])
    text = text + '\n 수익률: {:0.1f}%'.format(st_HDI.iloc[-1,2])
    text = text + '\n 수익금: {:0.1f}만원'.format(st_HDI.iloc[-1,3])
    
    text = text + '\n\nHK inno.N'
    text = text + '\n 종가 : {}원'.format(st_HKinnoN.iloc[-1,0])
    text = text + '\n 변화율: {:0.1f}%'.format(st_HKinnoN.iloc[-1,1])
    text = text + '\n 수익률: {:0.1f}%'.format(st_HKinnoN.iloc[-1,2])
    text = text + '\n 수익금: {:0.1f}만원'.format(st_HKinnoN.iloc[-1,3])
        
   
    text_DJI_Title = '다우지수'
    text_DJI_Title = text_DJI_Title + '\n 종가 : {:0.1f} ({:0.1f}%)'.format(st_DJI['Close'][-1],st_DJI.iloc[-1,-1])
    image_DJI = 'https://t1.daumcdn.net/finance/chart/us/stock/m3/DJI.png'
    image_link_DJI = 'https://m.stock.naver.com/worldstock/index/.DJI/total'



    text_INDEX_Title = 'KOSPI'
    text_INDEX_Title = text_INDEX_Title + '\n 종가 : {:0.1f} ({:0.1f}%)'.format(st_KOSPI.iloc[-1,0],st_KOSPI.iloc[-1,-1])
    text_INDEX_Contents = 'KOSDAQ'
    text_INDEX_Contents = text_INDEX_Contents + '\n 종가 : {}원 ({:0.1f}%)'.format(st_KOSDAQ.iloc[-1,0],st_KOSDAQ.iloc[-1,-1])
    #INDEX_price = [st_KOSPI.iloc[-1,0], st_KOSPI.iloc[-1,1], st_KOSDAQ.iloc[-1,0], st_KOSDAQ.iloc[-1,1]] # 종가, 변화율, 수익금, 수익금(%)
    #image_INDEX = 'https://t1.daumcdn.net/finance/chart/kr/stock/m3/D0011001.png'
    image_INDEX = 'https://t1.daumcdn.net/finance/chart/kr/stock/m3/KGG01P.png'
    image_link_INDEX = 'https://m.stock.naver.com/domestic/capitalization/KOSPI'
    

    text_HDI_Title = '현대두산인프라코어'
    #text_HDI_Title = text_HDI_Title + '\n 종가 : {}원'.format(st_HDI.iloc[-1,0])
    text_HDI_Contents = '변화율: {:0.1f}%'.format(st_HDI.iloc[-1,1])
    text_HDI_Contents = text_HDI_Contents + '\n 수익금: {:0.1f}만원 ({:0.1f}%)'.format(st_HDI.iloc[-1,3],st_HDI.iloc[-1,2])
    HDI_price = [st_HDI.iloc[-1,0], st_HDI.iloc[-1,1], st_HDI.iloc[-1,3], st_HDI.iloc[-1,2]] # 종가, 변화율, 수익금, 수익금(%)
    #image_HDI = 'https://ssl.pstatic.net/imgfinance/chart/item/candle/day/042670.png'
    image_HDI = 'https://t1.daumcdn.net/finance/chart/kr/candle/d/A042670.png?timestamp={}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    image_link_HDI = 'https://m.stock.naver.com/domestic/stock/042670/total'
    
    
    text_HKI_Title = 'HK inno.N'
    #text_HKI_Title = text_HKI_Title + '\n 종가 : {}원'.format(st_HKinnoN.iloc[-1,0])
    text_HKI_Contents = '변화율: {:0.1f}%'.format(st_HKinnoN.iloc[-1,1])
    text_HKI_Contents = text_HKI_Contents + '\n 수익금: {:0.1f}만원 ({:0.1f}%)'.format(st_HKinnoN.iloc[-1,3],st_HKinnoN.iloc[-1,2])
    HKI_price = [st_HKinnoN.iloc[-1,0], st_HKinnoN.iloc[-1,1], st_HKinnoN.iloc[-1,3], st_HKinnoN.iloc[-1,2]] # 종가, 변화율, 수익금, 수익금(%)
    #image_HKI = 'https://ssl.pstatic.net/imgfinance/chart/item/candle/day/195940.png'
    image_HKI = 'https://t1.daumcdn.net/finance/chart/kr/candle/d/A195940.png?timestamp={}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    image_link_HKI = 'https://m.stock.naver.com/domestic/stock/195940/total'
    

   
    # --------------------------------
    
    if datetime.datetime.today().weekday() not in [5,6]:
        for st in st_type:
            if st == 'DJI':
                sendToFrdMessageFeed(text_title=text_DJI_Title, text_contents="", frd_name=['김익현',], image_url=image_DJI, image_link_url=image_link_DJI)
            elif st == 'INDEX':
                sendToFrdMessageFeed(text_title=text_INDEX_Title, text_contents=text_INDEX_Contents, frd_name=['김익현',], image_url=image_INDEX, image_link_url=image_link_INDEX)
            elif st == 'HDI':
                sendToFrdMessageFeed_st(text_title=text_HDI_Title, text_contents=text_HDI_Contents, frd_name=['김익현',], image_url=image_HDI, image_link_url=image_link_HDI, price=HDI_price)
            elif st == 'HKI':
                sendToFrdMessageFeed_st(text_title=text_HKI_Title, text_contents=text_HKI_Contents, frd_name=['김익현',], image_url=image_HKI, image_link_url=image_link_HKI, price=HKI_price)
                #sendToFrdMessageFeed(text_title=text_HKI_Title, text_contents="오늘도 수고 많았어~~", frd_name=['이태은',], image_url=image_HKI, image_link_url=image_link_HKI)
        
        
    print('-' * 70)






# ----------------------------------------------------------------------------------
# HDI, HKI 종가 피드 보내기
def get_st_info_krx(tiker):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 주가 정보 전송 -')
    today = datetime.datetime.today().strftime('%Y%m%d')
    s_date = datetime.datetime.today() - datetime.timedelta(days=7)
    s_date = s_date.strftime('%Y%m%d')
    e_date = datetime.datetime.today()
    e_date = e_date.strftime('%Y%m%d')
    
    
    st = stock.get_market_ohlcv_by_date(s_date,e_date,ticker,name_display=True)
    st['당일_변화율'] = st.loc[:,['종가']].pct_change() * 100
    st = st.loc[:,['종가','당일_변화율','수익률','수익금']]

    
    text = '오늘의 주가({})'.format(datetime.datetime.today().strftime('%Y-%m-%d'))
    text = text + '\n\n현대두산인프라코어'
    text = text + '\n 종가 : {}원'.format(st.iloc[-1,0])
    text = text + '\n 변화율: {:0.1f}%'.format(st.iloc[-1,1])
    
    text = text + '\n\nHK inno.N'
    text = text + '\n 종가 : {}원'.format(st_HKinnoN.iloc[-1,0])
    text = text + '\n 변화율: {:0.1f}%'.format(st_HKinnoN.iloc[-1,1])
    text = text + '\n 수익률: {:0.1f}%'.format(st_HKinnoN.iloc[-1,2])
    text = text + '\n 수익금: {:0.1f}만원'.format(st_HKinnoN.iloc[-1,3])
        


    text_INDEX_Title = 'KOSPI'
    text_INDEX_Title = text_INDEX_Title + '\n 종가 : {:0.1f} ({:0.1f}%)'.format(st_KOSPI.iloc[-1,0],st_KOSPI.iloc[-1,-1])
    text_INDEX_Contents = 'KOSDAQ'
    text_INDEX_Contents = text_INDEX_Contents + '\n 종가 : {}원 ({:0.1f}%)'.format(st_KOSDAQ.iloc[-1,0],st_KOSDAQ.iloc[-1,-1])
    #INDEX_price = [st_KOSPI.iloc[-1,0], st_KOSPI.iloc[-1,1], st_KOSDAQ.iloc[-1,0], st_KOSDAQ.iloc[-1,1]] # 종가, 변화율, 수익금, 수익금(%)
    #image_INDEX = 'https://t1.daumcdn.net/finance/chart/kr/stock/m3/D0011001.png'
    image_INDEX = 'https://t1.daumcdn.net/finance/chart/kr/stock/m3/KGG01P.png'
    image_link_INDEX = 'https://m.stock.naver.com/domestic/capitalization/KOSPI'
    

    text_HDI_Title = '현대두산인프라코어'
    #text_HDI_Title = text_HDI_Title + '\n 종가 : {}원'.format(st_HDI.iloc[-1,0])
    text_HDI_Contents = '변화율: {:0.1f}%'.format(st_HDI.iloc[-1,1])
    text_HDI_Contents = text_HDI_Contents + '\n 수익금: {:0.1f}만원 ({:0.1f}%)'.format(st_HDI.iloc[-1,3],st_HDI.iloc[-1,2])
    HDI_price = [st_HDI.iloc[-1,0], st_HDI.iloc[-1,1], st_HDI.iloc[-1,3], st_HDI.iloc[-1,2]] # 종가, 변화율, 수익금, 수익금(%)
    #image_HDI = 'https://ssl.pstatic.net/imgfinance/chart/item/candle/day/042670.png'
    image_HDI = 'https://t1.daumcdn.net/finance/chart/kr/candle/d/A042670.png?timestamp={}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    image_link_HDI = 'https://m.stock.naver.com/domestic/stock/042670/total'
    
    
    text_HKI_Title = 'HK inno.N'
    #text_HKI_Title = text_HKI_Title + '\n 종가 : {}원'.format(st_HKinnoN.iloc[-1,0])
    text_HKI_Contents = '변화율: {:0.1f}%'.format(st_HKinnoN.iloc[-1,1])
    text_HKI_Contents = text_HKI_Contents + '\n 수익금: {:0.1f}만원 ({:0.1f}%)'.format(st_HKinnoN.iloc[-1,3],st_HKinnoN.iloc[-1,2])
    HKI_price = [st_HKinnoN.iloc[-1,0], st_HKinnoN.iloc[-1,1], st_HKinnoN.iloc[-1,3], st_HKinnoN.iloc[-1,2]] # 종가, 변화율, 수익금, 수익금(%)
    #image_HKI = 'https://ssl.pstatic.net/imgfinance/chart/item/candle/day/195940.png'
    image_HKI = 'https://t1.daumcdn.net/finance/chart/kr/candle/d/A195940.png?timestamp={}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    image_link_HKI = 'https://m.stock.naver.com/domestic/stock/195940/total'
    

   
    # --------------------------------
    
    if datetime.datetime.today().weekday() not in [5,6]:
        for st in st_type:
            if st == 'DJI':
                sendToFrdMessageFeed(text_title=text_DJI_Title, text_contents="", frd_name=['김익현',], image_url=image_DJI, image_link_url=image_link_DJI)
            elif st == 'INDEX':
                sendToFrdMessageFeed(text_title=text_INDEX_Title, text_contents=text_INDEX_Contents, frd_name=['김익현',], image_url=image_INDEX, image_link_url=image_link_INDEX)
            elif st == 'HDI':
                sendToFrdMessageFeed_st(text_title=text_HDI_Title, text_contents=text_HDI_Contents, frd_name=['김익현',], image_url=image_HDI, image_link_url=image_link_HDI, price=HDI_price)
            elif st == 'HKI':
                sendToFrdMessageFeed_st(text_title=text_HKI_Title, text_contents=text_HKI_Contents, frd_name=['김익현',], image_url=image_HKI, image_link_url=image_link_HKI, price=HKI_price)
                #sendToFrdMessageFeed(text_title=text_HKI_Title, text_contents="오늘도 수고 많았어~~", frd_name=['이태은',], image_url=image_HKI, image_link_url=image_link_HKI)
        
        
    print('-' * 70)
    
    
    


# ----------------------------------------------------------------------------------
# IPO 현재가 피드 보내기
def get_IPO_st_info(ticker=[], frd_name=[]):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - IPO 주가 정보 전송 -')
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    today = datetime.datetime.today()
    today = today.strftime('%Y%m%d')

    
    
    # -- 기존 DB 불러오기(시간 형태로 변환)
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)  
    
    
    # -- 전일 대비 새로 추가된 종목 찾기
    stock_code_old = set(stock.get_market_ticker_list(date=yesterday, market="ALL"))
    stock_code_new = set(stock.get_market_ticker_list(date=today, market="ALL"))
    
    new_IPO_ticker = list(stock_code_new.difference(stock_code_old))
    
    
    print("stock_code_old: ", len(stock_code_old))
    print("stock_code_new: ", len(stock_code_new))
    print("new_IPO_ticker; ", new_IPO_ticker)

    # -- 신규 상장 종목이 없으면 함수 종료
    if not new_IPO_ticker:
        print("금일({}) 신규 상장 종목이 없습니다.".format(today))
        return
    
    
    # -- 신규 상장 종목 확인
    try_num = 60
    while True:
        print('Try_num: ', 61-try_num)
        new_IPO_name = [stock.get_market_ticker_name(ticker) for ticker in new_IPO_ticker]
        if len(new_IPO_name) == 0:
            time.sleep(60)
            try_num -= 1
        else:
            break
        
        if try_num == 0:
            sendToFrdMessage('상장 종목 보내기 에러 발생',frd_name=['김익현'])
            return



    print("금일({}) 신규 상장 종목\n    : ".format(today),new_IPO_name)

    
    # -- 주가 확인
    new_IPOs_df = pd.DataFrame(columns=["종목명","티커","공모가","시가","고가","저가","종가","거래량","차트","링크"])
    
    for ticker in new_IPO_ticker:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - IPO 주가 -')
        
        new_IPO_df = stock.get_market_ohlcv(yesterday, today, ticker)
        print(new_IPO_df)
        new_IPO_name = stock.get_market_ticker_name(ticker)
        new_IPO_price_s = new_IPO_df.iloc[0,0] #시가
        new_IPO_price_c = new_IPO_df.iloc[0,3] #종가

        if new_IPO_name in ipodb_df.index:
            new_IPO_price_b = ipodb_df.loc[new_IPO_name, "공모가"]
            percent_change_s = round(((new_IPO_price_s/new_IPO_price_b)-1) * 100)
            percent_change_c = round(((new_IPO_price_c/new_IPO_price_b)-1) * 100)
        else:
            new_IPO_price_b = 0
            percent_change_s = "-"
            percent_change_c = "-"


    new_IPO_price= [new_IPO_price_b, new_IPO_price_s, percent_change_s, new_IPO_price_c, percent_change_c]


    # 네이버 차트 연결
    img_url = "https://ssl.pstatic.net/imgfinance/chart/mobile/day/{}_end.png".format(ticker)
    
    # 다음에서 차트 그림 가져오기
    img_url = "https://t1.daumcdn.net/finance/chart/kr/stock/d/A{}.png?timestamp={}".format(ticker, datetime.datetime.now().strftime('%Y%m%d%H%M'))
    image_link_url = "https://m.stock.naver.com/domestic/stock/{}/total".format(ticker)



    text_IPO_Title = new_IPO_name
    text_IPO_Contents = '공모가 : {}원  (시작가{}원)'.format(new_IPO_price_b,new_IPO_price_s)
    text_IPO_Contents = text_IPO_Contents + '\n현재가 : {}원 {}%'.format(new_IPO_price_c, percent_change_c)



    if (datetime.datetime.today().weekday() not in [5,6]) and ("스팩" not in new_IPO_name) and ("리츠" not in new_IPO_name):
        sendToFrdMessageFeed_IPO(text_title=text_IPO_Title, text_contents=text_IPO_Contents, frd_name=['김익현'], image_url=img_url, image_link_url=image_link_url, new_IPO_price=new_IPO_price)
                
            
            
            

# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    refresh_token()
    #get_st_info()
    #get_IPO_st_info(ticker=["042670"], frd_name=["김익현"])
    get_IPO_st_info(frd_name=["김익현"])
    #get_IPO_st_info()