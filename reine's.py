import discord
from googletrans import Translator
from discord.ext import commands
import requests
import xml.etree.ElementTree as ET
import json
import random
import asyncio
import re



client = discord.Client(verbose=True)
translator = Translator()




# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(',trans'):
        say = message.content
        say = say[7:]
        if say.find('-') == -1:
            str = say
            detact = translator.detect(str)
            befor_lang = detact.lang
            if befor_lang == 'ja':
                convert_string = translator.translate(str, src=befor_lang, dest='en')
                embed = discord.Embed(title='翻訳しました！　Done!', color=0xff0000)
                embed.add_field(name='-----------------------------', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
            else:
                convert_string = translator.translate(str, src=befor_lang, dest='ja')
                embed = discord.Embed(title='翻訳しました！　Done!', color=0xff0000)
                embed.add_field(name='-----------------------------', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
        else:
            trans, str = list(say.split('='))
            befor_lang, after_lang = list(trans.split('-'))
            convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
            embed = discord.Embed(title='翻訳しました！　Done!', color=0xff0000)
            embed.add_field(name='-----------------------------', value=convert_string.text, inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(',detect'):
        say = message.content
        s = say[8:]
        detect = translator.detect(s)
        m = 'この文字列の言語はたぶん ' + detect.lang + ' です。'
        await message.channel.send(m)


#挨拶
    if re.search("おはよう", message.content):
        if client.user != message.author:
            gm = "おはようございます" + message.author.name + "さん！"
            await message.channel.send(gm)

    if re.search("こんにちは", message.content):
        if client.user != message.author:
            ga = "こんにちは" + message.author.name + "さん！"
            await message.channel.send(ga)

    if re.search("こんばんは", message.content):
        if client.user != message.author:
            ge = "こんばんは" + message.author.name + "さん！"
            await message.channel.send(ge)


#helpやinfo
    if message.content.startswith(",info"):
        if client.user != message.author:
            embed = discord.Embed(title="すてぃら", description="こんにちは！すてぃらといいます！私は「雨宿り ReiNe Shelter:umbrella:」のオーナーReiNeによるBotです。よろしくお願いしますね^^", color=0x87cefa)
            embed.add_field(name="作成者", value="ReiNe#3517")
            embed.add_field(name="おでかけサーバー数", value=2)
            embed.add_field(name="招待リンク", value="https://discordapp.com/api/oauth2/authorize?client_id=564272479346884613&permissions=8&scope=bot")
            await message.channel.send(embed=embed)





#地震情報
    if message.content == ',地震情報':
        er = e()
        embed = discord.Embed(title='**地震情報**', description='', color=er['color'])
        embed.set_thumbnail(url=er['icon'])
        embed.add_field(name='発生時刻', value=er['time'], inline=True)
        embed.add_field(name='震源地', value=er['epicenter'], inline=True)
        embed.add_field(name='最大震度', value=er['intensity'], inline=True)
        embed.add_field(name='マグニチュード', value=er['magnitude'], inline=True)
        embed.add_field(name='震度1以上を観測した地域', value=er['e_1'], inline=False)
        embed.set_image(url=er['map'])
        await message.channel.send(embed=embed)
def e():
    xml_data_module = requests.get('https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml')
    xml_data_module.encoding = "Shift_JIS"
    root = ET.fromstring(xml_data_module.text)
    for item in root.iter('item'):
       deta_url = (item.attrib['url'])
       break
    deta = requests.get(deta_url)
    deta.encoding = "Shift_JIS"
    root = ET.fromstring(deta.text)
    e_1 = ''
    for Earthquake in root.iter('Earthquake'):
        time = (Earthquake.attrib['Time'])
        Intensity = (Earthquake.attrib['Intensity'])
        Epicenter = (Earthquake.attrib['Epicenter'])
        Magnitude = (Earthquake.attrib['Magnitude'])
        Depth = (Earthquake.attrib['Depth'])
        map_url = 'https://www3.nhk.or.jp/sokuho/jishin/'
        count = 1
    for Area in root.iter('Area'):
        e_1 += '\n' + Area.attrib['Name']
        if count == 10:
            e_1 += '\n他'
            break
        count = count + 1
    for Detail in root.iter('Detail'):
        map = map_url + Detail.text
        edic = {'time': time, 'epicenter': Epicenter, "intensity": Intensity, "depth": Depth, "magnitude": Magnitude, "map": map, "icon": eicon(Intensity), "color": eicolor(Intensity), 'e_1': e_1}
        return edic
def eicon(i):
    if i == '1':
        return('https://i.imgur.com/yalXlue.png')
    elif i == '2':
        return('https://i.imgur.com/zPSFvj6.png')
    elif i == '3':
        return('https://i.imgur.com/1DVoItF.png')
    elif i == '4':
        return("https://i.imgur.com/NqC3CE0.png")
    elif i == '5-':
        return("https://i.imgur.com/UlFLa3G.png")
    elif i == '5+':
        return("https://i.imgur.com/hExQwf2.png")
    elif i == '6-':
        return("https://i.imgur.com/p9RrO96.png")
    elif i == '6+':
        return("https://i.imgur.com/pNaFJ2Y.png")
    elif i == '7':
        return("https://i.imgur.com/ZoOhL4v.png")
def eicolor(i):
    if i == '1':
        return(0x51b3fc)
    elif i == '2':
        return(0x7dd45a)
    elif i == '3':
        return(0xf0ed7e)
    elif i == '4':
        return(0xfa782c)
    elif i == '5-':
        return(0xb30f20)
    elif i == '5+':
        return(0xb30f20)
    elif i == '6-':
        return(0xffcdde)
    elif i == '6+':
        return(0xffcdde)
    elif i == '7':
        return(0xffff6c)







client.run('NTY0MjcyNDc5MzQ2ODg0NjEz.XfjCrw.AQSxeN92qYE1x97Xg9sk0L7JAoI')