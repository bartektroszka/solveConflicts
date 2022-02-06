set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cp ../../levels/level8/importy.py kod.py
git add kod.py
git commit -m 'importy'

cp ../../levels/level8/readGraph.py kod.py
git add .
git commit -m "Grafu z pliku"

cp ../../levels/level8/inputNode.py kod.py
git add .
git commit -m "Wczytaj start"

git checkout HEAD~2
git checkout -b bugFix
cp ../../levels/level8/readfix.py kod.py
git add .
git commit -m "Drobny fix"

git checkout master
git merge bugFix -X theirs # Nie umiem zrobić sensownej wiadomości

cp ../../levels/level8/dfs.py kod.py
git add .
git commit -m 'dfs'

git checkout -b dfsFix
cp ../../levels/level8/dfsFix.py kod.py
git add .
git commit -m 'dfsFix'

git checkout master
cp ../../levels/level8/dfsStyleFix.py kod.py
git add .
git commit -m 'nazwy zmiennych'
