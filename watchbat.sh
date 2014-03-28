ADDR=$1
HOST=$(uname -n)
BATLVL=$(acpi -b | awk '{print $4}' | tr '{%,}' ' ')
if [[ $BATLVL -lt 60 ]]; then
	echo "Your battery is low! It is currently at $BATLVL percent" | mail -s "Battery on $HOST" $ADDR
fi
