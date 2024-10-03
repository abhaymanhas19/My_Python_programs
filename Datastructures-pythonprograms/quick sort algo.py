def quick_sort(array,f,q):
    pivot=array[f]
    p=f+1

    while True:
       while p<=q and array[p]<=pivot:
           p = p + 1
       while p <= q and array[q] >=pivot:
           q=q-1
       if q<p:
          break
       else:
           array[p],array[q]=array[q],array[p]
    array[f],array[q] = array[q] ,array[f]
    return q
def quick(array,f,q):
    if f < q:
       p=quick_sort(array,f,q)
       quick(array,f,p-1)
       quick(array,p+1,q,)

array=[4,8,6,7,2,4,5,9,7,2]

quick(array,0,len(array)-1)
print(array)
