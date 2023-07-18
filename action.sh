#!/usr/bin/env bash

if [ "$GITHUB_ACTIONS" == "true" ]; then
  echo "running in GitHub CI"
  if [ "$GITHUB_EVENT_NAME" == "pull_request" ]; then
    echo "running a pull request pipeline"

  fi
elif [ "$GITLAB_CI" == "true" ]; then
  echo "running in GitLab CI"
  if [ "$CI_PIPELINE_SOURCE" == "merge_request_event" ]; then
    echo "running a merge request pipeline"
    
  fi
else
  echo "not running in known CI, using regular entrypoint"
  ./entrypoint.sh
  exit $?
fi