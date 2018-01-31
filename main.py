import discord
#import urllib.request as req
import json
import os
import re

from currency import *
from coinmarketcap import Market
#from bs4 import BeautifulSoup


# 本番token
# token = "NDA1MzY1ODI0NDQyOTkwNTky.DUjV6A.kVeYsW0rldoLX4BtKczQCiXqI58"
# pettyaテストtoken
#token = "NDA0NjE4MDA4MjA0NTQxOTYy.DUoAtQ.DqDyvVDhSIQSMD-KNRtx86WKRgo"
token = "NDA3NTYwNTkxNDM2NDE0OTg2.DVK3gg.3tFv-GiJ0le-qYGGFynn5xARa4A"
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

        # if message.channel.id == "405377859662774281":
        if message.content.lower() == "?cmc":
            # coinmarketcapから価格を取得
            coin = market.ticker("bitcoin", convert='JPY')[0]
            msg = "Coinmarketcap：1BTCは" + str(coin['price_jpy']) + "円です。"
            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)
            # coinmarketcapから価格を取得
            coin = market.ticker("ethereum", convert='JPY')[0]
            msg = "Coinmarketcap：1ETHは" + str(coin['price_jpy']) + "円です。"
            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)
            # coinmarketcapから価格を取得
            coin = market.ticker("ripple", convert='JPY')[0]
            msg = "Coinmarketcap：1XRPは" + str(coin['price_jpy']) + "円です。"
            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)
            # coinmarketcapから価格を取得
            coin = market.ticker("nem", convert='JPY')[0]
            msg = "Coinmarketcap：1XEMは" + str(coin['price_jpy']) + "円です。"
            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)
            # coinmarketcapから価格を取得
            coin = market.ticker("experience-points", convert='JPY')[0]
            msg = "Coinmarketcap：1XPは" + str(coin['price_jpy']) + "円です。"
            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)

            # 送られてきたメッセージの引数が2つあった場合
        elif len(message.content.split(" ")) == 2:
            # 仮想通貨リストのPATH
            path = 'name_conv_list.txt'
            # リストが存在しているとき
            if os.path.isfile(path):
                # ファイルの読み込み
                f = open('name_conv_list.txt', 'r')
                # JSON 形式で読み込む
                json_data = json.load(f)
                # ファイルクローズ
                f.close()
                # ファイルの中身確認用
                # print("{}".format(json.dumps(json_data, indent=4)))
            else:
                msg = path+"を見つけられません"
                await client.send_message(message.channel, msg)
            # float型に変換可能(実数)かどうかの確認に正規表現を使う
            num_reg = re.compile("^\d+(\.\d+)?\Z")
            # 第1引数がcurrency_lsitの中にあり、かつ、第2引数が実数なら
            # coin * 枚数を計算
            args = message.content.split(" ")
            if args[0].lower() == '?btc' and bool(num_reg.match(args[1])):
                # coinmarketcapから価格を取得
                coin = market.ticker("bitcoin", convert='JPY')[0]
                price = float(coin['price_jpy']) * float(args[1])
                msg = "Coinmarketcap：" + str(args[1]) + "BTCは" + str(round(price, 3)) + "円です。"
                # 価格のメッセージを出力
                await client.send_message(message.channel, msg)
            elif args[0].lower() == '?eth' and bool(num_reg.match(args[1])):
                # coinmarketcapから価格を取得
                coin = market.ticker("ethereum", convert='JPY')[0]
                price = float(coin['price_jpy']) * float(args[1])
                msg = "Coinmarketcap：" + str(args[1]) + "ETHは" + str(round(price, 3)) + "円です。"
                # 価格のメッセージを出力
                await client.send_message(message.channel, msg)
            elif args[0].lower() == '?xem' and bool(num_reg.match(args[1])):
                # coinmarketcapから価格を取得
                coin = market.ticker("nem", convert='JPY')[0]
                price = float(coin['price_jpy']) * float(args[1])
                msg = "Coinmarketcap：" + str(args[1]) + "NEMは" + str(round(price, 3)) + "円です。"
                # 価格のメッセージを出力
                await client.send_message(message.channel, msg)
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
