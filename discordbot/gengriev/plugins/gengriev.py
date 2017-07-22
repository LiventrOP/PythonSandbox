# General Grievous
from disco.bot import Plugin


class FirstPlugin(Plugin):
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')
