#!/bin/bash
pipenv update mlspeclib
pipenv lock -r > requirements.txt

git add .
git commit -a -m 'updating requirements'
git push

docker build --no-cache -t mlspec/mlspeclib-action-samples-process-data .
docker push mlspec/mlspeclib-action-samples-process-data
