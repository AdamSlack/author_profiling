
f = open('processed.sql')

alphabet = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')

names = list(set([x+y+z for x in alphabet for y in alphabet for z in alphabet ]))


lines = f.readlines()

cols = lines[0].split(',')

print(len(names))
print(len(cols))

o = open('processed_table.sql', 'w')

for i in range (0, len(cols)):
    o.write('\t' + names[i] + '_value\t' + 'double' + '\t' + 'not null,' + '\n')

f.close()
o.close()