# WARNING, THIS FUNCTION SHOULD ALWAYS BE RUN FROM THE USER DIRECTORY
rm *
rm -rf .git
git init

set -e

touch .empty
git add .empty
git commit -m 'initial_commit'

git checkout -b liczby_catalana
cat ../../levels/level3/catalan.py > kod.py
git add kod.py
git commit -m "liczby Catalana"

git checkout master
git checkout -b szereg_taylora
git branch -d master

cat ../../levels/level3/taylor.py > kod.py
git add kod.py
git commit -m "szereg Taylora"