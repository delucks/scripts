import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class UtilBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nick, server, port):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        #super(UtilBot,self).__init__(self, [(server, port)], nick, nick)
        self.channel = channel
        self.nick = nick

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
    
    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.handle_message(e, a[1].strip())

    def handle_message(self, e, msg):
        nick = e.source.nick
        c = self.connection
        c.notice(self.channel, nick)
        #if cmd == "smile":
        #    c.notice(self.channel, smiles[0])
        #elif cmd == "smile1":
        #    c.notice(self.channel, smiles[1])
        #elif cmd == "smile2":
        #    c.notice(self.channel, smiles[2])
        #elif cmd == "smile3":
        #    c.notice(self.channel, smiles[3])
        #elif cmd == "fail":
        #    for failline in failwhale:
        #        c.notice (self.channel, failline)
        #elif cmd == "commands":
        #    c.notice(nick, "smile, smile1, smile2, smile3, fail")
        #else:
        #    c.notice(self.channel, random.choice(smiles))

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = UtilBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
