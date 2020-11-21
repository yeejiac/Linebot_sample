# ChoseNiceStock

# Line bot 控制端
串接herokuo
line bot developer地址(https://developers.line.biz/console/?status=success)
# 選股邏輯
短期目標為選擇三項選股邏輯
ex: 
殖利率較高，外資買賣比較等等

# 爬蟲抓取
爬取證交所網站每日股票成交資料及公開資訊觀測站公司資訊

https://www.twse.com.tw/fund/TWT38U?response=json&date=20201120
https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20201121&stockNo=0056
https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=20201120&selectType=ALL

# 環境條件:
Centos7(可以用docker建，但是要注意服務不能啟動的bug，不過還是建議裝一個虛擬機練習一下Linux的網卡還有其他阿哩布達的設定)
mariadb 10.5
mongodb

# 資料格式
Json + socket 傳輸