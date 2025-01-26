
for file in ./testtbt/*.tbt;do
    ./tbtparse.sh $file
    python3 handletrack.py > tmp.txt
    pref="$(basename "$file" .tbt)"
    echo $pref
    for res in track*;do
        mv $res $pref$res
    done
    mv $pref* data
    rm out.txt
    rm out.mid
done