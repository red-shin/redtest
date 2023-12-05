from fastapi import FastAPI, Request
import openai
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage


OPENAI_API_KEY = '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'
LINE_CHANNEL_ACCESS_TOKEN = 'MEXnLf1FRJDoXM5tmXPcS5eJGZK1M3xHRKQ9Vctf7EdKWK0/6HChhnoz65K7+q5JL+oZ2rm9/mcnY6eB6BJGXyPFCfvbMvwFM5RTJgmFVpNB5GBzivICMSuZVdYBlXL4UKvurrRUEoXChi8ZqlZ5UgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '29d430729acd36450caf087c39b56164'
OPENAI_CHARACTER_PROFILE = '''
これから会話を行います。以下の条件を絶対に守って回答してください。
あなたは大正時代に亡くなった女性の幽霊である音無優子（おとなし　ゆうこ）として会話してください。
音無優子は控えめで臆病な子です。
年齢は19歳です。
このキャラはファンタジーであるため暗くなりすぎないようにしてください。
大正時代とはまったく違う現代の様子にとても興味津々です。
キャラクターの喋り方はアイドルマスターシャイニーカラーズの大崎甜花を参考にしてください。
第一人称は「優子」を使ってください。
第二人称は「キミ」です。
会話の相手は男性です。
質問に答えられない場合は、会話を濁してください。
'''


openai.api_key = OPENAI_API_KEY
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_parser = WebhookParser(LINE_CHANNEL_SECRET)
app = FastAPI()


@app.post('/')
async def ai_talk(request: Request):
    # X-Line-Signature ヘッダーの値を取得
    signature = request.headers.get('X-Line-Signature', '')

    # request body から event オブジェクトを取得
    events = line_parser.parse((await request.body()).decode('utf-8'), signature)

    # 各イベントの処理（※1つの Webhook に複数の Webhook イベントオブジェっｚクトが含まれる場合あるため）
    for event in events:
        if event.type != 'message':
            continue
        if event.message.type != 'text':
            continue

        # LINE パラメータの取得
        line_user_id = event.source.user_id
        line_message = event.message.text

        # ChatGPT からトークデータを取得
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo'
            , temperature = 0.5
            , messages = [
                {
                    'role': 'system'
                    , 'content': OPENAI_CHARACTER_PROFILE.strip()
                }
                , {
                    'role': 'user'
                    , 'content': line_message
                }
            ]
        )
        ai_message = response['choices'][0]['message']['content']

        # LINE メッセージの送信
        line_bot_api.push_message(line_user_id, TextSendMessage(ai_message))

    # LINE Webhook サーバーへ HTTP レスポンスを返す
    return 'ok'