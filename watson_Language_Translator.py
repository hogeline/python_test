import discord
import sys
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

username = sys.argv[1]
password = sys.argv[2]

language_translator = LanguageTranslator(
    username = username,
    password = password
)

# テストtoken
token = "NDA0NjE4MDA4MjA0NTQxOTYy.DUoAtQ.DqDyvVDhSIQSMD-KNRtx86WKRgo"

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
        text = message.content  # メッセージを取り出す
        # 言語識別
        language = language_translator.identify(text)
        source = language['languages'][0]['language']
        if source == 'en':
            target = 'ja'
        elif source == 'ja':
            target = 'en'
        elif source == 'de':
            target = 'en'
        else:
            source = 'ja'
            target = 'en'
        # 翻訳
        translation = language_translator.translate(
            text=text,
            source=source,
            target=target)

        msg = translation["translations"][0]["translation"]

        await client.send_message(message.channel, msg)


client.run(token)
