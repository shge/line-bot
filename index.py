import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/")
def redirect_page():
    return 'https://github.com/shge/line-bot'
    # return redirect("https://github.com/shge/line-bot", code=303)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)  #
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    # port = int(os.getenv("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)

# from http.server import BaseHTTPRequestHandler
#
# PUSH_URL = "https://api.line.me/v2/bot/message/push"
# REPLY_URL = "https://api.line.me/v2/bot/message/reply"
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
