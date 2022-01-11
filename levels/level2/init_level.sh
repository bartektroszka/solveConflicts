set -e

mkdir style
git add .
git commit -m 'initial commit'

git chektout -b friend_branch
cat friend_file > style/plik.css
git add .
git commit -m "plik css twojego twojego przyjaciela"

git checkout -b your_branch
cat your_file > style/plik.css
git add .
git commit -m "twoja wersja pliku css"