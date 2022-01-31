# WARNING, THIS FUNCTION SHOULD ALWAYS BE RUN FROM THE USER DIRECTORY
set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level3/szablon.py > kod.py
git add kod.py
git commit -m 'szablon kodu'

git checkout -b liczby_catalana

# cat ../../levels/level3/silnia_rek.py > kod.py
# git add kod.py
# git commit -m "Silnia rekurencyjnie"

cat ../../levels/level3/catalan.py > kod.py
git add kod.py
git commit -m "liczby Catalana"


git checkout master
git checkout -b szereg_taylora
git branch -d master

# cat ../../levels/level3/silnia_iteracyjnie.py > kod.py
# git add kod.py
# git commit -m "Silnia iteracyjnie"

cat ../../levels/level3/taylor.py > kod.py
git add kod.py
git commit -m "szereg Taylora"
