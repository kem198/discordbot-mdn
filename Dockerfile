# ビルド
FROM emptypage/open_jtalk:22.04-1.11

# tzdata の入力を待たない
ENV DEBIAN_FRONTEND=noninteractive

# 環境構築
RUN set -x && \
    # apt インストール
    apt-get update -y && \
    apt-get install -y --no-install-recommends libopus-dev python3-pip tzdata && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
    # pip インストール
    pip3 install --upgrade pip && \
    pip3 install alkana==0.0.3 discord.py==2.2.2 jtalkbot==0.6.1.3 psycopg2-binary==2.9.4 && \
    # bot 用のディレクトリを作成
    mkdir /discordbot-mdn && \
    # 新規ユーザーを作成（root での稼働を防止するため）
    useradd myuser && \
    # ディレクトリへ所有権と権限を設定
    chown -R myuser /discordbot-mdn

# bot のソースコードをコンテナ内へ複製
COPY /discordbot-mdn/ /discordbot-mdn/

# ユーザーを切り替え
USER myuser

# 作業ディレクトリを指定
WORKDIR /discordbot-mdn

# コンテナ稼働時の実行コマンドを定義
CMD /bin/sh -c "python3 -u bot.py"
