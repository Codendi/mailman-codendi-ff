#!/bin/bash

# usage:
#   getallsubscribers.sh lists.host.example.com /full/path/to/dest/dir

read -s -p "Site admin mailman password: " passwd
echo

exporter="`pwd`/mailman-subscribers.py"
ml_host=$1
to_dir="$2"

mkdir -p "$to_dir"

cd /var/lib/mailman/lists/
for list in *
do
  if [ -d $list ]; then
    echo "Exporting $list"
    #echo "$exporter -c $ml_host $list $passwd | cat >> $to_dir/$list.csv"
    "$exporter" -c "$ml_host" "$list" "$passwd" | cat >> "$to_dir/$list.csv"
  fi
done
