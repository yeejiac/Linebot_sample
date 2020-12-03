from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# Create your views here.

message = {
      type: 'text',
      text: reply_text
    }

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
                if event.type == "text":
                    line_bot_api.reply_message( event.reply_token, TextSendMessage(text=event.message.text))
                elif event.type == "location":
                    locations = Location.objects.filter(area=event.message.text)
                    reply_text =  locations.latitude + "," + locations.longitude
                    line_bot_api.reply_message( event.reply_token, message)
                else:
                    line_bot_api.reply_message( event.reply_token, TextSendMessage(text=event.message.text))
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

