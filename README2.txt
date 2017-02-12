
GIT Simple Guide:
http://rogerdudler.github.io/git-guide/

git commit -am "Put comment message here"

git push

git status

. upload.sh tingeyal

HOW TO SEARCH FOR STRING IN FOLDER / FILES:

grep -rnw '/path/to/somewhere/' -e "pattern"

This was taken from the following site:

http://stackoverflow.com/questions/16956810/finding-all-files-containing-a-text-string-on-linux


HOW TO FIND AND REPLACE A STRING IN ALL FILES/SUBDIRECTORIES:

find <mydir> -type f -exec sed -i 's/<string1>/<string2>/g' {} +
e.g. find /home/k/dwad -type f -exec sed -i 's/test/mugs/g' {} +

http://stackoverflow.com/questions/1583219/awk-sed-how-to-do-a-recursive-find-replace-of-a-string

