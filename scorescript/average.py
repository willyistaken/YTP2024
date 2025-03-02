



if __name__=="__main__":
    cbarcnt=0;
    tbarcnt=0;
    csoundcnt=0;
    tsoundcnt=0;
    clearcnt = 0;
    ccomcnt=0;
    tcomcnt=0;
    k = int(input());

    group=0

    while(k==1):
        group+=1
        #print(group*4)
        line1 = input().split(' ');
        line2 = input().split(' ');
        line3 = input().split(' ');
        cbarcnt += int(line1[0]);
        tbarcnt += int(line1[1]);
        csoundcnt += int(line2[0]);
        tsoundcnt += int(line2[1]);
        clearcnt+=int(line2[2]);
        ccomcnt += int(line3[0]);
        tcomcnt += int(line3[1]);
        k = int(input());
    print("bar:" ,cbarcnt/tbarcnt);
    print("tab:", csoundcnt/tsoundcnt,'/',(csoundcnt-clearcnt)/(tsoundcnt-clearcnt));
    print("sound:", ccomcnt/tcomcnt,'/',(ccomcnt-clearcnt)/(tcomcnt-clearcnt));


