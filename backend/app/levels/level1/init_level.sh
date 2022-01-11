set -e

mkdir przepisy
touch przepisy/przepis.txt
git add .
git commit -m "Initial commit (empty przepis.txt)"

git checkout -b friend_branch
cat ../../levels/level1/friend_file > przepisy/przepis.txt
git add .
git commit -m "Przepis na naleśniki :)"

git checkout master
cat ../../levels/level1/your_file > przepisy/przepis.txt
git add .
git commit -m "Najlepsze naleśniki!!!"