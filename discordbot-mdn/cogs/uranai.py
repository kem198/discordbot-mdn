"""Cog Uranai"""

from datetime import datetime
import logging
import random

from discord.ext import commands
from discord.ext import tasks

from .utils import psql
from .utils import send as sd

class Uranai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 運勢リストの読み込み
        with open('./csv/fortune_list.csv', 'r', encoding='utf-8') as f:
            self.fortune_list = [s.strip() for s in f.readlines()]
        # print(self.fortune_list)

        # 運勢の星リストの初期化
        self.star_list = ['★', '★★', '★★★', '★★★★', '★★★★★', '⭐️⭐️⭐️⭐️⭐️⭐️']

        # ラッキーアイテムリストの読み込み
        with open('./csv/lucky_list.csv', 'r', encoding='utf-8') as f:
            self.lucky_list = [s.strip() for s in f.readlines()]
        # print(self.lucky_list)

    @tasks.loop(seconds=60)
    async def loop():
        """
        毎日0時にレコードを削除する
        """
        now = datetime.now().strftime('%H:%M')
        if now == '00:00':
            logging.info('played_fortune_users テーブルのレコードを削除')
            psql.execute_query('./sql/uranai/delete_user_id.sql')
    # ループ処理を実行
    loop.start()

    # 占いコマンド
    # @commands.cooldown で 15 秒に 1 回のみ実行可能としている
    # Ref:
    # https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.cooldown
    # https://qiita.com/daima3629/items/aed5c128fcbd258c2e38
    @commands.hybrid_command(
        description='🔮 今日の運勢を占うよ',
        aliases=['u']
    )
    @commands.cooldown(1, 15.0)
    async def uranai(self, ctx):
        """
        占いコマンド
        """
        logging.info('占いコマンドを受付')

        # played_fortune_users テーブルにユーザー ID があるか判定
        async with ctx.channel.typing():
            logging.info('played_fortune_users テーブルのユーザー ID をチェック')
            played_list = []
            played_list = psql.execute_query_fetch_list('./sql/uranai/select_user_id.sql')

        # played_list にユーザーIDがあるか判定
        if str(ctx.author.id) in played_list:
            logging.info('遊んだ人リストに ID があるため中断')
            await sd.send_uranai_played(ctx)
            logging.info('もだねちゃん占いを終了')
            return

        # 運勢占い処理
        random.shuffle(self.fortune_list)
        logging.info('運勢 3つを決定: %s, %s, %s', self.fortune_list[0], self.fortune_list[1], self.fortune_list[2])

        # 運勢用の星を算出してリストに格納
        star_result_list = random.choices(self.star_list, k=3, weights=[4, 15, 50, 25, 4, 2])
        star_result_list.sort(reverse=True)
        logging.info('運勢の星を決定: %s, %s, %s', star_result_list[0], star_result_list[1], star_result_list[2])

        # ラッキーアイテム占い処理
        lucky_num = random.randint(0, len(self.lucky_list)-1)
        lucky_value = self.lucky_list[lucky_num]
        logging.info('ラッキーアイテムを決定: %s', lucky_value)

        logging.info('結果を送信')
        # メッセージ送信
        await sd.send_uranai_result(ctx, self.fortune_list, star_result_list, lucky_value)

        # played_fortune_users テーブルへユーザーIDを格納する
        logging.info('played_fortune_users テーブルへ ユーザーID を格納')
        user_id = ctx.author.id
        psql.execute_query('./sql/uranai/insert_user_id.sql', {'user_id': user_id})

        logging.info('もだねちゃん占いを終了')

    # CommandOnCooldown エラーが発生した時メッセージを返す
    # https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.cooldown
    # https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html?highlight=commands%20cog#discord.ext.commands.Cog.listener
    # https://qiita.com/daima3629/items/aed5c128fcbd258c2e38
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            return await sd.send_on_command_error_cooldown(ctx)

async def setup(bot):
    await bot.add_cog(Uranai(bot))
