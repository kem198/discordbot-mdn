FROM emptypage/open_jtalk:22.04-1.11

ENV DEBIAN_FRONTEND=noninteractive

COPY discordbot-mdn/ /discordbot-mdn/
COPY requirements.txt /requirements.txt

RUN set -x && \
    # apt install
    apt-get update -y && \
    apt-get install -y --no-install-recommends libopus-dev python3-pip tzdata && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
    # pip install
    pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt && \
    # Add new user (to prevent running as root)
    useradd myuser && \
    # Set ownership and permissions for the directory
    chown -R myuser /discordbot-mdn

USER myuser

WORKDIR /discordbot-mdn

CMD python3 -u bot.py
