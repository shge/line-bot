import os
from flask import Flask, request, abort, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


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

    received = event.message.text
    send_message = received + '！'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=send_message)
    )


# if __name__ == '__main__':
#     app.run()
    # port = int(os.getenv('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)

# from http.server import BaseHTTPRequestHandler
#
# PUSH_URL = 'https://api.line.me/v2/bot/message/push'
# REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
#
#
# class handler(BaseHTTPRequestHandler):
#
#     def do_GET(self):
#         self.send_response(303)
#         self.send_header('Location', 'https://github.com/shge/line-bot')
#         # self.send_header('Content-type','text/plain')
#         self.end_headers()
#         # message = 'Hello!'
#         # self.wfile.write(message.encode())
#         return
#
#     def do_POST(self):
#         self.send_response(200)
#         # self.send_header('Content-type','text/plain')
#         self.end_headers()
#         # message = 'Hello!'
#         # self.wfile.write(message.encode())
#         return
