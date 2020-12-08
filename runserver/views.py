from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from runserver.locationTransfer import get_nearby_restaurant
import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def handle_text(event):
    if event.message.text == "我是87":
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text='你是87'))
    else:
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text=event.message.text))


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.type == "message":
                    if event.message.type == 'location':
                        urlList = get_nearby_restaurant(str(event.message.latitude), str(event.message.longitude))
                        if not urlList:
                            line_bot_api.reply_message( event.reply_token, TextSendMessage(text='error happen'))
                        else:
                            line_bot_api.reply_message( event.reply_token, [TextSendMessage(text= i) for i in urlList[0:5]])
                    if event.message.type == "text":
                        handle_text(event)
                    else:
                        line_bot_api.reply_message( event.reply_token, TextSendMessage(text='我聽不懂'))
                else:
                    print("un recognize message")
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


