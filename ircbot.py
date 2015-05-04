import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

'''
I'm gonna throw all the stupid commands I don't want to leave IRC for here
'''
class UtilBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nick, server, port):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        self.channel = channel
        self.nick = nick

    '''
    Actual Utility Functions
    '''
    def http_title(self, link):
        import urllib2
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(urllib2.urlopen(link).read())
        return soup.title.text

    '''
    IRC Handler Functions
    '''
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
        elif (e.arguments[0].startswith('!')):
            self.handle_command(e.arguments[0])

    def handle_command(self, e, cmd):
        nick = e.source.nick
        self.connection.notice(self.channel, '{n} tried to issue {c}'.format(n=nick,c=cmd))

    def handle_message(self, e, msg):
        nick = e.source.nick
        self.connection.notice(self.channel, '{n} is talking to me'.format(n=nick))

def main():
    import argparse
    p = argparse.ArgumentParser(description='IRC bot which does utility functions')
    p.add_argument('server', help='the server you want the bot to connect to')
    p.add_argument('channel', help='the channel the bot should join on the server')
    p.add_argument('-p', '--port', help='specify an alternate port (default 6667)', type=int, default=6667)
    p.add_argument('-n', '--nick', help='specify an alternate nickname (default utilbot)', default='utilbot')
    args = p.parse_args()
    bot = UtilBot(args.channel, args.nick, args.server, args.port)
    bot.start()

if __name__ == '__main__':
    main()
