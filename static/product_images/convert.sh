!#/bin/sh

for img in $(find ./before/ -name '*.jpg')
do  
	name=$(basename $img)
	convert $img -resize "300x300>" ./after/$name
done
