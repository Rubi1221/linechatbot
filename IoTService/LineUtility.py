#引用Http client
import requests
import json 
#Replye Message API端點
replyURL='https://api.line.me/v2/bot/message/reply'
#lineToken=' '#Bearer
getContent='https://api-data.line.me/v2/bot/message/%s/content'

pushMessageURL='https://api.line.me/v2/bot/message/push'
audioPath='https://10c5-61-227-123-132.ngrok-free.app/static/audio/'
#定義回復文字訊息的功能
def replyMessage(replyToken,message):
    #回應訊息的dict物件 
    msg={
    "replyToken":replyToken,
    "messages":[
        {
            "type":"text",
            "text":message
        }
    ]
       }
    #定義Header dict
    myHeader={"Content-Type":"application/json","Authorization":lineToken}
    #呼叫reply message api
    requests.post(url=replyURL,data=json.dumps(msg),headers=myHeader)
def replyTextAndAudioMessage(replyToken,message,audioFile,duration):
    #回應訊息的dict物件 
    msg={
    "replyToken":replyToken,
    "messages":[
        {
            "type":"text",
            "text":message
        },
        {
            "type":'audio',
            "originalContentUrl":audioPath+audioFile+'.mp3',
            "duration":duration #毫秒 1000=1秒

        }
    ]
   
    }
    #定義Header dict
    myHeader={"Content-Type":"application/json","Authorization":lineToken}
    #呼叫reply message api
    response=requests.post(url=replyURL,data=json.dumps(msg),headers=myHeader)
    print(response.json())

#讀取特定image id 圖檔
def readImage(imageId):
    #line get content api
    urlString=getContent %(imageId)
    print(urlString) 
    #正式提出請求 Line Token
    myHeader={"Authorization":lineToken}
    response=requests.get(url=urlString,headers=myHeader)
    #進行串流讀取
    if response.status_code==200:
       #try with resource with 開啟 在區段(縮排結束) 會自動執行close
       #wb
       with open("c:/tools/sample.jpg", 'wb') as f:
            print(type(response.content))
            f.write(response.content) #response透過content 取回bytes class(bytes array)
       #auto close file  
    return response.content  #回應bytes 類別
      
               
#send push Message(後端啟動 送出訊息到特定Line user id端)
def sendPushTextMessage(userid,message):
    #設定Request Header
    myHeaders={"Content-Type":"application/json","Authorization":lineToken}
    #訊息
    msg={"to":userid,"messages":[{"type":"text","text":message}]}
    #使用requests client
    requests.post(pushMessageURL,data=json.dumps(msg),headers=myHeaders)


from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫

from linebot.models import MessageAction, TemplateSendMessage, CarouselTemplate,  CarouselColumn
def CityandType(reolyToken):
    line_bot_api = LineBotApi('9SPKUcepOU2MwzV1rCr1IXivJQTEHteiKUr9gWYT1MUJgg3nPBCC6Mm01RFPCS42HzXbZNd0TPW1Kaqs6TbKM8T5bO6kMbMhen0zBjgRXwBqWTBh97DL7w4eyMWotBrgEDdNmPCpI494/ge86QK1LQdB04t89/1O/w1cDnyilFU=')
    line_bot_api.reply_message(reolyToken, TemplateSendMessage(
        alt_text='旅遊規劃選單',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://blog.tripbaa.com/wp-content/uploads/2020/01/content_a54af05dd75478a5c2d9f5ad588ca70c2299ef3f736c79219260cefe.png',
                    title='嘉義',
                    text='旅遊規劃',
                    actions=[
                        MessageAction(
                            label='戶外類型',
                            text='嘉義:戶外類型'
                        ),
                        MessageAction(
                            label='室內場所',
                            text='嘉義:室內場所'
                        ),
                        MessageAction(
                            label='文藝氣息',
                            text='嘉義:文藝氣息'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/6/6e/%E5%AE%89%E5%B9%B3%E5%8F%A4%E5%A0%A1%E4%B9%8B%E7%BE%8E.jpg',
                    title='台南',
                    text='旅遊規劃',
                    actions=[
                        MessageAction(
                           label='戶外類型',
                            text='臺南:戶外類型'
                        ),
                        MessageAction(
                            label='室內場所',
                            text='臺南:室內場所'
                        ),
                        MessageAction(
                            label='文藝氣息',
                            text='臺南:文藝氣息'
                        )
                    ]
                ),CarouselColumn(
                    thumbnail_image_url='https://www.tnupacktour.com.tw/image/data/711.jpg',
                    title='高雄',
                    text='旅遊規劃',
                    actions=[
                        MessageAction(
                           label='戶外類型',
                            text='高雄:戶外類型'
                        ),
                        MessageAction(
                            label='室內場所',
                            text='高雄:室內場所'
                        ),
                        MessageAction(
                            label='文藝氣息',
                            text='高雄:文藝氣息'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://puddings.tw/wp-content/uploads/pixnet/80a8ddcad5c1f252ab7869f0d17be49f.jpg',
                    title='屏東',
                    text='旅遊規劃',
                    actions=[
                        MessageAction(
                           label='戶外類型',
                            text='屏東:戶外類型'
                        ),
                        MessageAction(
                            label='室內場所',
                            text='屏東:室內場所'
                        ),
                        MessageAction(
                            label='文藝氣息',
                            text='屏東:文藝氣息'
                        )
                        
                    ]
                ),
                
            ]
        )
    ))