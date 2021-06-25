#!/bin/bash

sed -i '' 's/__version__ = .*/__version__ = '\'$1\''/' meal_plan_optimizer.py
sed -i '' 's/__version__ = .*/__version__ = '\'$1\''\\n",/' meal-plan-optimizer.ipynb

doxygen meal_plan_optimizer
cd latex
make
cd ..
mv latex/refman.pdf docs/refman.pdf
rm -r html
rm -r latex

git commit -a -m "Bump version number to "$1""
git checkout master
git merge hotfix
git tag $1
git checkout develop
git merge hotfix
git branch -d hotfix