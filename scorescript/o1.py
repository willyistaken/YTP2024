print("2 ",end='');
with open("temp.txt") as f:
    a = f.readline();
    n = len(a)-2;
    for i in range(0,n-1):
        print(1,end='');
