#!bin/sh

set -e

git config --global user.name "NDPGitBot"
git config --global user.email "ndpgitbot@newportdataproject.org"

git clone https://github.com/NewportDataPortal/seeclickfix-archive.git
python3 make-archive.py

DATE=`date +%Y-%m-%d`

cd ./seeclickfix-archive
git remote rm origin
git remote add origin https://$GITHUB_USER:$GITHUB_PASSWORD@github.com/NewportDataPortal/seeclickfix-archive.git
git add --all
git commit -m "update $DATE"
git push --set-upstream origin master
