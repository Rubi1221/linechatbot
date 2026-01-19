# Smart Travel Assistant Chatbot System

旅遊已經成為了現在人們生活的基本需求，每到假日就會有部分人選擇規劃旅遊來抒發平常生活中所承受的壓力。隨著科技的進步，人們想要規劃旅遊，都會透過網際網路來獲取資訊，並藉由這些資訊來規劃旅遊。但是網路上給的資訊都不一樣，這樣在規劃行程或是查詢景點時，都要尋找多個不同的建議來規劃行程，這樣是很花費時間的。我們想要解決的是要如快速有效地收集正確資訊，並規劃行程，本專題會以南部景點為例子，研發一個智慧旅遊規劃推薦系統，該系統具有查詢旅遊景點、規劃旅遊形成、景點照片辨識等功能。
本系統會以Line Bot呈現，並結合近期熱門的AI技術透過Line Bot提供詳細的熱門景點資訊，結合旅遊導覽，使旅客能夠不用花費時間蒐集資料也能享受美好的旅程務。該系統整合了安排行程和推薦景點的功能，以提升整體使用者體驗。


---

## 功能介紹

- 使用者訊息接收與身份識別
- 圖片輸入：旅遊景點影像辨識
- 文字輸入：
  - 景點／縣市查詢
  - 個人化旅遊行程規劃
  - 歷史互動紀錄查詢
- 使用者資料與查詢紀錄儲存

---

## 系統架構

- 前端／訊息平台：Message API
- 後端服務：Flask
- Webhook：接收與處理使用者訊息
- AI 服務：
  - Microsoft Azure Image Recognition API
  - OpenAI API（ChatGPT）
- 資料庫：SQL Server
<img width="865" height="350" alt="image" src="https://github.com/user-attachments/assets/5d527e7a-d523-4246-b812-62e075a3894b" />

---

## 系統功能流程操作

- 景點查詢功能
  
<img width="1039" height="458" alt="image" src="https://github.com/user-attachments/assets/383cf21a-77d0-458d-90da-408c8876eed1" />




- 規劃行程功能
  
<img width="1286" height="498" alt="image" src="https://github.com/user-attachments/assets/68736e5c-2fa3-417b-964a-c86e305bcd4c" />


- 景點照片辨識功能
  
<img width="1086" height="501" alt="image" src="https://github.com/user-attachments/assets/31547483-2f1b-473e-8052-4461c061f04a" />

- 歷史紀錄查詢功能
<img width="1307" height="517" alt="image" src="https://github.com/user-attachments/assets/11a3cd11-15ad-49c0-a357-b8bb7f5d3296" />



 

---
