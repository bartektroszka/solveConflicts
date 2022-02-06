set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level5/base.lor > file.lor
git add .
git commit -m 'szablon'

git checkout -b gałąź_kolegi

cat ../../levels/level5/friend_changes.lor > file.lor
git add .
git commit -m "Poprawki"

git checkout master
git checkout -b twoja_gałąź
git branch -d master
cat ../../levels/level5/your_changes.lor > file.lor
git add .
git commit -m "Drobne zmiany"

