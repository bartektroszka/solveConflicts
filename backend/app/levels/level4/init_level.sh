# We already assume that the user has deleted directory

set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level4/szablon.cpp > kod.cpp
git add kod.cpp
git commit -m 'Szablon kodu'

git checkout -b gałąź_kolegi

cat ../../levels/level4/friend_kod1.cpp > kod.cpp
git add kod.cpp
git commit -m "Operator par"

cat ../../levels/level4/friend_kod2.cpp > kod.cpp
git add kod.cpp
git commit -m "Przydatne dyrektywy"

cat ../../levels/level4/friend_kod3.cpp > kod.cpp
git add kod.cpp
git commit -m "Pierwsze rozwiązanie"

git checkout master
git checkout -b gałąź_koleżanki
git branch -d master
cat ../../levels/level4/moj_kod.cpp > kod.cpp
git add kod.cpp
git commit -m "Trochę kodu"

