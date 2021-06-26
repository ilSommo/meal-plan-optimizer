#!/bin/bash

sed -i '' 's/__version__ = .*/__version__ = '\'$1\''/' **/*.py
sed -i '' 's/__version__ = .*/__version__ = '\'$1\''\\n",/' *.ipynb

pip freeze > requirements.txt

pdoc -o ./docs --docformat numpy meal_plan_optimizer

git add .
git commit -m "Bump version number to "$1""
git checkout master
git merge release-$1
git tag $1
git checkout develop
git merge release-$1
git branch -d release-$1