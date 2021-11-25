def file_read(file_txt):
    file1 = open(file_txt, 'r')
    txt = []
    while True:
        line = file1.readline()
        if not line:
            break
        txt.append(line.strip())

    file1.close()
    return txt[5:]

def validator(n):
    txt = file_read("result(n="+str(n)+").txt")
    grid = dict()
    for i in range(n):
        for j in range(n):
            if txt[i][j] == "o":
                grid[i] = j
    if len(set(grid.keys())) != n :
        return False
    for i in range(n):
        for j in range(i+1,n):
            if grid.get(i)== grid.get(j) or abs(i-j) == abs(grid.get(i) - grid.get(j)):
                return False
    return True
print(validator(900))
for i in [5,20,40,100,200,300,400,600,700,800]:
    try:
        print(validator(i))
    except:
        print("FALSE")