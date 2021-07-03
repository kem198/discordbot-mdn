import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import random
from datetime import datetime
import subprocess
from .utils import psql


##### 占い用リスト・辞書 #####
# 運勢結果リスト
fortune_list = [
    '🕺 友達運',
    '💞 恋愛運',
    '🎮 ゲーム運',
    '💰 金運',
    '📝 勉強運',
    '💪 健康運',
    '🌈 お天気運',
    '🛌 睡眠運',
    '🖌 お絵描き運',
    '⚽️ スポーツ運',
    '💡 ひらめき運',
    '😭 感動運'
]

# 運勢結果リスト
star_list = ['★', '★★', '★★★', '★★★★', '★★★★★', '⭐️⭐️⭐️⭐️⭐️⭐️']

# ラッキーアイテムリスト
lucky_list = [
    '🍎 赤色',
    '🎇 橙色',
    '🍋 黄色',
    '📗 緑色',
    '🐳 青色',
    '🔮 紫色',
    '🐈‍⬛ 黒色',
    '🐑 白色',
    '🙆‍♂️ リアクション',
    '🍞 パン',
    '🍚 お米',
    '🍖 お肉',
    '🍜 ラーメン',
    '🐟 お魚',
    '🥬 野菜',
    '🍓 果物',
    '💊 お薬',
    '🍫 チョコレート',
    '🍬 アメ',
    '🍛 大好物',
    '🥤 ジュース',
    '🍵 お茶',
    '🐱 猫',
    '🐶 犬',
    '🐿 どうぶつ',
    '🎮 ゲーム',
    '👜 カバン',
    '🖊 ペン',
    '📔 ノート',
    '🎧 音楽',
    '🪕 普段は聴かない音楽',
    '👛 お財布',
    '💬 Discord',
    '💻 パソコン',
    '📱 携帯電話',
    '📺 テレビ',
    '🎞 動画',
    '👕 シャツ',
    '👚 お気に入りの服',
    '👘 あまり着ない服',
    '🚃 電車',
    '🚙 車',
    '🚓 パトカー',
    '🚠 珍しい乗り物',
    '🤝 人助け',
    '🪟 窓',
    '🏙 お昼',
    '🌇 夕焼け',
    '🌌 夜空',
    '🗡 斬撃',
    '🔨 打撃',
    '🏹 射撃',
    '😷 マスク',
    '🧸 ぬいぐるみ',
    '🎏 季節モノ',
    '⏳ 3分',
    '📻 レトロ',
    '🚽 トイレ',
    '🛀 お風呂',
    '🚿 シャワー',
    '💇‍♀️ 自分磨き',
    '💓 ドキドキ',
    '🔑 カギ',
    '🔀 シャッフル再生',
    '🔁 リピート再生',
    '😎 ドヤ顔',
    '😳 びっくり',
    '😄 笑顔',
    '🤔 考察',
    '😆 わーい',
    '😪 おねむ'
    ]

# 遊んだ人リストを定義
played_list = []

# played_list の中身を削除する関数を定義
def delete_played_tb():
    played_list.clear()
    psql.run_query('cogs/sql/uranai/delete_user_id.sql')
    print('===== DB とリストの中身を削除しました =====')


##### コグ #####
class Uranai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 指定日時に DB uranai_played_tb の中身を削除する
    @tasks.loop(seconds=60)
    async def loop():
        now = datetime.now().strftime('%H:%M')
        if now == '00:00':
            delete_played_tb()
    # ループ処理を実行
    loop.start()

    # もだねちゃん占い
    @commands.command(aliases=['u'])
    async def uranai(self, ctx):
        print('===== もだねちゃん占いを開始します =====')

        # DB uranai_played_tb にユーザー ID があるか判定
        async with ctx.channel.typing():
            print('--- DB の ユーザーID をチェック ---')
            played_list = []
            played_list = psql.run_query_to_list('cogs/sql/uranai/select_user_id.sql')

        # played_list にユーザーIDがあるか判定
        if str(ctx.author.id) in played_list:
            print('--- 遊んだ人リストにIDがあるため中断 ---')
            embed = discord.Embed(title='もだねちゃん占いは 1日1回までだよ',description=f'{ctx.author.display_name}さんの運勢はもう占っちゃった！\nまた明日遊んでね！', color=0xffab6f)
            await ctx.send(embed=embed)
            print('===== もだねちゃん占いを終了します =====')
            return

        # 運勢占い処理
        print('--- 運勢 3つを決定 ---')
        random.shuffle(fortune_list)
        print(fortune_list[0])
        print(fortune_list[1])
        print(fortune_list[2])

        # 運勢用の星を算出してリストに格納
        print('--- 運勢の星を決定 ---')
        star_result_list = random.choices(star_list, k=3, weights=[4, 15, 50, 25, 4, 2])
        star_result_list.sort(reverse=True)
        print(star_result_list)
        print(star_result_list[0])
        print(star_result_list[1])
        print(star_result_list[2])

        # ラッキーアイテム占い処理
        print('--- ラッキーアイテムを決定 ---')
        lucky_num = random.randint(0,len(lucky_list)-1)
        lucky_value = lucky_list[lucky_num]
        print(lucky_value)

        print('===== 結果を送信します =====')
        # メッセージ送信
        embed = discord.Embed(title='もだねちゃん占い', description=f'{ctx.author.display_name}さんの今日の運勢だよ！', color=0xffd6e9)
        embed.add_field(name='ㅤ\n' + fortune_list[0], value=star_result_list[0])
        embed.add_field(name='ㅤ\n' + fortune_list[1], value=star_result_list[1])
        embed.add_field(name='ㅤ\n' + fortune_list[2], value=star_result_list[2])
        embed.add_field(name='ㅤ\nラッキーアイテム', value=lucky_value)

        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        if '⭐️⭐️⭐️⭐️⭐️⭐️' in star_result_list:
            await ctx.send(f'わっ！★6 の運勢があるよ！\n今日はとっても良い日になりそうだね🌸\n\nまたねーっ！')
        else:
            await ctx.send(f'結果はどうだった？またねー！')

        # DB uranai_played_tb へユーザーIDを格納する
        print('--- DB へ ユーザーID を格納 ---')
        user_id = ctx.author.id
        psql.run_query('cogs/sql/uranai/insert_user_id.sql', {'user_id': user_id})
        print('--- DB へ格納完了 ---')

        print('===== もだねちゃん占いを終了します =====')


def setup(bot):
    bot.add_cog(Uranai(bot))