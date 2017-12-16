#!/bin/sh
set -ex

cd git_monitor_trigger/state
  a=$(cat $bot_type)
  if [ "$a" == "" ]; then
    message="$bot_type has gone below the threshold"
  else
    message="$bot_type has gone above the threshold at $a"
  fi
cd ..
curl $discord_webhook -d "{\"content\":\"$message\"}"