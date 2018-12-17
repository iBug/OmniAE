#!/bin/bash
set -e

e_info() { echo -e "\e[36;1m[Info]\e[0m $*" >&2; }
e_warning() { echo -e "\e[33;1m[Warning]\e[0m $*" >&2; }
e_error() { echo -e "\e[31;1m[Error]\e[0m $*" >&2; }
e_success() { echo -e "\e[32;1m[Success]\e[0m $*" >&2; }

if [ -z "$GH_TOKEN" ]; then
  e_error "No GitHub token is set, cannot deploy."
  exit 1
fi

REMOTE=origin
BRANCH=deploy
USERNAME=${CIRCLE_PROJECT_USERNAME:-iBug}
REPONAME=${CIRCLE_PROJECT_REPONAME:-AndroidOverflow}
REPO="$USERNAME/$REPONAME"

main() {
  e_info "Starting deploy"
  e_info "Moving branch to '$BRANCH'"
  git branch -M $BRANCH
  e_info "Setting remote with GH_TOKEN"
  git remote add "$REMOTE-deploy" "https://$GH_TOKEN@github.com/$REPO.git"
  e_info "Pushing to $REMOTE/$BRANCH"
  git push -q -u "$REMOTE-deploy" $BRANCH
  e_success "Successfully deployed"
}

main | sed "s/$GH_TOKEN/[secret]/g"
