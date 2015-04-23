import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class UtilBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nick, server, port):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        self.channel = channel
        self.nick = nick

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')
    
    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        if (self.nick + ':' in e.arguments[0]):
            a = e.arguments[0].split(':', 1)
            if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
                self.handle_message(e, a[1].strip())
        else if (e.arguments[0].startswith('!')):
            self.handle_command(e.arguments[0])

    def handle_command(self, e, cmd):
        nick = e.source.nick
        self.connection.notice(self.channel, '{n} tried to issue {c}'.format(n=nick,c=cmd))

    def handle_message(self, e, msg):
        nick = e.source.nick
        self.connection.notice(self.channel, '{n} is talking to me'.format(n=nick))

def main():
    import sys
    if len(sys.argv) != 4:
        print('Usage: testbot <server[:port]> <channel> <nickname>')
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print('Error: Erroneous port.')
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = UtilBot(channel, nickname, server, port)
    bot.start()

if __name__ == '__main__':
    main()
