# Zakładamy, że katalog użytkownika został już opróźniony

set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level1/podstawowy_przepis > przepis.txt
git add .
git commit -m "Initial commit"

git checkout -b friend_branch
cat ../../levels/level1/friend_file > przepis.txt
git add .
git commit -m "Idealne proporcje składników"

git checkout master
git checkout -b my_branch
git branch -d master
cat ../../levels/level1/your_file > przepis.txt

chmod 777 przepis.txt  # still necessary ??

git add .
git commit -m "Proporcje"