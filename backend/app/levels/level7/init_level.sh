set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cp -r ../../levels/level7/template/* .
git add .
git commit -m 'Szablon zmian'

git checkout -b rodzice

cp -r ../../levels/level7/parter/* .
git add .
git commit -m "Drobne sugestie do parteru"

cp -r ../../levels/level7/pietro/* .
git add .
git commit -m "Wymarzony wystrój piętra"

cp -r ../../levels/level7/ogrod/* .
git add .
git commit -m "Bajkowy ogórd z naszych snów"

git checkout master
git checkout -b remont
git branch -d master

cp -r ../../levels/level7/skromny_plan/* .
git add .
git commit -m "Wstępny plan zmian"

cp -r ../../levels/level7/notatki.txt .
git add .
git commit -m "przemyślenia"
