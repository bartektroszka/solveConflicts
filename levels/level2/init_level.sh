set -e

git init
cat ../../levels/level2/szablon.json > style.json
git add style.json
git commit -m 'Szablon styli'

git checkout -b friend_branch
cat ../../levels/level2/friend_file.json > style.json
git add style.json
git commit -m "Wersja przyjaciela"

git checkout master
git checkout -b your_branch
git branch -d master
cat ../../levels/level2/your_file.json > style.json
git add style.json
git commit -m "Moja wersja"