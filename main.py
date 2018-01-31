import discord
#import urllib.request as req
import json
import os
import re

from currency import *
from coinmarketcap import Market
#from bs4 import BeautifulSoup


# 本番token
token = "NDA1MzY1ODI0NDQyOTkwNTky.DUjV6A.kVeYsW0rldoLX4BtKczQCiXqI58"
# pettyaテストtoken
# token = "NDA0NjE4MDA4MjA0NTQxOTYy.DUoAtQ.DqDyvVDhSIQSMD-KNRtx86WKRgo"
# yufiテストtoken
# token = "NDA3NTYwNTkxNDM2NDE0OTg2.DVK3gg.3tFv-GiJ0le-qYGGFynn5xARa4A"
# 通貨変換対象リスト
currency_list = ['?btc', '?eth', '?xem', '?諭吉']

client = discord.Client()
client.get_all_members()
market = Market()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global element
    element = "{"

    # 送り主がBotだった場合反応したくないので
    if client.user != message.author:
        if message.content.startswith("?エラリスト") | message.content.startswith("？エラリスト"):
            count = 0
            for member in client.get_all_members():
                count += 1
            msg = "報告します！ 現在 " + str(count) + "人のエラリストが参加中です！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, msg)

        elif message.content.lower() in currency_list:
            src = message.content.lower().replace("?", "") + ".getBnk"

            if "諭吉" in src:
                src = src.replace("諭吉", "jpy")

            msg = eval(src)()

            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)

        if message.channel.id == "405377859662774281":
            # 送られてきたメッセージの引数が2つあった場合
            if len(message.content.split(" ")) == 2:
                try:
                    # 仮想通貨リストファイルのPATH
                    path = 'name_conv_list.txt'
                    # ファイルの読み込み
                    f = open(path, 'r')
                    # JSON 形式で読み込む
                    json_data = json.load(f)
                    # ファイルクローズ
                    f.close()
                    # float型に変換可能(実数)かどうかの確認に正規表現を使う
                    num_reg = re.compile("^\d+(\.\d+)?\Z")
                    # メッセージから引数を取得
                    args = message.content.split(" ")
                    key = args[0].replace("?", "").upper()
                    # 第1引数のkeyがjson_dataの中にあり、かつ、第2引数が実数なら
                    # coin * 枚数を計算
                    if json_data.get(key) is not None and bool(num_reg.match(args[1])):
                        # coinmarketcapから価格を取得
                        coin = market.ticker(json_data[key].replace(" ", "-"), convert='JPY')[0]
                        if (coin.get('error') is None):
                            price = float(coin['price_jpy']) * float(args[1])
                            msg = "Coinmarketcap：" + str(args[1]) + key +"は" + str(round(price, 3)) + "円です。"
                            # 価格のメッセージを出力
                            await client.send_message(message.channel, msg)
                        else:
                            msg = "Coinmarketcapに" + key + "は対応していません"
                            await client.send_message(message.channel, msg)
                except IOError:
                    print("ファイルがありません")
            elif message.content.lower() == "!conv":
                # coinmarketcapから価格を取得
                coin = market.ticker(limit=0)
            for i in range(len(coin)):
                keys = '"' + coin[i]['symbol'] + '"'
                values = '"' + coin[i]['name'] + '"'
                if i != len(coin) - 1:
                    element = element + keys + ":" + values + ","
                else:
                    element = element + keys + ":" + values + "}"
                    f = open('name_conv_list.txt', 'w')
                    f.write(element)
                    f.close()
                    msg = "name_conv_list.txtを作成しました。"
                    await client.send_message(message.channel, msg)
                    #            elif message.content.lower() == "!down_name":
                    #                await client.send_file(message.channel, 'name_conv_list.txt')

client.run(token)
