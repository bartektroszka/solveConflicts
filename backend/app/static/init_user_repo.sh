set -e
git status

touch master.txt
git add master.txt
git commit -m 'master commit'

git checkout -b branch_b
git checkout -b branch_a

touch a.txt
git add a.txt
git commit -m 'commit na galezi a'


git checkout branch_b

touch b.txt
git add b.txt
git commit -m 'commit na galezi b'

git checkout master
touch master2.txt
git add .
git commit -m 'drugi commit na masterze'

git merge branch_a
git merge branch_b