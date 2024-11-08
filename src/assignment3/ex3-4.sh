#!/bin/sh

echo "리눅스가 재밌나요? (yes / no)"

read answer

case $answer in
    yes | y | Y | Yes | YES | yyy | yyyy | yyyyy)
        echo "yes";;
    no | n | N | No | NO | nono | nnn | nnnn | nnnnn)
        echo "no";;
    *)
        echo "yes or no로 입력해 주세요. "
        exit 1;;
esac

exit 0
