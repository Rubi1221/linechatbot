#從flask模組引用到Flask類別class
from flask import Flask     
#建構Flask物件 在分享到整個系統模組去
#app global variable
app=Flask('__main__')
#package初始化引用DHTController 模組 裡面定義的端點route會生效


import IoTService.LineBotService
