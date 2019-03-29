import os
import sys

from flask import Flask, abort, redirect, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (MessageEvent, SourceUser, TextMessage,
                            TextSendMessage)

app = Flask(__name__)
access_token = os.getenv('ACCESS_TOKEN', None)
channel_secret = os.getenv('CHANNEL_SECRET', None)
if access_token is None or channel_secret is None:
    print('Specify ACCESS_TOKEN and CHANNEL_SECRET as environment variables.')
    sys.exit(1)
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)


@app.route('/', methods=['GET'])
def redirect_page():
    print('Redirected: ' + request.remote_addr)
    return redirect('https://github.com/shge/line-bot', code=303)


@app.route('/', methods=['POST'])
def callback():
    try:
        signature = request.headers['X-Line-Signature']
    except KeyError:
        print('No signature in header:' + request.remote_addr)
        abort(400)

    body = request.get_data(as_text=True)
    print('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("LINE Messaging API Error: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        print('Signature was in header, but invalid:' + request.remote_addr)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text = event.message.text

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + profile.status_message)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=text + '！')
        )
