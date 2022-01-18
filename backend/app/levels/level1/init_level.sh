# WARNING, THIS FUNCTION SHOULD ALWAYS BE RUN FROM THE USER DIRECTORY
rm * # to nie usunie katalogów użytkownika, ale jest mniejsza szansa na zrobienie sobie krzywdy tym skryptem
rm -rf .git
git init

set -e

touch '.empty'
git add .
git commit -m "Initial commit"

git checkout -b friend_branch
cat ../../levels/level1/friend_file > przepis.txt
git add .
git commit -m "Przepis na naleśniki :)"

git checkout master
cat ../../levels/level1/your_file > przepis.txt

chmod 777 przepis.txt

git add .
git commit -m "Najlepsze naleśniki!!!"