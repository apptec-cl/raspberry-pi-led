#!/bin/bash
cmd=$1
color=$2

start_function(){
  echo "Changing led color.."
  python lib/ledrgb.py -c $color -e prod
}

stop_function(){
	kill -9 $(pgrep -f 'ledrgb.py')
}

case "$cmd" in
  start)
    stop_function
    start_function
    ;;
  stop)
    stop_function
    ;;
  restart)
    stop_function && start_function;
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart} color"
esac
