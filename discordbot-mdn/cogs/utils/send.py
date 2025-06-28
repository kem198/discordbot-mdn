"""send message from bot"""

import asyncio
import logging
import discord

# 色の設定
COLOR_NORMAL = 0xffd6e9
COLOR_RUNNING = 0xe3e5e8
COLOR_WARNING = 0xffab6f

async def send_help(target):
    """
    ヘルプ機能のメッセージ送信: コマンド一覧

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'もだねちゃんヘルプ'
    description = 'もだねちゃんのスラッシュコマンド一覧だよ！\nもっと詳しい操作方法は [📙ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙お仕事内容ガイドブック) を確認してみてね。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```/talk-begin```', inline=False)
    embed.add_field(name='ㅤ\n🎤 読み上げを終了する', value='```/talk-end```', inline=False)
    embed.add_field(name='ㅤ\n✌ ジャンケンで遊ぶ',   value='```/janken```', inline=False)
    embed.add_field(name='ㅤ\n🔮 もだねちゃん占い',   value='```/uranai```', inline=False)
    embed.add_field(name='ㅤ\n❓ ヘルプを表示する',   value='```/help```', inline=False)
    embed.set_footer(text='ㅤ\nヒント:\n「!mdn」から始まる従来のコマンドでも操作できます。\n使用方法はガイドブックを参照してください。')

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_begin(target, talk_vc, talk_channel_id):
    """
    読み上げ機能のメッセージ送信: 読み上げ開始

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    talk_vc : class
        入室するボイスチャンネルのクラス
    talk_channel_id : int
        読み上げ対象のテキストチャンネルの ID
    """
    title = '読み上げを開始するよ'
    description = 'こちらの内容でおしゃべりを始めるね！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    embed.add_field(name='ㅤ\n🎤 入室ボイスチャンネル', value=talk_vc)
    embed.add_field(name='ㅤ\n📗 読み上げ対象チャンネル', value=f'<#{str(talk_channel_id)}>')
    embed.set_footer(text='ㅤ\nヒント: \n読み上げ対象を再設定したい時は、対象のテキストチャンネルで「/talk-begin」コマンドを再実行してください。')

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_restart(target, talk_channel_id):
    """
    読み上げ機能のメッセージ送信: 読み上げ対象チャンネルを再設定

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    talk_channel_id : int
        読み上げ対象のテキストチャンネルの ID
    """
    title = '読み上げ対象を再設定したよ'
    description = 'こちらのテキストチャンネルでおしゃべりを再開するね！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    embed.add_field(name='ㅤ\n📗 読み上げ対象チャンネル', value=f'<#{str(talk_channel_id)}>')

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_wait(target):
    """
    読み上げ機能のメッセージ送信: 読み上げ開始を待機

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = '読み上げの実施を待機するよ'
    description = '読み上げを開始するには、10秒以内にボイスチャンネルへ入室してね。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_RUNNING
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_stop(target):
    """
    読み上げ機能のメッセージ送信: 読み上げ開始を中断

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = '読み上げの実施を中断したよ'
    description = '読み上げを開始するには、コマンドを実行した方がボイスチャンネルへ入室してね。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_WARNING
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_end(target):
    """
    読み上げ機能のメッセージ送信: 読み上げを終了

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = '読み上げを終了したよ'
    description = 'ボイスチャンネルから退出して読み上げを終了しました。またね！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_end_auto(target):
    """
    読み上げ機能のメッセージ送信: 読み上げを終了（自動退出）

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = '読み上げを終了したよ'
    description = '皆いなくなったので、ボイスチャンネルから退出しました。またね！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_not_in_vc(target):
    """
    読み上げ機能のメッセージ送信: 読み上げ終了コマンドを受け取ったが、もだねちゃんがボイスチャンネルにいなかったとき

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'コマンドを受け付けられませんでした'
    description = 'そのコマンドは、私がボイスチャンネルへ入室している時のみ使用できるよ。\nこちらのコマンドを先に実行してね。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_WARNING
    )

    embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```/talk-begin```', inline=False)

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_talk_reconnect(target):
    """
    読み上げ機能のメッセージ送信: 再接続処理

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'ボイスチャンネルへ再入室しました'
    description = 'もだねちゃんが再起動したので、再接続処理を行いました。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_uranai_result(target, fortune_list, star_result_list, lucky_item):
    """
    占い機能のメッセージ送信: 結果

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'もだねちゃん占い'
    description = f'{target.author.display_name} さんの今日の運勢だよ！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_NORMAL
    )

    # 占い結果の表示
    for i in range(3):
        embed.add_field(name='ㅤ\n' + fortune_list[i], value=star_result_list[i])

    # ラッキーアイテムの表示
    embed.add_field(name='ㅤ\nラッキーアイテム', value=lucky_item)

    # 結果を送信
    await target.send(embed=embed)

    # 1秒待機後、結果に応じて台詞を送信する
    await asyncio.sleep(1)
    async with target.channel.typing():
        await asyncio.sleep(.5)
    if '⭐️⭐️⭐️⭐️⭐️⭐️' in star_result_list:
        await target.send('わっ！★6 の運勢があるよ！\n今日はとっても良い日になりそうだね🌸\n\nまたねーっ！')
    else:
        await target.send('結果はどうだった？またねー！')
    logging.info('メッセージを送信: %s', title)

async def send_uranai_played(target):
    """
    占い機能のメッセージ送信: 占い済み

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'もだねちゃん占いは 1日1回までだよ'
    description = f'{target.author.display_name} さんの運勢はもう占っちゃった！\nまた明日遊んでね！'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_WARNING
    )

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_on_command_error(target):
    """
    コマンドエラーを送信する

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    title = 'コマンドを受け付けられませんでした'
    description = 'なんらかの原因でコマンドを実行できなかったよ。ごめんね。\nコマンドが正しいか確認してみてね。'

    embed = discord.Embed(
        title=title,
        description=description,
        color=COLOR_WARNING
    )

    embed.add_field(name='ㅤ\n❓ ヘルプを表示する', value='```/help```', inline=False)
    embed.set_footer(text='ㅤ\n正しくコマンドを送信している場合でもこのメッセージが表示されることがあります。\n\n読み上げ関連の操作でこのメッセージが出てしまう場合は、「/talk-begin」を送信して読み上げ対象チャンネルの再設定をお試しください。\n\n問題が解決されない場合、お手数ですが以下の手順でもだねちゃんを切断してあげてください。\n\n1. ボイスチャンネルのもだねちゃんを右クリックする。\n2.「切断」を選ぶ。')

    await target.send(embed=embed)
    logging.info('メッセージを送信: %s', title)

async def send_yahho(target):
    """
    あいさつを送信する

    Parameters
    ----------
    target : class
        send() を実行する対象のクラス
    """
    text = 'やっほー！もだねちゃんだよ！'

    await target.send(text)
    logging.info('メッセージを送信: %s', text)
