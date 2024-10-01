import schedule

from kakao_message import *
from send_IPO_schedule import *
from update_IPO_db_v1 import *
from get_stock_info import *

import time
import traceback
# --------------------------------------------------------------------------------------------
# -- Inintial job

refresh_token()


#get_st_info(st_type = ['DJI','INDEX'])
#get_st_info(st_type = ['INDEX','HDI', 'HKI'])
get_st_info(st_type = ['HKI'])
#getIpoInfo() # IPO 정보 업데이트


#get_IPO_st_info(frd_name=["김익현"]) # IPO 현재가 전송


#sendMsgLaunch(frd_name=["김익현"]) # 상장일정 전송
#sendMsgSubs(frd_name=["김익현"]) # 청약일정 전송


sendMsgLaunchWeek() # 상장일정 요약 전송
sendMsgSubsWeek() # 청약일정 요약 전송




# --------------------------------------------------------------------------------------------
# -- job schedule
schedule.every(5).hours.do(refresh_token)
schedule.every().day.at("17:00").do(getIpoInfo)


schedule.every().day.at("07:30").do(sendMsgLaunch)
schedule.every().day.at("07:30").do(sendMsgSubs)

schedule.every().day.at("08:55").do(sendMsgLaunch)
#schedule.every().day.at("09:01").do(get_IPO_st_info)
#schedule.every().day.at("12:00").do(get_IPO_st_info)


#schedule.every().day.at("18:30").do(sendMsgLaunch)
#schedule.every().day.at("18:30").do(sendMsgSubs)

schedule.every().saturday.at("10:00").do(sendMsgLaunchWeek)
schedule.every().saturday.at("10:00").do(sendMsgSubsWeek)

#schedule.every().day.at("07:00").do(get_st_info, st_type = ['DJI','INDEX'])
#schedule.every().day.at("09:05").do(get_st_info, st_type = ['INDEX','HDI', 'HKI'])
#schedule.every().day.at("10:00").do(get_st_info, st_type = ['INDEX','HDI', 'HKI'])
#schedule.every().day.at("16:00").do(get_st_info, st_type = ['DJI','INDEX','HDI', 'HKI'])


while True:
    schedule.run_pending()