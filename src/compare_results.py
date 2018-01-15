mlp = []
rando = []
gnb = []
km = []
with open('compare_results.csv') as f:
    lines = f.readlines()
    for idx, l in enumerate(lines):
        if idx % 4 == 0:
            mlp.append(l)    
        if idx % 4 == 1:
            rando.append(l)
        if idx % 4 == 2:
            gnb.append(l)
        if idx % 4 == 3:
            km.append(l)


with open('ordered_compare.csv', 'a') as f:
    for l in mlp:
        f.write(l)
    f.write('\n')

    for l in rando:
        f.write(l)
    f.write('\n')

    for l in gnb:
        f.write(l)            
    f.write('\n')
        
    for l in km:
        f.write(l)
