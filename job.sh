#!/bin/sh

rm -rf email.txt

for i in `cat monitor.txt`; do
	LAST=`ls -1 results/$i*.txt | tail -n 2 | head -n 1`
	CURRENT=`ls -1 results/$i*.txt | tail -n 1`
	echo -------------- >> email.txt
	echo diff $LAST $CURRENT >> email.txt
	diff $LAST $CURRENT >> email.txt
done