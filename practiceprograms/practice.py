
#####################################################################################
## write the fibboncai serires upto n number
#####################################################################################

# def fibo(n):
#    n1 , n2 = 0, 1
#    if n ==1:
#        print(n1)
#        return
#    for i in range(n):
#        print(n1)
#        n1, n2 = n2 , n1 + n2
#    return

#fibo(10)

####################################################################################
## Reverse a given string with variout technique
####################################################################################

s = "abhayManhas"

# using slicing
# print(s[::-1])

reverse_string = ""
# Using negative index
#for i in range(len(s)-1, -1, -1):
#    reverse_string += s[i]

# Using simplest iterating
#for char in s:
#    reverse_string = char + reverse_string



###############################################################################################
# Find the missing number in consective array
###############################################################################################
#a=[0,1,2,3,4,5,7,8]

#total = len(a)+1

# Formula (number_of_total_elements * (firest_element + last_element) // 2)- this is expected sum
#expected_sum = (total*(a[0]+a[-1])) //2
#actual_sum = sum(a) # Given Array sum

#missing_value = expected_sum - actual_sum # Find the missing value
#print(missing_value)
