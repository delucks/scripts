uptime | awk '{print $1,$8<$9 ? "LOAD▲":"LOAD▼"}'
