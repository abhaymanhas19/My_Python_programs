list=[1,2,3,4,5,6,7,8,9]
data=int(input("Enter the value you want to search"))
l=0
u=len(list)-1
while l<=u:
    mid_value=(l+u)//2
    if list[mid_value]==data:
        print("The data is found at location: ", mid_value)
        break
    elif list[mid_value]<data:
        l=mid_value+1
    else:
       u=mid_value-1
else:
   print('element not found')

#with function ..binary search
#def binary_search(list,data):
#lower=0
 #   upper=len(list)-1
 #   while lower<=upper:
  #      mid=(lower+upper)//2
  #      if data==list[mid]:
  #          print("element is found at location :", mid)
  #          break
   #     elif data>list[mid]:
   #         lower=mid+1
   #     else:
    #        upper=mid-1
    #else:
     #   print("element not found")
#list=[1,2,3,4,5,6,7,8,9]
#data=85
#binary_search(list,data)