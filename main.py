import discord
#import urllib.request as req
#import json

from currency import *
#from coinmarketcap import Market
#from bs4 import BeautifulSoup


# 本番token
token = "NDA1MzY1ODI0NDQyOTkwNTky.DUjV6A.kVeYsW0rldoLX4BtKczQCiXqI58"
# pettyaテストtoken
#token = "NDA0NjE4MDA4MjA0NTQxOTYy.DUoAtQ.DqDyvVDhSIQSMD-KNRtx86WKRgo"
# 通貨変換対象リスト
currency_list = ['?btc', '?eth', '?xem', '?諭吉']

client = discord.Client()
client.get_all_members()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # 送り主がBotだった場合反応したくないので
    if client.user != message.author:
        if message.content.startswith("?エラリスト") | message.content.startswith("？エラリスト"):
            count = 0
            for member in client.get_all_members():
                count += 1
            msg = "報告します！ 現在 " + str(count) + "人のエラリストが参加中です！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, msg)

        elif message.content in currency_list:
            src = message.content.lower().replace("?", "") + ".getBnk"

            if "諭吉" in src:
                src = src.replace("諭吉", "jpy")

            msg = eval(src)()

            # 価格のメッセージを出力
            await client.send_message(message.channel, msg)


client.run(token)
