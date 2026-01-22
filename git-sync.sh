#!/bin/bash
cd ~/ && git pull origin main
# This line automatically applies any changes found in the k8s folder
kubectl apply -k ~/k8s/base/
