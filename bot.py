'''
Copyright 2018-2020 Evan Markowitz (ejm)
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import configparser
import obswebsocket, obswebsocket.requests

def parse_badges(badges):
    parsed = {}
    for badge_raw in badges.split(","):
        badge, version = badge_raw.split("/")
        parsed[badge] = version
    return parsed

def get_mod_from_tags(tags):
    for tag in tags:
        if tag["key"] == "badges":
            badges = parse_badges(tag["value"])
            if "moderator" in badges or "broadadcaster" in badges or "admin" in badges:
                return True
            return False

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token_, channel, ws, commands):
        self.token_ = token_
        self.channel = '#' + channel
        self.commands = commands
        self.ws = ws

        self.ws.connect()
        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [(server, port, token_)],
            username,
            username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd_ = e.arguments[0].split(' ')[0][1:]
            self.do_command(e, cmd_)
        return

    def do_command(self, e, cmd_):
        c = self.connection
        chan = self.channels[e.target]
        if get_mod_from_tags(e.tags):
            if cmd_ in self.commands:
                name = self.commands[cmd_]
                print("Changing scene to {}".format(name))
                self.ws.call(obswebsocket.requests.SetCurrentScene(name))

def main():
    config = configparser.ConfigParser()
    config.read("config.cfg")
    
    obs = config["obs"]
    ws = obswebsocket.obsws(obs["host"], int(obs["port"]), obs["password"])
    
    twitch = config["twitch"]
    commands = config["scenes"]
    try:
        bot = TwitchBot(
            twitch["username"],
            twitch["token"],
            twitch["channel"],
            ws,
            commands)
        bot.start()
    except KeyboardInterrupt:
        print("Ctrl-C")
        bot.ws.disconnect()
        bot.disconnect()
        sys.exit(0)
if __name__ == "__main__":
    main()
