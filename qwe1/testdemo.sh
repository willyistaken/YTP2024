python3 ../qwe1/genNote.py "$1" > ../qwe1/note.txt
../qwe1/aa.out ../qwe1/stat.txt ../qwe1/note.txt > ../qwe1/tabArray.txt
python3 ../qwe1/outputTrack.py < ../qwe1/tabArray.txt
rm ../qwe1/tabArray.txt
rm ../qwe1/note.txt

