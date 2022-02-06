set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level1/podstawowy_przepis > przepis.txt
git add .
git commit -m "Przepis bez składników"

git checkout -b gałąź_kolegi
cat ../../levels/level1/friend_file > przepis.txt
git add .
git commit -m "Idealne proporcje"

git checkout master
git checkout -b twoja_gałąź
git branch -d master
cat ../../levels/level1/your_file > przepis.txt

chmod 777 przepis.txt

git add .
git commit -m "Składniki"