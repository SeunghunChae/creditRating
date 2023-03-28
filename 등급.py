lista=[]
with open('최종_origin.csv','r',newline='') as f:
    while True:
        line=f.readline()
        lista.append(line)
        #print(line)
        if len(line)==0:
            break

#lista=lista[0:10]
with open('최종2_origin.csv','w',newline='') as f:
    for i in lista:
        i=i.replace('\n','')
        line=i.split(',')
        if line[0]=='한신평cp':
            if line[6].find('A1')!=-1:
                i+=',110'
            elif line[6].find('A2+')!=-1:
                i+=',120'
            elif line[6].find('A2')!=-1:
                i+=',121'
            elif line[6].find('A2-')!=-1:
                i+=',122'
            elif line[6].find('A3+')!=-1:
                i+=',130'
            elif line[6].find('A3')!=-1:
                i+=',131'
            elif line[6].find('A3-')!=-1:
                i+=',132'
            elif line[6].find('B+')!=-1:
                i+=',210'
            elif line[6].find('B')!=-1:
                i+=',211'
            elif line[6].find('B-')!=-1:
                i+=',212'
            elif line[6].find('C')!=-1:
                i+=',310'
            elif line[6].find('D')!=-1:
                i+=',410'
            else:
                i+=',변환등급'
        elif line[0]=='나신평cp':
            if line[5].find('A1')!=-1:
                i+=',110'
            elif line[5].find('A2+')!=-1:
                i+=',120'
            elif line[5].find('A2')!=-1:
                i+=',121'
            elif line[5].find('A2-')!=-1:
                i+=',122'
            elif line[5].find('A3+')!=-1:
                i+=',130'
            elif line[5].find('A3')!=-1:
                i+=',131'
            elif line[5].find('A3-')!=-1:
                i+=',132'
            elif line[5].find('B+')!=-1:
                i+=',210'
            elif line[5].find('B')!=-1:
                i+=',211'
            elif line[5].find('B-')!=-1:
                i+=',212'
            elif line[5].find('C')!=-1:
                i+=',310'
            elif line[5].find('D')!=-1:
                i+=',410'
            else:
                i+=',변환등급'
        elif line[0]=='한신평stb':
            if line[7].find('A1')!=-1:
                i+=',110'
            elif line[7].find('A2+')!=-1:
                i+=',120'
            elif line[7].find('A2')!=-1:
                i+=',121'
            elif line[7].find('A2-')!=-1:
                i+=',122'
            elif line[7].find('A3+')!=-1:
                i+=',130'
            elif line[7].find('A3')!=-1:
                i+=',131'
            elif line[7].find('A3-')!=-1:
                i+=',132'
            elif line[7].find('B+')!=-1:
                i+=',210'
            elif line[7].find('B')!=-1:
                i+=',211'
            elif line[7].find('B-')!=-1:
                i+=',212'
            elif line[7].find('C')!=-1:
                i+=',310'
            elif line[7].find('D')!=-1:
                i+=',410'
            else:
                i+=',변환등급'
        elif line[0]=='나신평stb':
            if line[5].find('A1')!=-1:
                i+=',110'
            elif line[5].find('A2+')!=-1:
                i+=',120'
            elif line[5].find('A2')!=-1:
                i+=',121'
            elif line[5].find('A2-')!=-1:
                i+=',122'
            elif line[5].find('A3+')!=-1:
                i+=',130'
            elif line[5].find('A3')!=-1:
                i+=',131'
            elif line[5].find('A3-')!=-1:
                i+=',132'
            elif line[5].find('B+')!=-1:
                i+=',210'
            elif line[5].find('B')!=-1:
                i+=',211'
            elif line[5].find('B-')!=-1:
                i+=',212'
            elif line[5].find('C')!=-1:
                i+=',310'
            elif line[5].find('D')!=-1:
                i+=',410'
            else:
                i+=',변환등급'
        i+='\n'
        f.write(i)
    
        
