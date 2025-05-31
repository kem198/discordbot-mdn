# ビルド
FROM emptypage/open_jtalk:22.04-1.11

# tzdata の入力を待たない
ENV DEBIAN_FRONTEND=noninteractive

# bot のソースコードをコンテナ内へ複製
COPY discordbot-mdn/ /discordbot-mdn/
COPY requirements.txt /requirements.txt

# 環境構築
RUN set -x && \
    # apt インストール
    apt-get update -y && \
    apt-get install -y --no-install-recommends libopus-dev python3-pip tzdata && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
    # pip インストール
    pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt && \
    # 新規ユーザーを作成（root での稼働を防止するため）
    useradd myuser && \
    # ディレクトリへ所有権と権限を設定
    chown -R myuser /discordbot-mdn

# ユーザーを切り替え
USER myuser

# 作業ディレクトリを指定
WORKDIR /discordbot-mdn

# コンテナ稼働時の実行コマンドを定義
CMD /bin/sh -c "python3 -u bot.py"
