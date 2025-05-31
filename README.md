
<!-- omit in toc -->
# ![おしゃべりぼっと！もだねちゃん](images/kv.png)

<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

<!-- omit in toc -->
## 目次

- [1. もだねちゃんとは？](#1-もだねちゃんとは)
- [2. Bot の導入方法・使い方](#2-bot-の導入方法使い方)
- [3. 構築](#3-構築)
    - [3.1. 必要なもの](#31-必要なもの)
    - [3.2. 実行手順](#32-実行手順)
- [4. 使用ソフトウェア](#4-使用ソフトウェア)
- [5. ライセンス](#5-ライセンス)
- [6. 参考文献](#6-参考文献)
    - [6.1. Discord Bot](#61-discord-bot)
    - [6.2. Docker](#62-docker)
- [7. 謝辞](#7-謝辞)

## 1. もだねちゃんとは？

もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる読み上げ Bot です。  
テキストチャンネルに投稿された文章をボイスチャンネルで読み上げてくれます。

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由でお声を出しづらい方でも、お友達と楽しく会話することができます。

働いている様子はこちら！※Youtube へ移動します

[<img src="images/movie_thumbnail.jpg" alt="読み上げBot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

## 2. Bot の導入方法・使い方

[📙お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙お仕事内容ガイドブック) をご覧ください。  
※ ご協力いただいている少数のサーバーにて試験運用中のため、現在 Bot の一般公開は行っておりません。

## 3. 構築

環境を構築して Bot を稼働させる場合は以下の手順で行います。  
実行に関しては自己責任でお願いします。

### 3.1. 必要なもの

- Docker および Docker Compose が実行可能な環境（手順は WSL2 上での実行）
- 約 850 MB 以上の空き容量（下記内訳）
    - `discordbot-mdn_main` イメージ: 546 MB
    - `postgres` イメージ: 217 MB
    - `discordbot-mdn_db-volume` ボリューム: 50 MB ～
- Discord Bot のトークン

### 3.2. 実行手順

1. リポジトリをクローン。

    ```shell
    $ git clone https://github.com/kenkenpa198/discordbot-mdn.git
    ```

2. リポジトリのルートディレクトリへ移動。

    ```shell
    $ cd discordbot-mdn
    ```

3. `.env` ファイルを作成し、パスワードとトークンを記述。

    ```shell
    $ cp .env.sample .env
    $ vim .env
    ```

    ```properties
    # PostgreSQL イメージ用の環境変数
    POSTGRES_USER=discordbot-mdn
    POSTGRES_PASSWORD=__ENTER_PG_PASSWORD_HERE__ # 好みのパスワードを記述
    POSTGRES_DB=discordbot-mdn-db

    # PostgreSQL の接続用 URL
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

    # bot のトークン
    BOT_TOKEN=__ENTER_BOT_TOKEN_HERE__           # Discord Bot のアクセストークンを記述
    ```

4. `docker-compose` コマンドでコンテナを立ち上げ。

    ```shell
    $ docker-compose up -d
    Creating network "discordbot-mdn_default" with the default driver
    ...
    Creating discordbot-mdn_db_1   ... done
    Creating discordbot-mdn_main_1 ... done
    ```

5. `main_1` `db_1` コンテナが起動していることを確認。

    ```shell
    $ docker ps
    CONTAINER ID   IMAGE                      ...   NAMES
    aaaaaaaaaaaa   discordbot-mdn_main        ...   discordbot-mdn_main_1
    bbbbbbbbbbbb   postgres:14.5-alpine3.16   ...   discordbot-mdn_db_1
    ```

6. コンテナのログを確認。`main_1` 側のログへ `Hello, World!` と表示されていれば OK 。

    ```shell
    $ docker-compose logs -f
    main_1  | ====================================
    main_1  |            discordbot-mdn
    main_1  | ====================================
    main_1  | 2022-11-08 21:55:43.408075
    main_1  | python 3.10.6
    main_1  | discord.py 2.5.2
    main_1  | 2022-11-08 21:55:43,409 [ INFO ] Bot を起動
    ...
    main_1  | 2022-11-08 21:55:47,198 [ INFO ] Bot ログイン後の処理を完了
    main_1  | 2022-11-08 21:55:47,198 [ INFO ] Hello, World!
    ```

7. Bot を招待したサーバーで実行確認。  
参考: [📙お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙お仕事内容ガイドブック)

## 4. 使用ソフトウェア

- [Rapptz/discord.py](https://github.com/Rapptz/discord.py)  
Copyright (c) 2015-present Rapptz  
License: [https://github.com/Rapptz/discord.py/blob/master/LICENSE](https://github.com/Rapptz/discord.py/blob/master/LICENSE)
- [zomysan/alkana.py](https://github.com/zomysan/alkana.py)  
License: [https://github.com/zomysan/alkana.py/blob/master/LICENSE](https://github.com/zomysan/alkana.py/blob/master/LICENSE)
- [Opus](https://opus-codec.org)  
License: [https://opus-codec.org/license/](https://opus-codec.org/license/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)  
License: [https://www.psycopg.org/docs/license.html](https://www.psycopg.org/docs/license.html)
- [emptypage/open_jtalk:22.04-1.11](https://hub.docker.com/layers/emptypage/open_jtalk/22.04-1.11/images/sha256-16f1ee83f32f019c5a44eb14fd557fa36a3ff00b89e064c65e47d81f193c9601?context=explore)  
Copyright © 2020 Masaaki Shibata  
License: [https://bitbucket.org/emptypage/open_jtalk-docker/src/master/LICENSE](https://bitbucket.org/emptypage/open_jtalk-docker/src/master/LICENSE)
- [postgres:14.5-alpine3.16](https://hub.docker.com/layers/library/postgres/14.5-alpine3.16/images/sha256-db802f226b620fc0b8adbeca7859eb203c8d3c9ce5d84870fadee05dea8f50ce?context=explore)  
License: [https://www.postgresql.org/about/licence/](https://www.postgresql.org/about/licence/)

## 5. ライセンス

[GNU General Public License v2.0](LICENSE)

## 6. 参考文献

### 6.1. Discord Bot

- [discord.py へようこそ。](https://discordpy.readthedocs.io/ja/latest/#)
- [Pythonで実用Discord Bot(discordpy解説) - Qiita](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [DiscordBot開発実践入門 - cod-sushi - BOOTH](https://cod-sushi.booth.pm/items/2391223)
- [DiscordBot運営実践入門 - cod-sushi - BOOTH](https://booth.pm/ja/items/1533599)
- [psycopg2 メモ - Qiita](https://qiita.com/hitsumabushi845/items/a421aff1bcd7999f7e40)
- [Pythonのデフォルト引数で[]とか{}を使うべきではないという話 | Cosnomi Blog](https://blog.cosnomi.com/posts/1471/)
- [Logging HOWTO — Python 3.11.0b5 ドキュメント](https://docs.python.org/ja/3/howto/logging.html)

### 6.2. Docker

- [社内のDockerfileのベストプラクティスを公開します│FORCIA CUBE│フォルシア株式会社](https://www.forcia.com/blog/002273.html)
- [Dockerイメージのレイヤの考え方とイメージの軽量化について - ネットワークエンジニアを目指して](https://www.itbook.info/network/docker02.html)
- [docker-composeでサービス運用しているなら設定しておきたいログローテート - Qiita](https://qiita.com/harachan/items/fa306cc1e6b497e592c3)
- [【Docker】PostgreSQLの起動時に初期データをセットアップ | 素人エンジニアの苦悩](https://amateur-engineer.com/docker-compose-postgresql/)
- [postgresql - Error when running psql command in /docker-entrypoint-initdb.d/db_init.sh (psql: could not connect to server: Connection refused) - Stack Overflow](https://stackoverflow.com/questions/51659972/error-when-running-psql-command-in-docker-entrypoint-initdb-d-db-init-sh-psql)
- [Postgres公式Dockerイメージのパスワードの扱いについて](https://zenn.dev/dowanna6/articles/6cc31869346a06)

## 7. 謝辞

しばたまさあきさん、捕食域の皆さんに相談やテストなどでご協力いただきました。  
ありがとうございました！
