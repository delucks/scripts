#!/usr/bin/env python2

# # # # # # # # # # # # # # # #
# Wallpaper Resolution Sorter #
# 	  by jluck@udel.edu		  #
# # # # # # # # # # # # # # # #

# Depends on python packages: Image, argparse, os, platform
# Depends on unix packages: xrandr, X 

try:
	import Image, argparse, os, platform
except ImportError:
	print "Not all required dependencies are installed, check the README"
	exit(2)

# Argument Parsing
parser = argparse.ArgumentParser(description="Gets the size of an image, and sorts it based on the user's screen resolution", add_help=True)
parser.add_argument('filepath', help='Provide path or file to analyze')
parser.add_argument('-l', '--local', action="store_true", help="Move all images less than screen resolution to local directory called lowres")
parser.add_argument('-a', '--absolute', action="store_true", help="Move to the absolute directory ~/pictures/wallpaper/lowres/")
parser.add_argument('--abspath', help='Path for low-res images to go')
parser.add_argument('-m', '--matching', action="store_true", help="Show all images less than screen resolution, take no action")
parser.add_argument('-A', '--all', action="store_true", help="Show all images in the directory, take no action, don't supress debug output")

args = parser.parse_args()

# Attempt to detect screen resolution from your OS, and if not, default to 1920x1080
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
		print "Are you sure this is a Windows system?"
		exit(2)
	screen_width = int(GetSystemMetrics (0))
	screen_height = int(GetSystemMetrics (1))
elif (platform.system() == "Darwin"):
	# Get a real unix box.
	try:
		import AppKit
	except ImportError:
		print "Are you sure this is a Mac system?"
		exit(2)
	screen = AppKit.NSScreen.screens()[0]
	screen_width = screen.frame().size.width
	screen_height = screen.frame().size.height
else:
	print "I'm proud of you."
	screen_width = 1920
	screen_height = 1080

# Grab the resolution of the picture, and pass that on to whatever options the user chose
def get_resolution(filename):
	try:
		image = Image.open(filename)
	except IOError:
		if args.all:
			print "%s is not a valid image" % (filename)
		return
	width = image.size[0]
	height = image.size[1]

	if (width < screen_width or height < screen_height):
		if (args.local or args.absolute):
			move_lowres(filename)
		elif (args.matching or args.all):
			print '%s %i %i' % (filename, width, height)
	elif args.all:
		print '%s %i %i' % (filename, width, height)

# Create the specified lowres dir, and move stuff there
def move_lowres(filename):
	if args.absolute:
		if args.abspath:
			lowpath = args.abspath
		else:
			lowpath = "/home/jamie/pictures/wallpaper/lowres/"
	else:
		lowpath = os.path.join(args.filepath, 'lowres')
	if not os.path.exists(lowpath):
		os.makedirs(lowpath)
	newname = os.path.join(lowpath, os.path.basename(filename))
	os.rename(filename, newname)

# Recursively follow directories and look for images
def select_files(path):
	if os.path.isfile(path):
		get_resolution(path)
	elif os.path.isdir(path):
		for f in os.listdir(path):
			fullpath = os.path.join(path, f)
			select_files(fullpath)

def main():
	if not args.filepath:
		print 'Needs a file or directory to analyze'
		return
	select_files(args.filepath)

if __name__=="__main__":
	main()
