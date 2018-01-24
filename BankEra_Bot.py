import discord
import urllib.request as req

from coinmarketcap import Market
from bs4 import BeautifulSoup


# 本番token
#token = "NDA1MzY1ODI0NDQyOTkwNTky.DUjV6A.kVeYsW0rldoLX4BtKczQCiXqI58"
# テストtoken
token = "NDA0NjE4MDA4MjA0NTQxOTYy.DUoAtQ.DqDyvVDhSIQSMD-KNRtx86WKRgo"
unit_price = 0.019
correction = 131

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
            m = "報告します！ 現在 " + str(count) + "人のエラリストが参加中です！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
        elif message.content.startswith("?btc") | message.content.startswith("?BTC"):
            market = Market()
            # coinmarketcapからBTCをユーロ建てで取得
            coin = market.ticker("bitcoin", convert='EUR')[0]

            # ユーロを下３桁で四捨五入
            eur = round(float(coin['price_eur']), 3)
            # バンクエラの価格で割り込み、購入可能なコイン数を算出
            bankera = (eur - correction) / unit_price
            echo = "1BTCで約" + str(round(bankera, 8)) + "コイン購入できます。"

            await client.send_message(message.channel, echo)
        elif message.content.startswith("?諭吉") | message.content.startswith("？諭吉"):
            url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=eurjpy"
            res = req.urlopen(url)

            soup = BeautifulSoup(res, 'html.parser')
            eur = soup.select_one(".stoksPrice").string

            bankera = 10000 / (float(eur) * unit_price)
            echo = "1万円で約" + str(round(bankera, 8)) + "コイン購入できます。"

            await client.send_message(message.channel, echo)


client.run(token)
