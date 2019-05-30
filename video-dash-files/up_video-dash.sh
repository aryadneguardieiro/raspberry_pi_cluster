#!/bin/bash

kubectl delete namespace nginx-ingress;

kubectl delete ingress video-dash-internal-storage;

kubectl delete endpoints video-dash-internal-storage;

kubectl delete services video-dash-internal-storage;

kubectl delete deployments video-dash-internal-storage;

#kubectl delete pvc nfs;

#kubectl delete pv nfs;

kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/common/ns-and-sa.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/common/default-server-secret.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/common/nginx-config.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/rbac/rbac.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/deployment/nginx-ingress.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/loadbalancer/service/nodeport.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/video-dash-internal-storage-resources.yaml && \
kubectl apply -f ~/raspberry_pi_cluster/video-dash-files/video-dash-internal-storage-ingress.yaml;


echo "fim!! :D"
