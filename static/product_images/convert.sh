#!/bin/sh

TMP=./before/tmp

for img in $(find ./before/ -name '*.jpg')
do  
	name=$(basename $img)
	convert $img -resize "600x600>" $TMP
	jpegtran -copy none -optimize -perfect $TMP > ./after/$name
done
