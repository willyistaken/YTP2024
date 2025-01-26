if [ -z "$1" ]; then
    echo "Usage: $0 <source_file.c>"
    exit 1
fi

file=$1
file-ext=${1%.tbt}
echo "$file"
./tbt-parser/tbt-printer --input-file "$file"
./tbt-parser/tbt-converter --input-file "$file" --emit-controlchange-events 0 --emit-pitchbend-events 0
# --emit-programchange-events 0 