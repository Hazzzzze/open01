#!/bin/sh

expression=$1

num1=$(echo "$expression" | grep -oP '^\d+')
op=$(echo "$expression" | grep -oP '[+-]')
num2=$(echo "$expression" | grep -oP '\d+$')

if [ "$op" = "+" ]; then
    result=$(expr $num1 + $num2)
elif [ "$op" = "-" ]; then
    result=$(expr $num1 - $num2)
else
    echo "Invalid operator"
    exit 1
fi

echo "$result"

exit 0

