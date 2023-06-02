#!/bin/bash
set -Eeuo pipefail

function check_binaries() {
  local missing_binaries=()
  local bold=$(tput bold)

  check_binary() {
    if ! command -v "$1" &>/dev/null; then
      missing_binaries+=("$1")
    fi
  }

  check_binary minikube
  check_binary helm
  check_binary kubectl

  if [[ ${#missing_binaries[@]} -gt 0 ]]; then
    echo "The following binaries are not installed: ${bold}${missing_binaries[*]}. Please make sure you install \
them before running the script."
    exit 1
  fi
}


function start_minikube()
{
  if minikube status | grep -q Running; then
    echo "Minikube is already running..."
  else
    echo "Starting minikube..."
    minikube start

    until minikube status | grep -q Running; do
      sleep 1
    done
  fi
}

function check_namespace() {
  local namespace="logfilter-demo"
  if kubectl get namespace $namespace &>/dev/null; then
    echo "Namespace $namespace already exists. Skipping..."
  else
    echo "Creating namespace $namespace..."
    kubectl create namespace $namespace
  fi
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
