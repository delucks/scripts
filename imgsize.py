#!/usr/bin/env python2

######################
# image size sorter v2
# delucks

try:
  from PIL import Image
  import argparse, os
  if args.auto:
    import platform
except ImportError:
  print "Not all required dependencies are installed"
  exit(2)

MODES = ["lt","le","gt","ge","eq"]
OUTPUT = ["csv","tsv","path","res"]

# Argument Parsing
parser = argparse.ArgumentParser(description="Image size toolkit", add_help=True)
parser.add_argument('filepath', help='Provide path to analyze')
parser.add_argument('--auto', action="store_true", help="Detect screen resolution")
parser.add_argument('-x', '--width', help="Width of outputted images")
parser.add_argument('-y', '--height', help="Height of outputted images")
parser.add_argument('--debug', action="store_true", help="Enable debugging output")
parser.add_argument('mode', help='Execution mode', choices=MODES)
args = parser.parse_args()

def dp(string):
  if args.debug:
    print string

screen_width = 1920
screen_height = 1080

if args.auto:
  if (platform.system() == "Linux" or platform.system() == "FreeBSD"):
    # Get the resolution from the active X display using xrandr
    screen = os.popen("xrandr -q -d :0").readlines()[0]
    screen_width = int(screen.split()[7])
    screen_height = int(screen.split()[9][:-1])
  elif (platform.system() == "Windows"):
    # Get the resolution from win32api
    try:
      from win32api import GetSystemMetrics
    except ImportError:
      dp("Are you sure this is a Windows system?")
      exit(2)
    screen_width = int(GetSystemMetrics (0))
    screen_height = int(GetSystemMetrics (1))
  elif (platform.system() == "Darwin"):
    # Get a real unix box.
    try:
      import AppKit
    except ImportError:
      dp("Are you sure this is a Mac system?")
      exit(2)
    screen = AppKit.NSScreen.screens()[0]
    screen_width = screen.frame().size.width
    screen_height = screen.frame().size.height
  else:
    dp("I like your platform. Where'd you get it, and how is it running python?")

# Take an opened image and return comparison bool of width/height
def chk_d(image,target,wh):
  if (wh == "width"):
    actual = image.size[0]
  else:
    actual = image.size[1]

  if (args.mode == 'le'):
    return (actual <= target)
  elif (args.mode == 'lt'):
    return (actual < target)
  elif (args.mode == 'ge'):
    return (actual >= target)
  elif (args.mode == 'gt'):
    return (actual > target)
  else:
    return (actual == target) # Default to equals

# Recursively follow directories and look for images
def select_files(path):
  final = []
  if os.path.isfile(path):
    try:
      image = Image.open(path)
    except IOError:
      dp("%s is not a valid image" % (path))
      return
    if args.auto:
        if (chk_d(image,screen_height,"height") and chk_d(image,screen_width,"width")):
          final.append(path)
    elif args.width:
      if args.height:
        if (chk_d(image,args.height,"height") and chk_d(image,args.width,"width")):
          final.append(path)
      else:
        if (chk_d(image,args.width,"width")):
          final.append(path)
    elif args.height:
        if (chk_d(image,args.height,"height")):
          final.append(path)
  elif os.path.isdir(path):
    for f in os.listdir(path):
      fullpath = os.path.join(path, f)
      files = select_files(fullpath)
      if files is not None:
        final = final + select_files(fullpath)
  return final

def main():
  if not args.filepath:
    print 'Needs a file or directory to analyze'
    return
  files = select_files(args.filepath)
  for item in files:
    print item

if __name__=="__main__":
  main()
