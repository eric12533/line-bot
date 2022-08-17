from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('wSsbcG6/Dm9RdTvaSGUYyImcSCrvWfZGln6sSAESEpkLO1e2WbnO1S6gcpzRzFAtGyM/tmwXCURnUzLGSwBcN7xXybPvAi7arrrjg7P9OK9ykuxLZU0hff67x3OMbLRSv1bzOrQ97+UJl2Pm0YgHsgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9edf85d5b7f53536a6f0f28e2df78608')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()