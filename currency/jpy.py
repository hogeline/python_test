import urllib.request as req
import json

# 1万円計算用
yukichi = 10000

# class Spectrocoin():

def __init__():
    pass

def getBnk():
    # spectrocoinから相場価格を取得(From:BNK To:BTC)
    url = 'https://spectrocoin.com/scapi/ticker/BNK/JPY'
    res = req.urlopen(url)

    # 取得した価格をjsonに変換
    price_ticker = json.loads(res.read().decode('utf8'))

    # １万円あたりの購入数を算出
    bankera = price_ticker['last'] * yukichi

    # 価格のメッセージを設定
    msg = "1万円で約" + str(round(bankera, 1)) + "BNK購入できます。"

    return msg
