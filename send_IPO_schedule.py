import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np
import json
import time
import schedule


from kakao_message import *





# end line
text_endline = '-' * 70

# --------------------------------------------------------------------------------------------
# -- 상장일
def sendMsgLaunch():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 상장주식 메시지 전송 -')
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')


    # 
    if datetime.datetime.now().time() < datetime.time(15,30,00):
        # -- 
        text = '오늘 상장({})'.format(datetime.datetime.today().strftime('%Y.%m.%d'))
    else:
        # --
        text = '내일 상장({})'.format((datetime.datetime.today()+datetime.timedelta(hours=24)).strftime('%Y.%m.%d'))
    

    for st in ipodb_df.index:
      if pd.isnull(ipodb_df.loc[st,'상장일']):
        continue
    
      if datetime.datetime.today() > ipodb_df.loc[st,'상장일']-datetime.timedelta(hours=8) and datetime.datetime.today() < ipodb_df.loc[st,'상장일']+datetime.timedelta(hours=16):
        text = text + '\n-{} | {}원 | {} | {}:1'.format(st,int(ipodb_df.loc[st,'공모가']),ipodb_df.loc[st,'주관사'],ipodb_df.loc[st,'개인청약경쟁률'])
        
        
        
    if len(text.split('\n')) > 1:
        print(text)
        #sendToFrdMessage(text)
        sendToFrdMessage(text, frd_name=['김익현'])
    
    print(text_endline)

# --------------------------------------------------------------------------------------------
# -- 개인청약

def sendMsgSubs():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 청약 주식 메시지 전송 -')
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')
    
    ipodb_df.sort_values(by='개인청약_시작',inplace=True)


    # 
    if datetime.datetime.now().time() < datetime.time(15,30,00):
        # -- 
        text = '오늘 청약({})'.format(datetime.datetime.today().strftime('%Y.%m.%d'))
    else:
        # --
        text = '내일 청약({})'.format((datetime.datetime.today()+datetime.timedelta(hours=24)).strftime('%Y.%m.%d'))
    

    for st in ipodb_df.index:
      if pd.isnull(ipodb_df.loc[st,'개인청약_시작']):
        continue
      elif datetime.datetime.today()>ipodb_df.loc[st,'개인청약_시작']-datetime.timedelta(hours=8) and datetime.datetime.today()<ipodb_df.loc[st,'개인청약_종료']+datetime.timedelta(hours=16):
        if np.isnan(ipodb_df.loc[st,'공모가']):
            text = text + '\n-{} | {}원 | {} ({}~{})'.format(st,'nan',ipodb_df.loc[st,'주관사'],ipodb_df.loc[st,'개인청약_시작'].strftime('%m.%d'),ipodb_df.loc[st,'개인청약_종료'].strftime('%m.%d'))
        else:
            text = text + '\n-{} | {}원 | {} ({}~{})'.format(st,int(ipodb_df.loc[st,'공모가']),ipodb_df.loc[st,'주관사'],ipodb_df.loc[st,'개인청약_시작'].strftime('%m.%d'),ipodb_df.loc[st,'개인청약_종료'].strftime('%m.%d'))

    if len(text.split('\n')) > 1:
        print(text)
        #sendToFrdMessage(text)
        sendToFrdMessage(text, frd_name=['김익현'])
        
    print(text_endline)




# --------------------------------------------------------------------------------------------
# -- 상장일
def sendMsgLaunchWeek():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 상장주식 메시지 전송 -')
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')
    
    ipodb_df.sort_values(by='상장일',inplace=True)


    text = '다음 상장 일정'
    
    
    ipodb_df.sort_values(by='상장일', inplace=True)

    for st in ipodb_df.index:
      if pd.isnull(ipodb_df.loc[st,'상장일']):
        continue
    
      if datetime.datetime.today() < ipodb_df.loc[st,'상장일'] and datetime.datetime.today()+datetime.timedelta(days=7) > ipodb_df.loc[st,'상장일']:
        text = text + '\n-{} | {} ({})'.format(st,ipodb_df.loc[st,'주관사'],ipodb_df.loc[st,'상장일'].strftime('%m.%d %a'))
    
        
        
    if len(text.split('\n')) > 1:
        pass
        print(text)
        #sendToFrdMessage(text)
        sendToFrdMessage(text, frd_name=['김익현'])
        

    
    print(text_endline)

# --------------------------------------------------------------------------------------------
# -- 개인청약

def sendMsgSubsWeek():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - 청약 주식 메시지 전송 -')
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')


    text = '다음 청약 일정'
    

    ipodb_df.sort_values(by='개인청약_시작', inplace=True)
    
    for st in ipodb_df.index:
      if pd.isnull(ipodb_df.loc[st,'개인청약_시작']):
        continue
      elif datetime.datetime.today()<ipodb_df.loc[st,'개인청약_시작'] and datetime.datetime.today()+datetime.timedelta(days=7)>ipodb_df.loc[st,'개인청약_종료']:
        stock_firm = ipodb_df.loc[st,'주관사']
        date  = ipodb_df.loc[st,'개인청약_시작'].strftime('%m.%d %a')
        text = text + '\n-{} | {} ({})'.format(st, stock_firm, date)
    
    
    if len(text.split('\n')) > 1:
        print(text)
        #sendToFrdMessage(text)
        sendToFrdMessage(text, frd_name=['김익현'])
    
    print(text_endline)




# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    refresh_token()
    sendMsgSubsWeek()
    sendMsgLaunchWeek()
