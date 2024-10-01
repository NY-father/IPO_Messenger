import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
from tabulate import tabulate

from kakao_message import *





# --------------------------------------------------------------------------------------------
# -- IPO 주식 DB 업데이트
def getIpoInfo():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
  # -- 기존 DB 불러오기(시간 형태로 변환)
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')


  # -- 네이버 금융에서 IPO정보 크롤링
    response = requests.get("https://finance.naver.com/sise/ipo.naver")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    ipo_sts = soup.select(".item_area")



  # -- 주식 정보 딕셔너리 형태로 저장
    header = ['종목','시장','공모희망가_저','공모희망가_고','공모가','업종','주관사',
                                '개인청약경쟁률','개인청약_시작','개인청약_종료','상장일','진행상태']

    stinfo_dic = {key: [None]*(len(ipo_sts)-1) for key in header}

    for i in range(0,len(ipo_sts)-1):
      # 텍스트만 리스트로 변환
      ipo_st = ipo_sts[i].text.strip().replace("\t","")
      stinfo_raw = ipo_st.split("\n")
      stinfo_raw = list(filter(None, stinfo_raw))

      # print("stinfo_raw:", stinfo_raw,"\n\n")
    
    
       # 시장
      stinfo_dic['시장'][i] = stinfo_raw[0][0:2]
      
       # 종목
      stinfo_dic['종목'][i] = stinfo_raw[0][3:]
      
       # 공모희망가, 공모가
      if '~' in stinfo_raw[stinfo_raw.index('공모가')+1]:
        stinfo_dic['공모희망가_저'][i] = int(stinfo_raw[2].split("~")[0].replace(',',''))
        stinfo_dic['공모희망가_고'][i] = int(stinfo_raw[2].split("~")[1].replace(',',''))
      elif stinfo_raw[stinfo_raw.index('공모가')+1] == '미정':
        stinfo_dic['공모가'][i] = None
      else:
        stinfo_dic['공모가'][i] = int(stinfo_raw[stinfo_raw.index('공모가')+1].replace(',',''))
      
       # 업종
      if '업종' in stinfo_raw:
        stinfo_dic['업종'][i] = stinfo_raw[stinfo_raw.index('업종')+1]
      
       # 주관사
      if '주관사' in stinfo_raw:
        stinfo_dic['주관사'][i] = stinfo_raw[stinfo_raw.index('주관사')+1]
              
       # 개인청약경쟁률
      if '개인청약경쟁률' in stinfo_raw:
        stinfo_dic['개인청약경쟁률'][i] = float(stinfo_raw[stinfo_raw.index('개인청약경쟁률')+1].split(':')[0].replace(',',''))
              
       # 개인청약 기간
      if ('개인청약' in stinfo_raw) and (not stinfo_raw[stinfo_raw.index('개인청약')+1] == '미정'):
        stinfo_dic['개인청약_시작'][i] = '20' + stinfo_raw[stinfo_raw.index('개인청약')+1].split('~')[0]
        stinfo_dic['개인청약_종료'][i] = stinfo_dic['개인청약_시작'][i].split('.')[0] + '.' + stinfo_raw[stinfo_raw.index('개인청약')+1].split('~')[1]
      
       # 상장일
      if not stinfo_raw[stinfo_raw.index('상장일')+1] == '미정':
        stinfo_dic['상장일'][i] = '20' + stinfo_raw[stinfo_raw.index('상장일')+1]
      else:
        stinfo_dic['상장일'][i] = None
      
       # 진행상태
      if '진행상태' in stinfo_raw:
        stinfo_dic['진행상태'][i] = stinfo_raw[stinfo_raw.index('진행상태')+1]
      else:
        stinfo_dic['진행상태'][i] = '공모청약완료'
      

    print(stinfo_dic['종목'])




  # -- 주식 정보 데이터프레임 생성
    stinfo_df = pd.DataFrame(stinfo_dic)
    stinfo_df.set_index('종목', inplace = True)

    stinfo_df['개인청약_시작'] = pd.to_datetime(stinfo_df['개인청약_시작'],format='%Y.%m.%d')
    stinfo_df['개인청약_종료'] = pd.to_datetime(stinfo_df['개인청약_종료'],format='%Y.%m.%d')
    stinfo_df['상장일'] = pd.to_datetime(stinfo_df['상장일'],format='%Y.%m.%d')
    
    
    stinfo_df['개인청약경쟁률'].fillna(value=np.nan, inplace=True)
    




  # -- 기존 DB 업데이트
  
    text = '- IPO 정보 업데이트 -'


    # -- 신규 종목 추가
    add_sts = list(set(stinfo_df.index) - set(ipodb_df.index))
    for ind in add_sts:
      ipodb_df = ipodb_df.append(stinfo_df.loc[[ind]])

    
    # -- 변경값 수정
    mod_sts = []
    for ind in stinfo_df.index:
      for col in stinfo_df.columns:
        if not ((str(stinfo_df.loc[ind,col]) =='nan') or (str(stinfo_df.loc[ind,col]) =='NaT')):
          if not stinfo_df.loc[ind,col] == ipodb_df.loc[ind,col]:
            mod_sts.append('{}({})'.format(ind,col))
            ipodb_df.loc[ind,col] = stinfo_df.loc[ind,col]
    


    # -- 종목 삭제
    drop_sts = list(set(ipodb_df.index) - set(stinfo_df.index))
    if len(drop_sts) != 0:
        ipodb_df = ipodb_df.drop(drop_sts)
        
    
    
    # -- Send message
    text = text + ("\n추가 : " + ",".join(add_sts)) + ("\n삭제 : " + ",".join(drop_sts)) + ("\n수정 : " + ",".join(mod_sts))
    if len(text) == 33:
        print(text.split('\n')[0])
    else:
        print(text)
        #sendToFrdMessage(text, frd_name=['김익현'])



  # -- DB 저장
    ipodb_df.to_csv("IPO공모주_DB_new.csv", mode='w', encoding='utf-8-sig')
    
    
  # -- end line
    print('-' * 70)





# --------------------------------------------------------------------------------------------
# -- Show IPO DB
def showIPO_DB():
    ipodb_df = pd.read_csv("IPO공모주_DB_new.csv")
    ipodb_df.set_index('종목', inplace = True)

    ipodb_df['개인청약_시작'] = pd.to_datetime(ipodb_df['개인청약_시작'],format='%Y-%m-%d')
    ipodb_df['개인청약_종료'] = pd.to_datetime(ipodb_df['개인청약_종료'],format='%Y-%m-%d')
    ipodb_df['상장일'] = pd.to_datetime(ipodb_df['상장일'],format='%Y-%m-%d')

    ipodb_df.sort_values(by=['개인청약_시작'], axis=0, inplace=True)
    print(tabulate(ipodb_df.iloc[0:10,[0,3,5,7,9,6]], headers = 'keys', tablefmt = 'psql'))

  # -- end line
    print('-' * 70)


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    from kakao_message import *
    #refresh_token()
    getIpoInfo()
    
    

