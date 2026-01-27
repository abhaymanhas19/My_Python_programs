import sys

def main(values):
    number_of_test_cases = int(values[0])
    total_sum = 0
    completed = 0
    def perform_test_case(lst):
        nonlocal total_sum
        nonlocal completed

        if completed >= number_of_test_cases:
            return True

        if  len(lst) < 2:
            return False

        number_of_elements = int(lst[0])
        elements = lst[1]
        elements = elements.strip().split()

        if number_of_elements != len(elements):
            return False

        # apply power of four  on negative numbers
        f_numbers =  list(map(lambda x : int(x)**4 if int(x) < 0 else 0, elements))

        #Recursive sum with lambda function
        sum_of_f_numbers = lambda lst : 0 if not lst else lst[0] + sum_of_f_numbers(lst[1:])
        total_sum += sum_of_f_numbers(f_numbers)
        completed +=1


        return perform_test_case(lst[2:])


    if not perform_test_case(values[1:]):
        return -1
    return total_sum







if __name__=="__main__":
   values = sys.stdin.read().splitlines()
   result = main(values)
   print(result)
