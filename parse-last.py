#!/usr/bin/env python2
'''
Parse the output of `last` into a summary or munge it into a different format.
No arguments defaults to `./parse_last.py success --format summary`.

(delucks - 15/11/2015)
'''

# parses each line of the last output into a dict
def parse_last(last_gen):
    for line in last_gen:
        if 'wtmp begins' in line or line.strip() == '':
            continue
        sp = line.split()
        l = {}
        l['user'] = sp[0] # heh luser
        if l['user'] == 'reboot':
            continue # not interesting
        l['tty'] = sp[1]
        l['ip'] = sp[-1]
        time_str = ' '.join(sp[2:-1])
        if not 'still logged' in time_str:
            l['time'] = ' '.join(sp[2:-2])
            lng = sp[-2]
            l['length'] = lng[1:-1] if lng.startswith('(') and lng.endswith(')') else lng
            l['loggedin'] = False
        else:
            l['time'] = time_str
            l['loggedin'] = True
        yield l

# grab two unique user'd login records
def get_two(gen):
    cool, user = None, None
    for log_r in gen:
        if not user:
            user = log_r['user']
            cool = log_r
        if log_r['user'] != user:
            return [cool, log_r]

# munge it inot a csv
def csv_line(gen):
    for log_r in gen:
        info = [
            log_r['user'],
            log_r['ip'],
            log_r['tty'],
            log_r['loggedin'],
            log_r['time']
        ]
        if 'length' in log_r.keys():
            info.append(log_r['length'])
        yield ','.join([str(i) for i in info])

def max_key(freq_dict):
    top = (None, 0)
    for item, count in freq_dict.iteritems():
        if count > top[1]:
            top = (item, count)
    return top[0]

# extract some summary data
def user_summary(gen):
    users = {}
    for log_r in gen:
        if log_r['user'] in users:
            users[log_r['user']]['count'] += 1
            if log_r['ip'] not in users[log_r['user']]['ips']:
                users[log_r['user']]['ips'][log_r['ip']] = 1
            else:
                users[log_r['user']]['ips'][log_r['ip']] += 1
        else:
            users[log_r['user']] = {
                    'count': 1,
                    'last': log_r['time'],
                    'current': log_r['loggedin'],
                    'ips': {log_r['ip']: 1},
            }
    return users

def interactive():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('method',
            choices=['stdin', 'fail', 'success'],
            help='where to read last output. fail & success use subprocess, stdin should be from `last -awi`',
            default='success',
            nargs='?'
        )
    p.add_argument('-f', '--format',
            choices=['json', 'summary', 'csv'],
            help='output formatting. defaults to summary',
            default='summary',
            dest='format_type',
        )
    p.add_argument('--describe', help='describe the JSON data format with two examples', action='store_true')
    p.add_argument('--file', dest='outfile', help='dump a file of all filtered records')
    # filters
    p.add_argument('--who', help='filter to logged-in users', action='store_true')
    p.add_argument('--current', help='filter to your user', action='store_true')
    p.add_argument('--users', help='filter to these users (comma-sep)')
    args = p.parse_args()
    # information gathering, will populate the variable 'logins'
    if args.method == 'stdin':
        import sys
        logins = parse_last(sys.stdin)
    else:
        from subprocess import check_output
        if args.method == 'fail':
            cmd = 'sudo lastb -awi'
        else:
            cmd = 'last -awi'
        out = check_output(cmd.split()) # subprocess call
        logins = parse_last(out.splitlines())
    if args.describe:
        from pprint import pprint
        pprint(get_two(logins))
    else:
        # filtering, will populate the variable 'out_data'
        if args.current:
            import getpass
            cuser = getpass.getuser()
            out_data = filter(lambda x: x['user'] == cuser, logins)
        elif args.who:
            out_data = filter(lambda x: x['loggedin'], logins)
        elif args.users:
            usernames = args.users.split(',')
            out_data = filter(lambda x: x['user'] in usernames, logins)
        else:
            out_data = logins
        # outputting, will format the variable 'out_data'
        if args.format_type == 'json':
            import json
            out_text = json.dumps(list(out_data))
        elif args.format_type == 'csv':
            out_csv = csv_line(out_data)
            out_text = ''
            for line in out_csv:
                out_text += line + '\n'
        else: # args.format_type == 'summary':
            from prettytable import PrettyTable
            table = PrettyTable(['User', 'Logins', 'Last', 'Top IP', 'Current?'])
            table.align = 'l'
            users = user_summary(out_data)
            for name, meta in users.iteritems():
                table.add_row([
                        name,
                        meta['count'],
                        meta['last'],
                        max_key(meta['ips']),
                        str(users[name]['current'])
                ])
            out_text = table.get_string(sortby= 'Logins')
        if args.outfile:
            with open(args.outfile, 'w+') as f:
                f.write(out_text.strip())
        else:
            print out_text.strip()

if (__name__=='__main__'):
    interactive()
