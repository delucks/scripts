from flask import Flask, request, render_template
import logging
import platform
import multiprocessing
app = Flask(__name__)

'''
functionality
    statistics about the machine it's running on
    ability to issue arbitrary shell commands and display the output
    generalized statistics like ping to a site, your server load, etc
    fuzzy search of bookmarks
design
    simple white or grey background, colorful graphs
    some kind of a JS graphing library for the frontend
    read most of the info directly off proc so it's fast
poll proc every few seconds, put information into a DB w/ timestamp
    frontend is a separate thread/process that renders the app
    queries the DB through JS for information
'''

'''
utility functions
'''

def gen_nonempty(iterative):
    for item in iterative:
        if item.strip() != '':
            yield item

# read /proc/cpuinfo, parse the data into a dict
def proc_cpuinfo():
    with open('/proc/cpuinfo', 'r') as info:
        information = {'proc_count': 0}
        for entry in gen_nonempty(info.readlines()):
            sep = [i.strip() for i in entry.split(':')]
            cat = sep[0]
            datum = sep[1]
            if cat == 'processor':
                information['proc_count'] += 1
            elif cat == 'model name':
                information['model'] = datum
            elif cat == 'BogoMIPS':
                information['speed'] = datum
            elif cat == 'Hardware':
                information['name'] = datum
    return information

# read loadavg from proc
def proc_load():
    with open('/proc/loadavg', 'r') as info:
        data = info.read().split()
        return {1: data[0], 5: data[1], 15: data[2]}

# read some memory stats from proc. all numbers are in kilobytes
def proc_mem():
    with open('/proc/meminfo', 'r') as info:
        information = {}
        for memstat in gen_nonempty(info.readlines()):
            sep = [i.strip() for i in memstat.split(':')]
            cat = sep[0]
            datum = sep[1].rstrip(' kB')
            if cat == 'MemTotal':
                information['total'] = datum
            elif cat == 'MemFree':
                information['free'] = datum
            elif cat == 'Buffers':
                information['buffers'] = datum
            elif cat == 'Cached':
                information['cache'] = datum
            elif cat == 'SwapCached':
                information['swap'] = datum
            elif cat == 'Active':
                information['active'] = datum
    return information

'''
application logic
'''

@app.route('/')
def render_dashboard():
    pass

if (__name__ == '__main__'):
    app_args = {
            'host': '127.0.0.1',
            'debug': True
            }
    # so far this works, but 
    # TODO: figure out why reloading the file kills the subprocess
    # foobar
    #app_proc = multiprocessing.Process(target=app.run, kwargs=app_args)
    #app_proc.start()
    app.run(host='127.0.0.1', debug=True) # this blocks
    print proc_mem()
