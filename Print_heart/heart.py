key = input("enter the word you like...")

print("\n".join([''.join([(key[(x-y)%len(key)]\
if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')\
for x in range(-30,30)])for y in range(15,-15,-1)]))
