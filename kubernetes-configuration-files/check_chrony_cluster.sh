#!/bin/bash

PASSWORD=$1

#INTERNAL_IPS=($(kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'))

INTERNAL_IPS=( "192.168.0.128" )

for IP in "${INTERNAL_IPS[@]}"
do
  echo ""
  echo "Reaching $IP"
  sshpass -p $PASSWORD ssh cloud@$IP chronyc sources || sshpass -p $PASSWORD ssh pi@$IP chronyc sources

  EXIT_STATUS=$?

  if (( $EXIT_STATUS == 127 )); then
    echo ""
    echo "Installing chronyc on $IP"
    sshpass -p $PASSWORD scp ../raspberrypi-configuration-files/chrony_config.sh cloud@IP:~/ || sshpass -p $PASSWORD scp ../raspberrypi-configuration-files/chrony_config.sh pi@IP:~/
    sshpass -p $PASSWORD ssh cloud@IP sh chrony_config.sh || sshpass -p $PASSWORD ssh pi@IP sh chrony_config.sh
  fi

done


