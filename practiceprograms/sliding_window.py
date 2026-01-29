# Maintain a window [L..R] and move it to avoid recomputing

# Best for: Subarrays/substrings, “contiguous” problems (sum, length, counts).

# Sliding Window (Optimized)
def max_sum_sliding_window(arr, k):
    window_sum = sum(arr[:k])   # sum of first window
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i]        # add right element
        window_sum -= arr[i - k]    # remove left element
        max_sum = max(max_sum, window_sum)

    return max_sum



# Variable-Size Sliding Window Example
def longest_subarray_sum_k(arr, k):
    left = 0
    curr_sum = 0
    max_len = 0

    for right in range(len(arr)):
        curr_sum += arr[right]

        while curr_sum > k:
            curr_sum -= arr[left]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
