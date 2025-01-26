

for i in {33..33};do
    wget -r -l 0 -A "*.tbt" --ignore-tags=nofollow -e robots=off -nd -P ./testtbt https://tabs.tabit.net/list.php?f=$i
    for file in ./testtbt/*\ *; do 
        mv "$file" "${file// /}"; 
    done
    for file in ./testtbt/*\'*; do 
        mv "$file" "${file//\'/}"; 
    done
    for file in ./testtbt/*.tbt;do
        ./tbtparse.sh $file
        python3 handletrack.py > tmp.txt
        pref="$(basename "$file" .tbt)"
        echo $pref
        for res in track*;do
            mv $res $pref$res
        done
        mv $pref*.txt ./data
        mv $pref*.mid ./data
        rm out.txt
        rm out.mid
    done
    rm ./testtbt/*.tbt
done
