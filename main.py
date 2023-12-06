from fastapi import FastAPI, Request
import openai
import os
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage

OPENAI_API_KEY = os.environ.get('API_KEY')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_AKEY')
LINE_CHANNEL_SECRET = os.environ.get('LINE_SKEY')
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



