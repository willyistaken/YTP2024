
#wget -q -r -l 0 -A "*.tbt" --ignore-tags=nofollow -e robots=off -nd -P ./testtbt https://tabs.tabit.net/list.php?f=2
if [ -z "$(ls ./testtbt)" ]; then
    exit
fi
for file in ./testtbt/*\ *; do 
    if [ ! -e "$file" ]; then
        continue
    fi
    mv "$file" "${file// /}"; 
done
for file in ./testtbt/*\'*; do 
    if [ ! -e "$file" ]; then
        continue
    fi
    mv "$file" "${file//\'/}"; 
done
echo doing $i
for file in ./testtbt/*.tbt; do
    if [ ! -e "$file" ]; then
        continue
    fi
    ./tbtparse.sh $file > /dev/null 2>&1
    python3 handletrack.py > tmp.txt
    # rm out.txt
    # rm out.mid
    pref="$(basename $file .tbt)"
    for res in track*;do
        if [ ! -e "$res" ]; then
            continue
        fi
        mv "${res}" "${pref}${res}"
    done
    mv "${pref}"*.txt ./../tabsdata 2>/dev/null
    mv "${pref}"*.mid ./../tabsdata 2>/dev/null
done