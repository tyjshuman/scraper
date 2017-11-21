#!/bin/sh
for i in $1/*;
do
#echo "%s/}/}/g
#%s/[\n
#%s/\n]
#w
#q
#" | ex $i;
sed -i 's/},/}/g' $i
sed -i 's/[' $i
sed -i 's/]' $i
sed -i '$d' $i
sed -i '1,1d' $i
#echo $i
#tr -d '[\n' < $i >> $i".clean"
#tr -d '\n]' < $i".clean" >> $i".cleaner"
#mv $i".cleaner" $i
#rm $i".clean"
done
