#!/bin/bash
cmd=$1
color=$2

start_function(){
  echo "Changing led color.."
  python ledrgb.py -c $color
}

stop_function(){
	kill $(pgrep -f 'python ledrgb.py')
}

case "$cmd" in
  start)
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