#!/bin/bash
set -ex

pushd states
  for i in *; do
    eval "$i=\$(cat $i)"
  done
  states=$(ls)
popd
pushd git_monitor/state
  for i in ${states[*]}; do
    a="${i}_threshold"
    threshold=${!a}
    a="${i}"
    result=${!a}
    readings=$(cat $i)
    if [ $result -gt $threshold ]; then
      if [ "$readings" == "" ]; then
        echo $result > $readings
      fi
    else
      if [ "$readings" != "" ]; then
        echo "" > $readings
      fi
    fi
    if [[ -n $(git status --porcelain) ]]; then
      git config --global user.name $git_user
      git config --global user.email $git_email
      git add .
      git commit -m "state change $readings"
    fi
  done
popd
shopt -s dotglob
cp -r git_monitor/* output
