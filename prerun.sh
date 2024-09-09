#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "export BOT_TOKEN=" > bot.env
echo "Venv created, set the bot token on 'bot.env' and run ./start.sh to start bot"