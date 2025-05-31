FROM emptypage/open_jtalk:22.04-1.11

# No waiting tzdata inputs
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /requirements.txt
RUN set -x && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends libopus-dev python3-pip tzdata && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt

COPY discordbot-mdn/ /discordbot-mdn/
RUN mkdir -p /discordbot-mdn && \
    useradd myuser && \
    chown -R myuser /discordbot-mdn

USER myuser
WORKDIR /discordbot-mdn

CMD ["python3", "-u", "bot.py"]
