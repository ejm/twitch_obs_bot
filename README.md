# twitch_obs_bot
Control your OBS scenes through Twitch chat!

## Requirements
* Python 3 (tested on 3.5)
* `irc` (`pip install irc`)
* `obs-websocket-py` (`pip install obs-websocket-py`)
* [obs-websocket](https://github.com/Palakis/obs-websocket)

## How to Use
* Move `config.cfg.example` to `config.cfg`
* Edit the values in `config.cfg` to fit your needs
    * **Note**: Scene names are **case sensitive**
    * If you need a token, you can use [this helpful website](https://twitchapps.com/tmi)
* Run `bot.py`
* Type `!cmd` where `cmd` is the scene ID (like `catcam`) in chat
* ????????
* Profit!

## License
This bot is a fork of [this sample](https://github.com/twitchdev/chat-samples/blob/master/python/chatbot.py) provided by Amazon and is licensed under the Apache License.

## Maintenance and Support
This was a one-off project for the OBS Discord server and will likely not be maintained.  Feel free to put things in the Issue tracker, but, I make no guarantees!