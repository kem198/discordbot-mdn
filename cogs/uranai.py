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
    '⚽️ スポーツ運'
]

# 運勢結果リスト
star_list = [
    '★',
    '★★',
    '★★',
    '★★',
    '★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★★'
]

# ラッキーアイテムリスト
lucky_list = [
    '🍎 赤色',
    '🎇 橙色',
    '🍋 黄色',
    '📗 緑色',
    '🐳 青色',
    '🔮 紫色',
    ':black_cat: 黒色',
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
    '🌌 夜空'
    ]

# 遊んだ人リストを定義
played_list = []

# played_list の中身を削除する関数を定義
def delete_played_tb():
    query = psql.get_query('cogs/sql/uranai/delete_id.sql')
    with psql.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
    played_list.clear()
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

        async with ctx.channel.typing():
            # DB uranai_played_tb にユーザー ID があるか判定
            # TODO: クエリの実行まで関数化したい（引数の複数指定がうまくいかない）
            # TODO: ここの読込で1秒程度待ち時間が発生してしまう
            print('--- DB の ユーザーID をチェック ---')
            query = psql.get_query('cogs/sql/uranai/select_id.sql')
            with psql.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    # 取得した ID のリストを作成
                    played_list.clear() # リストを一旦クリアする
                    for row in cur:
                        played_list.append(str(row[0])) # 取得したレコードをリストへ変換
                    print(played_list)
                conn.commit()

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

        print(fortune_list)
        for i in range(3):
            print('運勢 ' + str(i) + '：' + fortune_list[i])

        star_num_list = []
        for i in range(3):
            star_num_list.append(random.randint(0,len(star_list)-1))
        print('ソート前：' + str(star_num_list))
        star_num_list.sort(reverse=True)
        print('ソート後：' + str(star_num_list))

        # ラッキーアイテム占い処理
        print('--- ラッキーアイテムを決定 ---')
        lucky_num = random.randint(0,len(lucky_list)-1)
        lucky_value = lucky_list[lucky_num]
        print('ラッキーアイテム：' + lucky_value)

        print('===== 結果を送信します =====')
        # メッセージ送信
        embed = discord.Embed(title='もだねちゃん占い', description=f'{ctx.author.display_name}さんの今日の運勢だよ！', color=0xffd6e9)
        embed.add_field(name='ㅤ\n' + fortune_list[0], value=star_list[star_num_list[0]])
        embed.add_field(name='ㅤ\n' + fortune_list[1], value=star_list[star_num_list[1]])
        embed.add_field(name='ㅤ\n' + fortune_list[2], value=star_list[star_num_list[2]])
        embed.add_field(name='ㅤ\nラッキーアイテム', value=lucky_value)

        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        await ctx.send(f'結果はどうだった？またねー！')

        # DB uranai_played_tb へユーザーIDを格納する
        print('--- DB へ ユーザーID を格納 ---')
        query = psql.get_query('cogs/sql/uranai/insert_id.sql')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {'user_id': (str(ctx.author.id))})
            conn.commit()
        print('--- DB へ格納完了 ---')

        print('===== もだねちゃん占いを終了します =====')


def setup(bot):
    bot.add_cog(Uranai(bot))