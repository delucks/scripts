# a quick hack when I found out about the dbus interface
TOGGLE="dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause"
STOP="dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop"
PREV="dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous"
NEXT="dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next"
TRACK=$(dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | grep -A 1 'xesam:title' | grep variant | sed 's/variant//g' | sed 's/string//g' | sed -e 's/^ *\"//g' -e 's/\" *$//g')
ARTIST=$(dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | grep -A 2 'xesam:artist' | grep string | grep -v xesam | sed 's/string//g' | sed -e 's/^ *\"//g' -e 's/\" *$//g')

case "$1" in
	toggle)
		$TOGGLE
		mpc toggle
		~/scripts/dvol show
		;;
	stop)
		$STOP
		mpc stop
		;;
	prev)
		$PREV
		mpc prev
		~/scripts/dvol show
		;;
	next)
		$NEXT
		mpc next
		~/scripts/dvol show
		;;
	*)
		echo "You goofed"
		exit 1
esac
