#!/bin/bash

sed -i '' 's/__version__ = .*/__version__ = '\'$1\''/' branch_and_bound.py
sed -i '' 's/__version__ = .*/__version__ = '\'$1\''\\n",/' meal-plan-optimizer.ipynb

git commit -a -m "Bump version number to "$1""
git checkout master
git merge release-$1
git tag $1
git checkout develop
git merge release-$1
git branch -d release-$1