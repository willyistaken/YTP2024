
datapath=./../tabsdata
tbtpath=./../tbttmp
if [ ! -d "$datapath" ]; then
    mkdir $datapath
fi
if [ ! -d "$tbtpath" ]; then
    mkdir $tbtpath
fi

for i in {2000..3000};do
    echo downloading $i
    wget -q -r -l1 -A "*.tbt" --ignore-tags=nofollow -e robots=off -nd -P $tbtpath "https://tabs.tabit.net/list.php?f=$i"
    if [ -z "$(ls $tbtpath)" ]; then
        continue
    fi
    for file in $tbtpath/*\ *; do 
        if [ ! -e "$file" ]; then
            continue
        fi
        mv "$file" "${file// /}"; 
    done
    for file in $tbtpath/*\'*; do 
        if [ ! -e "$file" ]; then
            continue
        fi
        mv "$file" "${file//\'/}"; 
    done
    echo doing $i
    for file in $tbtpath/*.tbt; do
        if [ ! -e "$file" ]; then
            continue
        fi
        echo $file
        ./tbtparse.sh $file > /dev/null 2>&1
        python3 handletrack.py
        rm out.txt
        rm out.mid
        pref="$(basename $file .tbt)"
        for res in track*;do
            if [ ! -e "$res" ]; then
                continue
            fi
            mv "${res}" "${pref}${res}"
        done
        mv "${pref}"*.txt $datapath 2>/dev/null
        mv "${pref}"*.mid $datapath 2>/dev/null
    done
    rm $tbtpath/*
done

rmdir $tbtpath
