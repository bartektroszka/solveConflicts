# We already assume that the user has deleted directory

set -e

git init
cat ../../levels/level5/base.lor > file.lor
git add .
git commit -m 'szablon'

git checkout -b friend_branch

cat ../../levels/level5/friend_changes.lor > file.lor
git add .
git commit -m "Lorem enchanced"

git checkout master
git checkout -b my_branch
git branch -d master
cat ../../levels/level5/your_changes.lor > file.lor
git add .
git commit -m "Kalorem"

