set -e

git init
git config user.name "user"
git config user.email "user@user.com"
git config core.editor true

cp -r ../../levels/level7/template/* .
git add .
git commit -m 'Szablon zmian'

git checkout -b rodzice

cp -r ../../levels/level7/parter/* .
git add .
git commit -m "Sugestie - parter"

cp -r ../../levels/level7/pietro/* .
git add .
git commit -m "Wymarzone piętro"

cp -r ../../levels/level7/ogrod/* .
git add .
git commit -m "Bajkowy ogród"

git checkout master
git checkout -b remont
git branch -d master

cp -r ../../levels/level7/skromny_plan/* .
git add .
git commit -m "Wstępny plan zmian"

cp -r ../../levels/level7/notatki.txt .
git add .
git commit -m "Kilka notatek"
