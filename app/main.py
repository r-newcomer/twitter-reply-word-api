from pickle import FALSE
from fastapi import FastAPI
# -*- coding: utf-8 -*-
import urllib
from requests_oauthlib import OAuth1Session, OAuth1
import requests
import sys
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/getReplyes/{user_id}/{tweet_id}")
async def getReplyes(user_id: str, tweet_id: str):
  # APIの秘密鍵
  CK = 'fleZFPaDqRau5GQCSDvE52K9O'
  CKS = 'VxIW4feseH6yWIkjqeqvWSIYIezZ8uQCVU1Ll8gumc1i7Js5wm'
  AT = '3159940184-IF2oHQHTkrWSDc0WCGAgY9ft9DOvcdCEm3myEBr'
  ATS = 'UAkHLpyh6DCD5k4Rrf78wPfcQWz3c9l8Q955U6daik5tv'
  # ユーザー・ツイートID
  #user_id = '@jalannet'
  #tweet_id = '1579456721335918594' # str型で指定
  print(user_id)
  print(tweet_id)
  # 検索時のパラメーター
  count = 100 # 一回あたりの検索数(最大100/デフォルトは15)
  range = 100 # 検索回数の上限値(最大180/15分でリセット)
  # ツイート検索・リプライの抽出
  tweets = search_tweets(CK, CKS, AT, ATS, user_id, tweet_id, count, range)
  # 抽出結果を表示
  #print(tweets[0:5])
  return json.dumps(tweets, ensure_ascii=False)




def search_tweets(CK, CKS, AT, ATS, user_id, tweet_id, count, range):
    # 文字列設定
    user_id += ' exclude:retweets' # RTは除く
    user_id = urllib.parse.quote_plus(user_id)
    # リクエスト
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)
    auth = OAuth1(CK, CKS, AT, ATS)
    response = requests.get(url, auth=auth)
    #print(response.json())
    data = response.json()['statuses']
    print(data)
    # ２回目以降のリクエスト
    cnt = 0
    reply_cnt = 0
    tweets = []
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > range:
            break
        for tweet in data:
            if tweet['in_reply_to_status_id_str'] == tweet_id: # ツイートIDに一致するものを抽出
                tweets.append(tweet['text'])  # ツイート内容
                reply_cnt += 1
            maxid = int(tweet["id"]) - 1
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        try:
            data = response.json()['statuses']
        except KeyError: # リクエスト回数が上限に達した場合のデータのエラー処理
            print('上限まで検索しました')
            break
    print('検索回数 :', cnt)
    print('リプライ数 :', reply_cnt)
    return tweets
