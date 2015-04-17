def get_color(color):
    prefix = '\x1b[3'
    colorcodes = {
            'black':'0m',
            'red':'1m',
            'green':'2m',
            'yellow':'3m',
            'blue':'4m',
            'magenta':'5m',
            'cyan':'6m',
            'white':'7m',
            'reset':'9;49m'}
    return prefix+colorcodes[color]

def clear_screen():
    return '\033[2J\033[;H'
