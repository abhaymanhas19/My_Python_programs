
#with function

#def search (list,n):
#    for x in range(len(list)):
#       if list[x]==n:
#          print("found")
#          break
#    else:
#        print("not found")
#list=[12,45,74,85,68,21,254,14,15]
#n=852
#search(list,n)

list=[1,2,47,22,56,23,56,67]
n=int(input("enterr he number you want to search:-"))
i=0
while i<len(list):
    if list[i]==n:
       print(i)
       break
    i+=1
else:
    print("not found")


