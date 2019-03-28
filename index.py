import os
from flask import Flask, request, abort, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/", methods=['GET'])
def redirect_page():
    return redirect("https://github.com/shge/line-bot", code=303)


@app.route("/", methods=['POST'])
def callback():
    try:
        signature = request.headers['X-Line-Signature']
    except KeyError:
        print("No signature in header.")
        abort(400)

    body = request.get_data(as_text=True)
    print("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Signature was in header, but invalid.")
        abort(400)

    return abort(200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


# if __name__ == "__main__":
#     app.run()
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
