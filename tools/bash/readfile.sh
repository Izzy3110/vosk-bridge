#!/bin/ksh
LINE_NUMBERS=0
if [[ $2 -eq 1 ]]; then
    LINE_NUMBERS=1
fi

I=0
while IFS= read -r line
do
  if [[ $LINE_NUMBERS -eq 1 ]]; then
    echo -e $I": "$line
  else
    echo -e "${line}"
  fi
  I=$((I+1))
done < $1

