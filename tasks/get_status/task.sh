#!/bin/bash
set -e

echo "Securing connecting..."

results=$(sshpass -p $ssh_pass ssh -o StrictHostKeyChecking=no  $ssh_user@$ssh_host sensors)
case_fan1=$(echo "$results" | grep fan2 | tr -s ' ' | cut -d' ' -f2)
case_fan2=$(echo "$results" | grep fan5 | tr -s ' ' | cut -d' ' -f2) 
cpu_fan=$(echo "$results" | grep fan4 | tr -s ' ' | cut -d' ' -f2)
gpu_temp=$(echo "$results" | grep temp1 | tr -s ' ' | cut -d' ' -f2 | cut -d'.' -f1 | cut -d'+' -f2)
sys_temp=$(echo "$results" | grep SYSTIN | tr -s ' ' | cut -d' ' -f2 | cut -d'.' -f1 | cut -d'+' -f2)
cpu_temp=$(echo "$results" | grep CPUTIN | tr -s ' ' | cut -d' ' -f2 | cut -d'.' -f1 | cut -d'+' -f2)
psu_temp=$(echo "$results" | grep AUXTIN0 | tr -s ' ' | cut -d' ' -f2 | cut -d'.' -f1 | cut -d'+' -f2)

echo "Case Fan #1: $case_fan1"
echo "Case Fan #2: $case_fan2"
echo "CPU Fan: $cpu_fan"
echo "GPU Temp: $gpu_temp"
echo "SYS Temp: $sys_temp"
echo "CPU Temp: $cpu_temp"
echo "PSU Temp: $psu_temp"

# check for empty values

pushd states
  echo $cpu_temp > cpu_temp
  echo $case_fan1 > case_fan1
  echo $case_fan2 > case_fan2
  echo $cpu_fan > cpu_temp
  echo $gpu_temp > gpu_temp
  echo $sys_temp > sys_temp
  echo $psu_temp > psu_temp
popd