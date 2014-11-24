scheme=$(cd ~/dev/wp/colors/ && ls *.colors | dmenu)
test -h ~/.colors && unlink ~/.colors
test -h ~/.colorsX && unlink ~/.colorsX
echo "$scheme"
ln -s ~/dev/wp/colors/$scheme ~/.colors
scheme+="X"
echo "$scheme"
ln -s ~/dev/wp/colors/$scheme ~/.colorsX
xrdb -merge ~/.Xresources
