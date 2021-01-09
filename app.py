import requests
import configparser
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from locationTransfer import get_nearby_restaurant
import json


app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['LINE_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(config['line_bot']['LINE_CHANNEL_SECRET'])


def handle_text(event):
    if event.message.text == "我是87":
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text='你才87'))
    elif event.message.text == "你是87":
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text='對'))
    else:
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text=event.message.text))


@app.route("/mylinebot/callback", methods=['POST'])
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            for event in events:
                if isinstance(event, MessageEvent):  # 如果有訊息事件
                    print(event)
                    if event.type == "message":
                        if event.message.type == 'location':
                            urlList = get_nearby_restaurant(str(event.message.latitude), str(event.message.longitude))
                            if not urlList:
                                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='error happen'))
                            else:
                                if len(urlList) == 0:
                                    line_bot_api.reply_message( event.reply_token, TextSendMessage(text='error happen'))
                                elif len(urlList) < 5:
                                    line_bot_api.reply_message( event.reply_token, [TextSendMessage(text= i) for i in urlList])
                                else:
                                    line_bot_api.reply_message( event.reply_token, [TextSendMessage(text= i) for i in urlList[0:5]])
                        if event.message.type == "text":
                            handle_text(event)
                            # data = [event.source.user_id, "", event.message.text]
                        else:
                            line_bot_api.reply_message( event.reply_token, TextSendMessage(text='我聽不懂'))
                    else:
                        print("un recognize message")
        except InvalidSignatureError:
            print("InvalidSignatureError error")


if __name__ == '__main__':
    app.run()