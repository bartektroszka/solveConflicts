set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level2/szablon.json > style.json
git add style.json
git commit -m 'Szablon styli'

git checkout -b gałąź_kolegi
cat ../../levels/level2/friend_file.json > style.json
git add style.json
git commit -m "Zielony footer"

git checkout master
git checkout -b twoja_gałąź
git branch -d master
cat ../../levels/level2/your_file.json > style.json
git add style.json
git commit -m "Czerwony header"