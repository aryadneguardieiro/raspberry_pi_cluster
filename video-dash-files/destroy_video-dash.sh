#!/bin/bash

kubectl delete endpoints video-dash;

kubectl delete services video-dash;

kubectl delete deployments video-dash;

kubectl delete pvc nfs;

kubectl delete pv nfs;

echo "fim!! :D"
