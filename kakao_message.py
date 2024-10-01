import requests
import datetime
import json

# --------------------------------------------------------------------------------------------
# -- 카카오

from kakao_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

token_file_name = 'kakao_code_KIH'


# --------------------------------------------------------------------------------------------
# -- 코드 발급
def get_code():
    """ KOE322 발생 시 코드 재발행 방법
인터넷 브라우저 주초창에 아래 주소 입력 후 발급 받은 코드 복사하여 입력
https://kauth.kakao.com/oauth/authorize?client_id=f0bc5c2b3b6a3a65062d5aed132afa5c&response_type=code&redirect_uri=http://localhost:5000/oauth
"""
    url = "https://kauth.kakao.com/oauth/token"
    code = input("code: ")


    data = {
        "grant_type"   : "authorization_code",
        "client_id"    : "f0bc5c2b3b6a3a65062d5aed132afa5c",
        "redirect_url" : "http://localhost:5000/oauth",
        "code"         : code
    }
    
    response = requests.post(url, data=data)
    tokens = response.json()
    
    print(tokens)
    with open("{}.json".format(token_file_name), "w") as fp:
        json.dump(tokens, fp)

# --------------------------------------------------------------------------------------------
# -- 토큰 발행
def refresh_token():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'\n - kakao 토큰 재발행 -')
    # -- token 정보 불러오기
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens_ori = json.load(fp)

    url_token = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type" : "refresh_token",
        "client_id" : CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token" : tokens_ori['refresh_token']
    }

    response_token = requests.post(url_token, data=data)
    tokens_new = response_token.json()

    print(tokens_new)
    if 'access_token' in tokens_new.keys():
        
        for key in tokens_new.keys():
            tokens_ori[key] = tokens_new[key]


        # -- 토큰 저장
        # kakao_code.json 파일 저장
        with open("{}.json".format(token_file_name), "w") as fp:
            json.dump(tokens_ori, fp)
        
        text = '토큰을 재발행 성공\n' + tokens_new['access_token']
        print('    토큰을 재발행 성공')
        
    else:
        text = '토큰 재발행 오류\n' + tokens_new['access_token']
        print(text)
        sendToFrdMessage(text, frd_name=['김익현'])
    
    print('-' * 70)
    


# --------------------------------------------------------------------------------------------
# -- Friends에게 메세지 보내기
def showFriendsList():
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)
    
    headers = {"Authorization": "Bearer "+tokens['access_token']}


# -- Get friends list
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    
    result = json.loads(requests.get(url, headers=headers).text)
    friends_list = result.get("elements")
    
    print(friends_list)
    friend_name = []
    for friend in friends_list:
        friend_name.append(friend['profile_nickname'])
        
    print('회원 리스트 :', friend_name)
    
    
    




# --------------------------------------------------------------------------------------------
# -- 나에게 메세지 보내기
def sendToMeMessage(text):
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)

    headers = {"Authorization": "Bearer "+tokens['access_token']}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {"web_url": "http://m.38.co.kr/ipo/fund.php",
                 "mobile_web_url": "http://m.38.co.kr/ipo/fund.php"},
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}

    response = requests.post(url, headers=headers, data=data)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


# --------------------------------------------------------------------------------------------
# -- Friends에게 메세지 보내기
def sendToFrdMessage(text,frd_name=[]):
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)
    
    headers = {"Authorization": "Bearer "+tokens['access_token']}


# -- Get friends list
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    
    result = json.loads(requests.get(url, headers=headers).text)
    friends_list = result.get("elements")


# -- Send message
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #friend에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {"web_url": "http://m.38.co.kr/ipo/fund.php",
                 "mobile_web_url": "http://m.38.co.kr/ipo/fund.php"},
        "button_title": "바로 확인"
        }


    for friend in friends_list:
                
        if (len(frd_name) != 0) and (not (friend['profile_nickname'] in frd_name)):
            continue
                
                        
        data = {
            'receiver_uuids': '["{}"]'.format(friend.get('uuid')),
            "template_object": json.dumps(post)
            }

        response = requests.post(url, headers=headers, data=data)
        if response.json().get('successful_receiver_uuids'):
            print('메시지를 성공적으로 보냈습니다. : {}'.format(friend.get('profile_nickname')))
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))



# --------------------------------------------------------------------------------------------
# -- Friends에게 피드 보내기
def sendToFrdMessageFeed(text_title,text_contents,image_url,image_link_url,frd_name=[]):
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)
    
    headers = {"Authorization": "Bearer "+tokens['access_token']}


# -- Get friends list
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    
    result = json.loads(requests.get(url, headers=headers).text)
    friends_list = result.get("elements")


# -- Send message
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #friend에게 보내기 주소

    post = {
        "object_type": "feed",
        "content": {
            "title" : text_title,
            "image_url" : image_url,
            "image_width": 996, #700,
            "image_height": 519, #289,
            "description" : text_contents,
            "link" : {
                "mobile_web_url" : image_link_url
                }
            }
        }



    for friend in friends_list:
                
        if (len(frd_name) != 0) and (not (friend['profile_nickname'] in frd_name)):
            continue
                
                        
        data = {
            'receiver_uuids': '["{}"]'.format(friend.get('uuid')),
            "template_object": json.dumps(post)
            }

        response = requests.post(url, headers=headers, data=data)
        if response.json().get('successful_receiver_uuids'):
            print('메시지를 성공적으로 보냈습니다. : {}'.format(friend.get('profile_nickname')))
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


#------------------------------------------------------------------------
# -- Friends에게 피드 보내기
def sendToFrdMessageFeed_IPO(text_title,text_contents,image_url,image_link_url,new_IPO_price,frd_name=[]):
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)
    
    headers = {"Authorization": "Bearer "+tokens['access_token']}


# -- Get friends list
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    
    result = json.loads(requests.get(url, headers=headers).text)
    friends_list = result.get("elements")


# -- Send message
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #friend에게 보내기 주소
    
    post = {
        "object_type": "feed",
        "item_content": {
            "profile_text" : text_title,
            "items" : [{"item": "공모가", "item_op": "{:,}원".format(int(new_IPO_price[0]))},
                       {"item": "시초가", "item_op": "{:,}원".format(new_IPO_price[1])},
                       #{"item": "시초가(%)", "item_op": "{:0.1f}%".format(int(new_IPO_price[2]))},
                       {"item": "현재가", "item_op": "{:,}원".format(int(new_IPO_price[3]))},
                       #{"item": "현재가(%)", "item_op": "{:0.1f}%".format(int(new_IPO_price[4]))}
                       ]
            },
        "content": {
            "title" : datetime.datetime.now().strftime('%Y년 %m월 %d일(%a)   %H시 %M분'),
            "image_url" : image_url,
            "image_width": 996, #700,
            "image_height": 519, #289,
            #"description" : text_contents,
            "link" : {
                "mobile_web_url" : image_link_url
                }
            }
        }
    


    for friend in friends_list:
                
        if (len(frd_name) != 0) and (not (friend['profile_nickname'] in frd_name)):
            continue
                
                        
        data = {
            'receiver_uuids': '["{}"]'.format(friend.get('uuid')),
            "template_object": json.dumps(post)
            }

        response = requests.post(url, headers=headers, data=data)
        if response.json().get('successful_receiver_uuids'):
            print('메시지를 성공적으로 보냈습니다. : {}'.format(friend.get('profile_nickname')))
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))



#------------------------------------------------------------------------
# -- Friends에게 피드 보내기
def sendToFrdMessageFeed_st(text_title,text_contents,image_url,image_link_url,price,frd_name=[]):
    with open("{}.json".format(token_file_name), "r") as fp:
        tokens = json.load(fp)
    
    headers = {"Authorization": "Bearer "+tokens['access_token']}


# -- Get friends list
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    
    result = json.loads(requests.get(url, headers=headers).text)
    friends_list = result.get("elements")


# -- Send message
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #friend에게 보내기 주소

    post = {
        "object_type": "feed",
        "item_content": {
            "profile_text" : "금일 종가 : " + text_title,
            "items" : [{"item": "종가", "item_op": "{:,}원".format(price[0])},
                       {"item": "종가(%)", "item_op": "{:0.1f}%".format(price[1])},
                       {"item": "수익금", "item_op": "{:0.1f}원".format(price[2])},
                       {"item": "수익률(%)", "item_op": "{:0.1f}%".format(price[3])}]
            },
        "content": {
            #"title" : datetime.datetime.now().strftime('%Y년 %m월 %d일(%a)'),
            "title"  : text_title + ": {:,}원({:0.1f}%)".format(price[0],price[1]),
            "image_url" : image_url,
            "image_width": 996, #700,
            "image_height": 519, #289,
            #"description" : text_contents,
            "link" : {
                "mobile_web_url" : image_link_url
                }
            }
        }
    


    for friend in friends_list:
                
        if (len(frd_name) != 0) and (not (friend['profile_nickname'] in frd_name)):
            continue
                
                        
        data = {
            'receiver_uuids': '["{}"]'.format(friend.get('uuid')),
            "template_object": json.dumps(post)
            }

        response = requests.post(url, headers=headers, data=data)
        if response.json().get('successful_receiver_uuids'):
            print('메시지를 성공적으로 보냈습니다. : {}'.format(friend.get('profile_nickname')))
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))




if __name__ == '__main__':
    #get_code()
    refresh_token()
    #showFriendsList()