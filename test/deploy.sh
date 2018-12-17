#!/bin/bash

e_info() { echo -e "\e[36;1m[Info]\e[0m $*" >&2 }
e_warning() { echo -e "\e[33;1m[Warning]\e[0m $*" >&2 }
e_error() { echo -e "\e[31;1m[Error]\e[0m $*" >&2 }
e_success() { echo -e "\e[32;1m[Success]\e[0m $*" >&2 }

if [ -z "$GH_TOKEN" ]; then
  e_error "No GitHub token is set, cannot deploy."
  exit 1
fi

e_success "Ready to deploy"
