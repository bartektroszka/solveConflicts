set -e

git init
git config user.name "user"
git config user.email "user@user.com"
git config core.editor true

cat ../../levels/level3/szablon.py > kod.py
git add kod.py
git commit -m 'Szablon kodu'

git checkout -b catalan

cat ../../levels/level3/catalan.py > kod.py
git add kod.py
git commit -m "Liczby Catalana"

git checkout master
git checkout -b taylor
git branch -d master

cat ../../levels/level3/taylor.py > kod.py
git add kod.py
git commit -m "Szereg Taylora"
