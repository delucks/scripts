scheme=$(cd ~/dotfiles/colors/ && ls *.colors | dmenu)
test -h ~/.colors && unlink ~/.colors
test -h ~/.colorsX && unlink ~/.colorsX
echo "$scheme"
ln -s ~/dotfiles/colors/$scheme ~/.colors
scheme+="X"
echo "$scheme"
ln -s ~/dotfiles/colors/$scheme ~/.colorsX
xrdb -merge ~/.Xresources
