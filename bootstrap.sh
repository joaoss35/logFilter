#!/bin/bash
set -Eeuo pipefail

function check_binaries()
{
  if ! command -v minikube &>/dev/null; then
    echo "minikube is not installed. Please install it before running the script."
    exit 1
  fi

  if ! command -v helm &>/dev/null; then
    echo "helm is not installed. Please install it before running the script."
    exit 1
  fi

  if ! command -v kubectl &>/dev/null; then
    echo "kubectl is not installed. Please install it before running the script."
    exit 1
  fi
}

function start_minikube()
{
  if minikube status | grep -q Running; then
    echo "Minikube is already running..."
  else
    # Start minikube
    echo "Starting minikube..."
    minikube start

    # Wait for minikube to start
    until minikube status | grep -q Running; do
      sleep 1
    done
  fi
}

function check_namespace()
{
  echo "Creating namespace..."
  kubectl create namespace logfilter-demo || {
    echo "Error creating namespace logfilter-demo"
    exit 1
  }
}

function install_chart(){
  echo "Installing OurApp Helm chart..."
  helm upgrade -i our-app charts/logfilter -f charts/logfilter/values.yaml -n logfilter-demo || {
    echo "Error installing OurApp Helm chart"
    exit 1
  }
}

main()
{
    check_binaries
    start_minikube
    check_namespace
    install_chart
}

main "$@"
