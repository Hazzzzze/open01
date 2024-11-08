#!/bin/sh

folder_name=$1

if [ ! -d "$folder_name" ]; then
    mkdir "$folder_name"
else
    echo "폴더 '$folder_name'가 이미 존재합니다."
fi

for i in 0 1 2 3 4; do
    file_name="file$i.txt"
    file_path="$folder_name/$file_name"
    subfolder_path="$folder_name/file$i"

    touch "$file_path"

    if [ ! -d "$subfolder_path" ]; then
        mkdir "$subfolder_path"
    fi

    ln -s "../$file_name" "$subfolder_path/$file_name"
done

