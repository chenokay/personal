!#/bin/sh

files=$(find ./before/ -name '*.jpg')

for file in $files
do
	bsname=$(basename "$file")
	jpegtran -copy none -optimize -perfect $file > ./after/$bsname
done
