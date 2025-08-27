# def quick_sort(array,f,q):
#     pivot=array[f]
#     p=f+1

#     while True:
#        while p<=q and array[p]<=pivot:
#            p = p + 1
#        while p <= q and array[q] >=pivot:
#            q=q-1
#        if q<p:
#           break
#        else:
#            array[p],array[q]=array[q],array[p]
#     array[f],array[q] = array[q] ,array[f]
#     return q
# def quick(array,f,q):
#     if f < q:
#        p=quick_sort(array,f,q)
#        quick(array,f,p-1)
#        quick(array,p+1,q,)

# array=[4,8,6,7,2,4,5,9,7,2]

# quick(array,0,len(array)-1)
# print(array)




array = [2,53,89,234,6,2,7,2,67,73,6,53,73,1] #,start = 0 ,end=13

after_iteration_1 = [2,1,89,234,6,2,7,2,67,73,6,53,73,53] #,start=1,end=13


def sort_partitaion_arry(array,start,end):
    pivot = array[start]
    pointer = start+ 1

    while True:
        while pointer<=end and array[pointer]<=pivot:
            pointer +=1
        while pointer<=end and array[end]>=pivot:
            end -=1
        if pointer>end:
            break
        else:
            array[pointer],array[end] = array[end] , array[pointer]
    array[start],array[end] = array[end],array[start]
    return end

def quick_sort(array,start,end):
    if start < end:
        p=sort_partitaion_arry(array,start,end)
        quick_sort(array,start,p-1)
        quick_sort(array,p+1,end)

        
quick_sort(array=array,start=0,end=len(array)-1)
print(array)        


