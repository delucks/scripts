uptime | awk '{if ($8 < $9) {print "LOAD\xe2\x96\xb2";} else {print "LOAD\xe2\x96\xbc";}}'
