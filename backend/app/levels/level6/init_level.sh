set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level6/puste_daty.txt > wyjazd.txt
git add .
git commit -m 'pusty kalendarz'

git checkout -b mat

cat ../../levels/level6/mat.txt > wyjazd.txt
git add .
git commit -m "mat"

git checkout master
git checkout -b pat
git branch -d master
cat ../../levels/level6/pat.txt > wyjazd.txt
git add .
git commit -m "pat"

cat ../../levels/level6/pat_bzdury.txt > wyjazd.txt

