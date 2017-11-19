#!/bin/sh
for i in *;
do
#echo "%s/}/}/g
#%s/[\n
#%s/\n]
#w
#q
#" | ex $i;
sed -i -e 's/}/}/g' $i
sed -i -e 's/[\n//' $i
sed -i -e 's/\n]//' $i
done
