#Line Bot 聊天機器人 網際網路掛勾WebHook callback服務
#處理加入好友 或者文字聊天或者圖片聊天
from IoTService import app #引用Flask物件 公用變數
#引用flask模組代表一個前端的請求資訊request local proxy
from flask import request,make_response #具有與前端一個獨立的交談層session
from IoTService.DBUtility import createConnection,query,update,querymuti
from IoTService.LineUtility import replyMessage,readImage,sendPushTextMessage,CityandType
#Http Client
import requests
import json
import os
import time
import datetime
#send repy message api服務位址

replyURL='https://api.line.me/v2/bot/message/reply'
#token=' '#Bearer
userProfileURL='https://api.line.me/v2/bot/profile/'

#-----------------------OPEN AI API--------------------------
#openaiKey=''#Bearer 
openaiURL='https://api.openai.com/v1/chat/completions'

# 使用者查詢狀態
stateSqlQ = 'SELECT isActive FROM LinerUser WHERE UserID = %s'
stateSqlU = "UPDATE LinerUser SET isActive = %s WHERE UserID = %s"

#Custom Vision ai 端點
customAIURL=''
#Custom Vision key
priductionKey=''


#定義Line Bot回呼callback 端點
@app.route("/api/v1/linebot/hook",methods=['POST'])
def lineBotProcess():
    #dict
    hookData=request.get_json() #將json字串反序列化成dict or list物件
    print(type(hookData))
    #取出訊息的第一筆(可以多則訊息)
    data=hookData['events'][0]
    
    curUser=data['source'] #dict物件
    #取出Line系統id(user id)
    #判斷是否為個人使用者
    userId=''
    if curUser["type"]=="user":
       #個人 取出user id
       userId=curUser['userId']
    #判斷其中的type屬性
    print(f'Line使用者 user id:{userId}')
    if data["type"]=="follow": #加入好友 或者解鎖
        #取得前端加入好友產生回覆令牌Token 用在send reply message上銜接點
        replyToken=data['replyToken']
        print(replyToken)
        #新增好友
        print(f'User Id:{userId} 已經加入好友了')
        #獲取使用user get profile api(取得使用者更詳細的資訊)
        profileURL=userProfileURL+userId
        proHeader={"Authorization":token}
        #回應一個Response物件
        resp=requests.get(profileURL,headers=proHeader) #呼喚取得使用者完整資訊api
        #讀回資料
        profile=resp.json() #取回dict or list
        #取使用者名稱與圖片
        name=profile['displayName']
        try:
             image=profile['pictureUrl']
        except Exception as ex:
             image = 'None'
        lang=profile['language']
        print(f'{name}/{image}/{lang}')
        #寫到資料庫去
        #呼叫資料庫模組 要一個連接物件(具有開啟連接)
        try:
            connection=createConnection()
            print(type(connection))
            #呼叫查詢(第一次加入-新增記錄 或者解鎖-修改記錄)
            result=query(connection,'select UserID from LinerUsers Where UserID=%s',(userId))
            print(result)
            #None 新增/修改 解鎖欄位isActive
            if result==None:
                #加入好友
                print('新增')
                sql='Insert Into LinerUsers(UserID,DisplayName,Language,PictureURL,isActive) values(%s,%s,%s,%s,%s)'
                #呼叫更新資料模組
                try:
                    update(connection,sql,(userId,name,lang,image,True))
                except Exception as ex:
                    print(ex)    
            else:
                #解鎖 修改資料isActive為1
                print('解鎖') #進行修改
                sql='update LinerUsers set isActive=%s where UserID=%s'
                #呼叫更新資料模組
                try:
                    update(connection,sql,(True,userId))
                except Exception as ex:
                    print(ex)  
                    

            #關閉連接
            connection.close()
        except Exception as ex:
            print('資料連接有問題')    
        print(lang)
        #歡迎詞
        msg=f'{name} 您好\n歡迎你加入漫遊南臺灣\n請依照下列選單\n選擇您想去的縣市\n或是讓我們幫您規劃旅遊行程'
        #回應一個Response狀態碼 帶200 給Line Message api
        response=make_response("",204) #http status code-204 OK 沒有回內容
        #send reply message已讀已回
        #準備資料 送給Line使用者資料
        data={"replyToken":replyToken,
         "messages":[
            {
                "type":"text",
                "text":msg
            }

           ]
        }
        #序列dict物件成json String
        jsonData=json.dumps(data)
        #標頭
        myHeaders={"Content-Type":"application/json","Authorization":token}
        #採用Http Request post送出去
        requests.post(replyURL,data=jsonData,headers=myHeaders)
        #封鎖作業    
    elif data['type']=='unfollow':
        connection=createConnection()
        print(type(connection))
        #進行封鎖 進行修改資料isActive false
        sql='update LinerUsers set isActive=%s where UserID=%s'
        #呼叫更新資料模組
        try:
                update(connection,sql,(False,userId))
        except Exception as ex:
                print(ex) 
        #聊天訊息處理            
    elif data['type']=='message':
         replyToken=data['replyToken']
         #取出聊天訊息額外的屬性message
         message=data['message']
         #判斷聊天內容類型
         if message['type']=='text':
              #取出聊天文字
              content=message['text']
              print('聊天訊息:'+content)
              #TODO文字聊天 借助NLP ai or chatGPT解析
              #先當鸚鵡 回應訊息到使用者端去
              #replyMessage(replyToken,f'鸚鵡說:{content}')  
              if content == "規劃行程":
                   CityandType(replyToken)
              if content == "查詢嘉義景點":
                try:
                      city = "嘉義"

                      conn = createConnection()
                      
                      sql = 'SELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE City = %s'
                      

                      AttractionsInf = querymuti(conn, sql, (city))
                      print(AttractionsInf)
                        
                      #msg=f'景點:{AttractionsInf[0]}\n地址:\n{AttractionsInf[1]}\n營業時間:{AttractionsInf[2]}\n電話:\n{AttractionsInf[3]}\n票價:{AttractionsInf[4]}\n網址:{AttractionsInf[5]}'
                      msg = ''
                      for Len in range(0,len(AttractionsInf)):
                            msg += f'景點:{AttractionsInf[Len][0]}\n地址:{AttractionsInf[Len][1]}\n營業時間:\n{AttractionsInf[Len][2]}\n電話:{AttractionsInf[Len][3]}\n票價:\n{AttractionsInf[Len][4]}\n官網:{AttractionsInf[Len][5]}'
                            msg += '\n---------------------\n'
                      replyMessage(replyToken,f'嘉義景點資訊\n---------------------\n{msg}')
                      
                      replyMessage(replyToken,f'{city}景點資訊\n---------------------\n{msg}') 

                      
                      conn.close()
                except Exception as ex:
                        replyMessage(replyToken,f'資料庫查無此景點!!') 

                try:
                     
                     conn = createConnection()
                     history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                     update(conn,history_sql,(userId,content))
                     conn.close()
                
                except Exception as ex:
                     print("無法插入資料")     
              elif content == "查詢臺南景點":
                try:
                      city = "臺南"
                      conn = createConnection()
                      
                      sql = 'SELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE City = %s'
                      AttractionsInf = querymuti(conn, sql, (city))
                      print(AttractionsInf)
                        
                      #msg=f'景點:{AttractionsInf[0]}\n地址:\n{AttractionsInf[1]}\n營業時間:{AttractionsInf[2]}\n電話:\n{AttractionsInf[3]}\n票價:{AttractionsInf[4]}\n網址:{AttractionsInf[5]}'
                      msg = ''
                      for Len in range(0,len(AttractionsInf)):
                            msg += f'景點:{AttractionsInf[Len][0]}\n地址:{AttractionsInf[Len][1]}\n營業時間:\n{AttractionsInf[Len][2]}\n電話:{AttractionsInf[Len][3]}\n票價:\n{AttractionsInf[Len][4]}\n官網:{AttractionsInf[Len][5]}'
                            msg += '\n---------------------\n'
                      replyMessage(replyToken,f'臺南景點資訊\n---------------------\n{msg}')
                      
                      replyMessage(replyToken,f'{city}景點資訊\n---------------------\n{msg}') 
                      conn.close()
                except Exception as ex:
                        replyMessage(replyToken,f'資料庫查無此景點!!') 
                try:
                     
                     conn = createConnection()
                     history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                     update(conn,history_sql,(userId,content))
                     conn.close()
                
                except Exception as ex:
                     print("無法插入資料")                     
              elif content == "查詢高雄景點":
                try:
                      city = "高雄"
                      conn = createConnection()
                      
                      sql = 'SELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE City = %s'
                      AttractionsInf = querymuti(conn, sql, (city))
                      print(AttractionsInf)
                        
                      #msg=f'景點:{AttractionsInf[0]}\n地址:\n{AttractionsInf[1]}\n營業時間:{AttractionsInf[2]}\n電話:\n{AttractionsInf[3]}\n票價:{AttractionsInf[4]}\n網址:{AttractionsInf[5]}'
                      msg = ''
                      for Len in range(0,len(AttractionsInf)):
                            msg += f'景點:{AttractionsInf[Len][0]}\n地址:{AttractionsInf[Len][1]}\n營業時間:\n{AttractionsInf[Len][2]}\n電話:{AttractionsInf[Len][3]}\n票價:\n{AttractionsInf[Len][4]}\n官網:{AttractionsInf[Len][5]}'
                            msg += '\n---------------------\n'
                      replyMessage(replyToken,f'高雄景點資訊\n---------------------\n{msg}')
                      
                      replyMessage(replyToken,f'{city}景點資訊\n---------------------\n{msg}') 
                      conn.close()
                    
                except Exception as ex:
                        replyMessage(replyToken,f'資料庫查無此景點!!') 
                try:
                     
                     conn = createConnection()
                     history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                     update(conn,history_sql,(userId,content))
                     conn.close()
                
                except Exception as ex:
                     print("無法插入資料")                              
              elif content == "查詢屏東景點":
                try:
                      city = "屏東"
                      conn = createConnection()
                      
                      sql = 'SELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE City = %s'
                      AttractionsInf = querymuti(conn, sql, (city))
                      print(AttractionsInf)
                        
                      #msg=f'景點:{AttractionsInf[0]}\n地址:\n{AttractionsInf[1]}\n營業時間:{AttractionsInf[2]}\n電話:\n{AttractionsInf[3]}\n票價:{AttractionsInf[4]}\n網址:{AttractionsInf[5]}'
                      msg = ''
                      for Len in range(0,len(AttractionsInf)):
                            msg += f'景點:{AttractionsInf[Len][0]}\n地址:{AttractionsInf[Len][1]}\n營業時間:\n{AttractionsInf[Len][2]}\n電話:{AttractionsInf[Len][3]}\n票價:\n{AttractionsInf[Len][4]}\n官網:{AttractionsInf[Len][5]}'
                            msg += '\n---------------------\n'
                      replyMessage(replyToken,f'屏東景點資訊\n---------------------\n{msg}')
                      
                      replyMessage(replyToken,f'{city}景點資訊\n---------------------\n{msg}') 
                      conn.close()
                except Exception as ex:
                        replyMessage(replyToken,f'資料庫查無此景點!!') 
                try:
                     
                     conn = createConnection()
                     history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                     update(conn,history_sql,(userId,content))
                     conn.close()
                
                except Exception as ex:
                     print("無法插入資料")                             
              elif content == "嘉義:戶外類型":                   
                   city = '嘉義'
                   travel_tpye = '戶外類型'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  

              elif content == "嘉義:室內場所":                   
                   city = '嘉義'
                   travel_tpye = '室內場所'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}') 
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "嘉義:文藝氣息":                   
                   city = '嘉義'
                   travel_tpye = '文藝氣息'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}') 
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "臺南:戶外類型":                   
                   city = '臺南'
                   travel_tpye = '戶外類型'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "臺南:室內場所":                   
                   city = '臺南'
                   travel_tpye = '室內場所'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "臺南:文藝氣息":                   
                   city = '臺南'
                   travel_tpye = '文藝氣息'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')    
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")                                                   
              elif content == "高雄:戶外類型":
                   city = '高雄'
                   travel_tpye = '戶外類型'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')  
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")     
              elif content == "高雄:室內場所":
                   city = '高雄'
                   travel_tpye = '室內場所'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}') 
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "高雄:文藝氣息":
                   city = '高雄'
                   travel_tpye = '文藝氣息'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')         
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")                                                   
              elif content == "屏東:戶外類型":
                   city = '屏東'
                   travel_tpye = '戶外類型'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')      
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")                          
              elif content == "屏東:室內場所":
                   city = '屏東'
                   travel_tpye = '室內場所'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')  
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")  
              elif content == "屏東:文藝氣息":
                   city = '屏東'
                   travel_tpye = '文藝氣息'
                   openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
                   #設定傳送上去的資料json
                   openaiSourceData='您是旅遊規劃專家，請幫我規畫行程，地點在'+ city +'旅遊類型為'+travel_tpye+'請用繁體中文回覆'
                   openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}
                   #正式提出請求
                   openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
                   #print(openaiResponse.json())
                   #Openai api語意回應的結果 取出內容
                   aiData=openaiResponse.json()
                   content=aiData['choices'][0]['message']['content']
                   print(content)
                   #反序列化字串為物件dict 
                   replyMessage(replyToken,f'{content}')         
                   Itinerary = '旅遊規劃紀錄:地點為'+ city + '類型為' +travel_tpye
                   try:
                     
                     conn = createConnection()
                     Itinerary_sql = 'Insert Into ItineraryRecord(UserID,UserRecord,ContentRecord) values(%s,%s,%s)'
                     update(conn,Itinerary_sql,(userId,Itinerary,content))
                     conn.close()
                
                   except Exception as ex:
                     print("無法插入資料")                                     
              elif content == '查詢景點歷史紀錄':
                try:
                    conn = createConnection()
                   
                    sql = 'Select UserRecord, CONVERT(varchar,CreateDate,120) as date from HistoryRecord Where UserID =  %s\n'
                    UserRecord = querymuti(conn, sql, (userId))
                    print(UserRecord)
                    if UserRecord == []:
                        replyMessage(replyToken,f'該用戶無歷史紀錄') 
                    else:
                        msg = ''
                        for Len in range(0,len(UserRecord)):
                            msg += f'歷史紀錄:{UserRecord[Len][0]}\n查詢時間:{UserRecord[Len][1]}'
                            msg += '\n---------------------\n'
                        replyMessage(replyToken,f'使用者歷史紀錄\n---------------------\n{msg}')
                    conn.close()
                except Exception as ex:
                    replyMessage(replyToken,f'該用戶無歷史紀錄')  
              
              elif content == '查詢旅遊規劃歷史紀錄':
                try:
                    conn = createConnection()
                   
                    sql = 'Select UserRecord, ContentRecord ,CONVERT(varchar,CreateDate,120) as date from ItineraryRecord Where UserID =  %s\n'
                    UserRecord = querymuti(conn, sql, (userId))
                    print(UserRecord)
                    if UserRecord == []:
                        replyMessage(replyToken,f'該用戶無歷史紀錄') 
                    else:
                        msg = ''
                        for Len in range(0,len(UserRecord)):
                            msg += f'{UserRecord[Len][0]}\n\n行程規劃內容:\n{UserRecord[Len][1]}\n\n查詢時間:{UserRecord[Len][2]}'
                            msg += '\n--------------------------------\n'
                        replyMessage(replyToken,f'使用者旅遊規劃歷史紀錄\n--------------------------------\n{msg}')
                    conn.close()
                except Exception as ex:
                    replyMessage(replyToken,f'該用戶無歷史紀錄')  
              
              elif content == '刪除歷史紀錄':
                try:
                     conn = createConnection()
                     history_sql = 'DELETE From HistoryRecord Where UserID  = %s'
                     update(conn,history_sql,(userId))
                     replyMessage(replyToken,f'歷史紀錄已刪除')
                     conn.close()
                     conn = createConnection()
                     history_sql = 'DELETE From ItineraryRecord Where UserID  = %s'
                     update(conn,history_sql,(userId))
                     replyMessage(replyToken,f'歷史紀錄已刪除')
                     conn.close()
                except Exception as ex:
                    replyMessage(replyToken,f'該用戶無歷史紀錄')
              else:
                try:
                    conn = createConnection()
                    sql = "declare @content nvarchar(100)\nset @content = %s\nSELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE Attactions LIKE '%' + @content + '%'"
                    AttractionInf = querymuti(conn, sql, (content)) 
                    if AttractionInf == []:
                        replyMessage(replyToken,f'該景點不在南部或不存在') 
                    else:
                        print(AttractionInf)
                        msg = ''
                        for Len in range(0,len(AttractionInf)):
                                msg += f'景點:{AttractionInf[Len][0]}\n地址:{AttractionInf[Len][1]}\n營業時間:\n{AttractionInf[Len][2]}\n電話:{AttractionInf[Len][3]}\n票價:\n{AttractionInf[Len][4]}\n官網:{AttractionInf[Len][5]}'
                                msg += '\n---------------------\n'
                        replyMessage(replyToken,f'景點資訊\n----------------------\n{msg}')
                        conn.close()
                        conn = createConnection()
                        history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                        update(conn,history_sql,(userId,content))
                        conn.close()
    
                except Exception as ex:
                    replyMessage(replyToken,f'該景點不在南部或不存在')  
            #--------------------Image 配合Custom Vision AI進行影像推測----------------------------------------------    
         elif message['type']=='image':
              replyToken=data['replyToken']
              #處理圖片
              #取出圖片id
              imageId=message['id']
              print(type(imageId))
              #借助getFile api結合這一個id圖取圖片檔
              byte=readImage(imageId)
              #呼喚AI Custom Vision(上傳圖片bytes 進行分析)
              #將byte物件內容 轉換成byte array
              buffer=bytearray(byte)
              #------------------Custom Vision AI 推測-----------------------------------
              #print(buffer)  
              #呼喚Custom Vision AI 採用傳送圖片方式進行解析
              #定義Http Header Content-Type and prediction-key
              aiHeader={"Content-Type":"application/octet-stream","Prediction-Key":priductionKey}
              aiResponse=requests.post(customAIURL,data=buffer,headers=aiHeader)
              preData=aiResponse.json() #dict
              #print(aiResponse.json())
              #處理推測資料 取出最高分 推測tagName
              predictions=preData['predictions'] #list
              #lambda expression 採用 走訪 逐一傳遞進來dict 進行sort key設定
              #排序方式預設生冪 透過sorted()第三個參數採用反向 變成降冪排序
              sortPred=sorted(predictions,key=lambda p:p['probability'], reverse = True)
              #print(sortPred)  
              #取出第一筆 Top歸測結果
              result=sortPred[0]
              #取出分數
              rate=result['probability'] #float
              tagName=result['tagName']
              print(f'分析結果:{tagName} 分數:{rate}') 



              if rate >= 0.7:
                    conn = createConnection()
                    sql = "declare @content nvarchar(100)\nset @content = %s\nSELECT Attactions, Address, BusinessHours, Telephone, TicketPrice, Web FROM Attractions WHERE Attactions LIKE '%' + @content + '%'"
                    AttractionInf = query(conn, sql, (tagName))  
                    msg = f'景點:{AttractionInf[0]}\n地址:{AttractionInf[1]}\n營業時間:\n{AttractionInf[2]}\n電話:{AttractionInf[3]}\n票價:\n{AttractionInf[4]}\n官網:{AttractionInf[5]}'
                    replyMessage(replyToken,f'分析結果為{tagName}\n{tagName}景點資訊如下\n----------------\n{msg}')

                    conn = createConnection()
                    history_sql = 'Insert Into HistoryRecord(UserID,UserRecord) values(%s,%s)'
                    update(conn,history_sql,(userId,f'照片辨識結果為{tagName}'))
                    conn.close()
              else:
                   replyMessage(replyToken,f'照片裡的景點不在南部或該照片不屬於景點照')
              conn.close()
    else:
        response=make_response("",204)     
    return response  
        

   
'''
        #設定header bearer token and Content-Type
              openAIHeader={'Authorization':openaiKey,'Content-Type':'application/json'}
              #設定傳送上去的資料json
              openaiSourceData='您是旅遊規劃專家，'+ content +'請用繁體中文回覆'
              openaiData={"model": "gpt-3.5-turbo","messages": [{"role": "user", "content":openaiSourceData}],"temperature": 0.7}  
              #正式提出請求
              openaiResponse=requests.post(url=openaiURL,headers=openAIHeader,data=json.dumps(openaiData))
              print(openaiResponse.json())
              #Openai api語意回應的結果 取出內容
              aiData=openaiResponse.json()
              content=aiData['choices'][0]['message']['content']
              #print(content)
              #反序列化字串為物件dict 
              replyMessage(replyToken,f'{content}')  
       '''    