# Binary Search Variants

Status: done, in progress
Theme: Binary Search
Created time: December 29, 2023 4:25 PM
Last edited time: December 31, 2023 10:06 PM

Binary search is a powerful algorithm that is frequently adapted for various scenarios beyond just finding an element in a sorted array. Here are some of the most commonly used variants of binary search:

### 1. Standard Binary Search

Search for an element in a sorted array. If found, return its index; otherwise, return -1.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

```

### 2. Finding the First or Last Occurrence

Used when the array contains duplicates and you want to find the first or last occurrence of a target element.

```python
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Move left to find the first occurrence
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

```

### 3. Finding the Closest Element

Find the element in the array which is closest to the target value.

```python
def find_closest(arr, target):
    left, right = 0, len(arr) - 1
    closest = float('inf')
    while left <= right:
        mid = left + (right - left) // 2
        if abs(arr[mid] - target) < abs(closest - target):
            closest = arr[mid]
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return closest

```

### 4. Finding the Peak Element

Used in scenarios like finding a peak element in an array where an element is considered a peak if it is greater than its neighbors.

```python
def find_peak(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left

```

### 5. Binary Search on Answer

Used in scenarios where you need to decide if a condition can be satisfied (like allocating minimum pages, aggressive cows, etc.).

```python
def is_feasible(mid, condition):
    # Check if the condition is met for the value mid
    pass

def binary_search_on_answer(low, high, condition):
    while low < high:
        mid = low + (high - low) // 2
        if is_feasible(mid, condition):
            high = mid
        else:
            low = mid + 1
    return low

```

Each of these variants modifies the binary search in a way that it can be applied to a particular problem or scenario, showcasing the versatility and efficiency of the binary search algorithm.