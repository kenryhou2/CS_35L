#!/bin/sh

cat $1 |
grep '<td>.*</td>' | #track lines with <td> and </td>
sed 's/^\s*//g' | #get rid of spaces
sed 's/<[^>]*>//g' | #rid non relevant html tags
sed '/^$/d' | #rids blank lines
sed -n '1~2!p' | #rids digits and english specific chars
tr [:upper:] [:lower:] | #replaces uppercase with lowercase 
tr '`' "'" | #replace ` as '
sed 's/, /\n/g' | #separate words with comma and space
sed 's/ /\n/g' | 
sed "/[^pk'mnwlhaeiou]/d" | #remove non hawaiian
sort -u | #sort words uniquely
sed '/^$/d' #removes final spaces
