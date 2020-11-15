# coding: utf-8
from discord.ext import commands
import discord
import os
import platform
from os.path import join, dirname
from dotenv import load_dotenv

print('===== もだねちゃんを起動します =====')
print('python ' + platform.python_version())
print('discord.py ' + discord.__version__)

bot = commands.Bot(command_prefix='!mdn ') # コマンド実行を示す「!mdn 」を指定
bot.remove_command('help') # デフォルトの help を削除

# bot 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルへログイン通知を表示
    print('===== ログインしました =====')
    print('===== bot 起動時の処理を実行します =====')

    # アクティビティ表示を変更
    print('--- アクティビティ表示を変更 ---')
    client = bot
    act = discord.Game('「 !mdn h 」でヘルプを表示するよ！             ') # \U0001f338: 🌸
    await client.change_presence(status=None, activity=act)

    print('===== bot 起動時の処理を完了しました =====')

@bot.event
async def on_command_error(ctx, error):
    print('--- エラーコード：001 ---')
    embed = discord.Embed(title='コマンドを受け付けられませんでした',description='なんらかの原因でコマンドを実行できなかったよ。ごめんね。\n以下のコマンドを実行して、使い方を確認してみてね！', color=0xeaa55c)
    embed.add_field(name='ㅤ\n❓ ヘルプを表示する', value='```!mdn h```', inline=False)
    await ctx.send(embed=embed)

# Cogの読み込み
bot.load_extension('cogs.talk')
bot.load_extension('cogs.janken')
bot.load_extension('cogs.help')
bot.load_extension('cogs.hello')
bot.load_extension('cogs.uranai')
bot.load_extension('cogs.petite')
bot.load_extension('cogs.reload')

# .envファイルの読み込み
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Botの起動とDiscordサーバーへの接続
bot.run(BOT_TOKEN)