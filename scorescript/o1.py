print("2 ",end='');
with open("temp.txt") as f:
    a = f.readlines();
    n = len(a[0]);
    tab_array=[];
    bar=0;
    note=0;
    for k in range(0,n):
        if(a[0][k]=='|'):
            bar+=1;
            note=0;
            continue; 
            for
          
