import os
import sys
import markovify
import markov

from flask import Flask, abort, redirect, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (AudioMessage, ButtonsTemplate, CameraAction,
                            CameraRollAction, CarouselColumn, CarouselTemplate,
                            ConfirmTemplate, DatetimePickerAction, FileMessage,
                            FollowEvent, ImageCarouselColumn,
                            ImageCarouselTemplate, ImageMessage,
                            ImageSendMessage, JoinEvent, LeaveEvent,
                            LocationAction, LocationMessage,
                            LocationSendMessage, MessageAction, MessageEvent,
                            PostbackAction, PostbackEvent, QuickReply,
                            QuickReplyButton, SourceGroup, SourceRoom,
                            SourceUser, StickerMessage, StickerSendMessage,
                            TemplateSendMessage, TextMessage, TextSendMessage,
                            UnfollowEvent, URIAction, VideoMessage)

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


# static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# @app.route('/static/<path:path>')
# def send_static_content(path):
#     return send_from_directory('static', path)

# def make_static_tmp_dir():
#     try:
#         os.makedirs(static_tmp_path)
#     except OSError as exc:
#         if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
#             pass
#         else:
#             raise


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text = event.message.text

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + str(profile.display_name)),
                    TextSendMessage(text='Status message: ' + str(profile.status_message)),
                    TextSendMessage(text='User ID: ' + profile.user_id)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))

    elif text == '@bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving room'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))

    elif text == 'image':
        url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/LINE_logo.svg/1024px-LINE_logo.svg.png'
        app.logger.info("url=" + url)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(url, url)
        )

    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'quick_reply':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ])))

    elif text == '.melos':

        # Load from JSON
        json = open('melos.json').read()
        text_model = markovify.Text.from_json(json)
        try:
            sentence = markov.make_sentences(text_model, start='', max=150, min=20)
        except KeyError:
            sentence = 'Error'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=sentence)
        )


    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=text + '！')
        )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    available_sticker_packages = [1, 2, 3, 4, 11537, 11538, 11539]
    if int(event.message.package_id) in available_sticker_packages:
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id=event.message.package_id,
                sticker_id=event.message.sticker_id
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="I don't have that sticker. I'm jealous!")
        )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title='Location', address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    # message_content = line_bot_api.get_message_content(event.message.id)
    # with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
    #     for chunk in message_content.iter_content():
    #         tf.write(chunk)
    #     tempfile_path = tf.name

    # dist_path = tempfile_path + '.' + ext
    # dist_name = os.path.basename(dist_path)
    # os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Received ' + ext)
            # TextSendMessage(text='Saved content.'),
            # TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    # message_content = line_bot_api.get_message_content(event.message.id)
    # with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
    #     for chunk in message_content.iter_content():
    #         tf.write(chunk)
    #     tempfile_path = tf.name

    # dist_path = tempfile_path + '-' + event.message.file_name
    # dist_name = os.path.basename(dist_path)
    # os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Received file'),
            # TextSendMessage(text='Saved file.'),
            # TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    print('User ' + event.source.user_id + " followed me!")
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Thanks for following me!')
    )


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print('User ' + event.source.user_id + " unfollowed me...")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type + '!'))


@handler.add(LeaveEvent)
def handle_leave(event):
    print("Got leave event: " + str(event.source))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
