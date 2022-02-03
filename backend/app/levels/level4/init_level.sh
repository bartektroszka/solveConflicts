# We already assume that the user has deleted directory

set -e

git init
git config user.name "user"
git config user.email "user@user.com"

cat ../../levels/level4/szablon.cpp > kod.cpp
git add kod.cpp
git commit -m 'szablon kodu'

git checkout -b friend_branch

cat ../../levels/level4/friend_kod1.cpp > kod.cpp
git add kod.cpp
git commit -m "some fancy operators" 

cat ../../levels/level4/friend_kod2.cpp > kod.cpp
git add kod.cpp
git commit -m "helpful defines"

cat ../../levels/level4/friend_kod3.cpp > kod.cpp
git add kod.cpp
git commit -m "some actual code"

git checkout master
git checkout -b my_branch
git branch -d master
cat ../../levels/level4/moj_kod.cpp > kod.cpp
git add kod.cpp
git commit -m "Starter pack"

