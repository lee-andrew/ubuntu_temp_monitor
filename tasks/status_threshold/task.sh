#!/bin/bash
set -e

pushd states
  result=$(cat $readings)
popd
pushd git_monitor/state
  if [ $result -gt $threshold ]; then
    if [ ! -s $readings  ]; then
      echo $result > $readings
    fi
  else
    if [ -s $readings ]; then
      echo "" > $readings
    fi
  fi
  if [[ -n $(git status --porcelain) ]]; then
    git config --global user.name $git_user
    git config --global user.email $git_email
    git add .
    git commit -m "state change $readings"
  fi
popd
shopt -s dotglob
cp -r git_monitor/* output