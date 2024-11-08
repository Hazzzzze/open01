#!/bin/sh

folder_name=$1

if [ ! -d "$folder_name" ]; then
    mkdir "$folder_name"
else
    echo "폴더 '$folder_name'이 이미 존재합니다."
fi

for i in $(seq 1 5); do
    touch "$folder_name/file$i.txt"
    echo "$folder_name/file$i.txt"
done

tar -czf "$folder_name/$folder_name.tar" -C "$folder_name" .

new_folder="${folder_name}/${folder_name}"
mkdir "$new_folder"

tar -xzf "$folder_name/$folder_name.tar" -C "$new_folder"

