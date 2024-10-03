def buublesort(array):
   for j in range(len(array)-1):
      for i in range(len(array)-1):
         if array[i] > array[i + 1]:
             array[i], array[i + 1] = array[i + 1], array[i]
   return array


array=[]

n=int(int(input("how many elements you want to add:-")))
while len(array)<=n:

     values=int(input("enter the values of array:-"))
     array.append(values)
print("The elements of array are ",array)

print("The sorted array is ",(buublesort(array)))
