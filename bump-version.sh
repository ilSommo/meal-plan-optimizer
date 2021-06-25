#!/bin/bash

sed -i '' 's/__version__ = .*/__version__ = '\'$1\''/' meal_plan_optimizer.py
sed -i '' 's/__version__ = .*/__version__ = '\'$1\''\\n",/' meal-plan-optimizer.ipynb

pip freeze > requirements.txt

doxygen *
cd latex
make
cd ..
mv latex/refman.pdf docs/refman.pdf
rm -r html
rm -r latex

git commit -a -m "Bump version number to "$1""
git checkout master
git merge release-$1
git tag $1
git checkout develop
git merge release-$1
git branch -d release-$1