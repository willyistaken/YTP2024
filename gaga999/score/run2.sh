
#!/bin/bash




# Check if the user provided a folder argument
if [[ -z "$1" ]]; then
    echo "Usage: $0  <program>"
    exit 1
fi

# Assign the folder path
folder="libs"

# Check if the folder exists
if [[ ! -d "$folder" ]]; then
    echo "Error: Folder '$folder' not found."
    exit 1
fi

# Iterate through .mid files in the specified folder

files=("$folder"/*.mid)
total=${#files[@]} 
if (($# >= 2)); then
	total=$2
fi
echo "$total"
count=0
for mid_file in "$folder"/*.mid; do
    # Check if any .mid files exist
    [[ -e "$mid_file" ]] || continue

    txt_file="${mid_file%.mid}.txt"


	#CHANGE HERE , whatever your program do here, just output it to temp.txt, $1 is your program(which is the argument this script take)
	#python "$mid_file" > temp.txt
	#cp "$mid_file" ~/code/YTP/tabsdata/algo/tuttut/midis/a.mid
    #cd ~/code/YTP/tabsdata/algo/tuttut/
	#python midi_tabs_cli.py "a.mid" > /dev/null
	#cp ~/code/YTP/tabsdata/algo/tuttut/tabs/a.txt ~/code/YTP2024/scorescript/temp.txt
	#cd ~/code/YTP2024/scorescript/.
	#python o1.py >> temp.txt	
	
	# "$1" "$mid_file" > temp.txt
	
	# echo "$mid_file"
	python3 "$1" "$mid_file" > temp.txt
	
	if [[ $? -eq 0 ]]; then
		rm result.txt
		echo 1 >> result.txt
		# ./a.out "$txt_file" temp.txt >> result.txt
		# ./armb.out "$txt_file" temp.txt >> result.txt
		./armc.out "$txt_file" temp.txt >> result.txt
		
		if [[ $? -eq 0 ]]; then
			:
		else
			echo "${txt_file} a.out error";
		fi	
	else
		echo "${txt_file} python error";
	fi
	((count++))
	percentage=$((count * 100 / total))

	printf "\rProgress: [%-50s] %d%% (%d/%d)" \
        "$(printf '#%.0s' $(seq 1 $((percentage / 2))))" \
        "$percentage" "$count" "$total"
	echo 0 >> result.txt
	echo ""
	echo "$mid_file"
	python3 average.py < result.txt
	if [[ $count -ge $total ]];then
		break;
	fi
done
echo ""

