# WARNING, THIS FUNCTION SHOULD ALWAYS BE RUN FROM THE USER DIRECTORY
rm *.json
yes | rm -r .git
git init

set -e

touch .empty
git add .empty
git commit -m 'initial_commit'

git checkout -b friend_branch
cat ../../levels/level2/friend_file.json > style.json
git add style.json
git commit -m "plik json twojego twojego przyjaciela"

git checkout master
git checkout -b your_branch
cat ../../levels/level2/your_file.json > style.json
git add style.json
git commit -m "twoja wersja pliku json"