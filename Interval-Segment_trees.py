from intervaltree import Interval, IntervalTree
import time
import numpy as np
import matplotlib.pyplot as plt

# Class to represent a segment tree
class SegmentTree:
    def __init__(self, arr): # Constructor
        self.arr = arr      # Store the input array
        self.tree = [0] * (4 * len(arr))  # Assuming maximum tree size
        self.build_tree(0, 0, len(arr) - 1) # Build the segment tree
        
        
    def build_tree(self, node, start, end): # Build the segment tree
        if start == end:    # Leaf node
            self.tree[node] = self.arr[start]   # Store value in tree node
        else:   # Recursive step
            mid = (start + end) // 2    # Calculate the mid point
            self.build_tree(2 * node + 1, start, mid)
            self.build_tree(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def query(self, node, start, end, left, right): # Query the segment tree
        if left > end or right < start: # No overlap
            return 0
        if left <= start and right >= end: # Complete overlap
            return self.tree[node]
        
        mid = (start + end) // 2        # Partial overlap
        left_sum = self.query(2 * node + 1, start, mid, left, right)    # Query left child
        right_sum = self.query(2 * node + 2, mid + 1, end, left, right) # Query right child
        return left_sum + right_sum     # Return sum of left and right child

        
    def update(self, node, start, end, index, value): # Update the segment tree
        if start == end:        # Leaf node
            self.arr[index] = value     # Update the input array
            self.tree[node] = value     # Update the tree node
        else:
            mid = (start + end) // 2        # Calculate the mid point
            if index <= mid:                # Index is in the left child
                self.update(2 * node + 1, start, mid, index, value)     # Update left child
            else:
                self.update(2 * node + 2, mid + 1, end, index, value)   # Update right child    
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]     # Update the tree node

   


# Function to measure insertion performance
def measure_insertion_performance(interval_list, num_iterations=10):    # num_iterations is the number of times to repeat the experiment
    timings = []             # List to store timings
    tree = IntervalTree()    # Create an empty interval tree

        # Build the segment tree
    for _ in range(num_iterations): # Repeat the experiment num_iterations times
        start_time = time.time()    # Measure start time
        for interval in interval_list:  # Insert each interval into the tree
            tree.add(interval)      # Insert the interval
        end_time = time.time()      # Measure end time
        
        elapsed_time = end_time - start_time # Calculate the elapsed time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings) # Calculate the average time
    return average_time

# Function to measure deletion performance
def measure_deletion_performance(interval_list, num_iterations=10): # num_iterations is the number of times to repeat the experiment
    timings = []
    tree = IntervalTree()

        #
    for _ in range(num_iterations): # Repeat the experiment num_iterations times
        for interval in interval_list:  # Insert each interval into the tree
            tree.add(interval)          # Insert the interval
        
        start_time = time.time()        # Measure start time
        for interval in interval_list:  
            tree.remove(interval)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings)     # Calculate the average time
    return average_time

# Function to measure query performance for overlapping intervals
def measure_query_overlap_performance(tree, query_intervals, num_iterations=10):    # num_iterations is the number of times to repeat the experiment
    timings = []
    
    for _ in range(num_iterations): # Repeat the experiment num_iterations times
        start_time = time.time()    
        for query_interval in query_intervals:  # Query each interval
            result = tree.overlap(query_interval.begin, query_interval.end) # Query the tree
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings)
    return average_time

# Function to measure query performance for containing a point
def measure_query_point_performance(tree, query_points, num_iterations=10):   # num_iterations is the number of times to repeat the experiment
    timings = []
        
    for _ in range(num_iterations):
        start_time = time.time()
        for query_point in query_points:   # query points are the midpoints of the intervals
            result = tree.overlap(query_point, query_point)
        end_time = time.time() # Measure end time
        
        elapsed_time = end_time - start_time # Calculate the elapsed time
        timings.append(elapsed_time) # Store the elapsed time
    
    average_time = np.mean(timings)
    return average_time

# Number of intervals to test
num_intervals = [100, 500, 1000, 2000, 5000, 10000]

num_queries = 100 # Number of range queries to test

insert_timings = []     # List to store insertion timings
delete_timings = []     # List to store deletion timings
query_overlap_timings = []  # List to store query overlap timings
query_point_timings = []    # List to store query point timings
expected_timings = []       # List to store expected O(log N) timings
segment_tree_build_timings = []     # List to store segment tree build timings
segment_tree_query_timings = []     # List to store segment tree query timings
update_timings = []         # List to store segment tree update timings


num_iterations = 10         # Number of iterations to average timings over


    # Measure performance for each number of intervals
for num in num_intervals:
    intervals = [Interval(i, i+1) for i in range(num)]

    # Measure segment tree build time
    start_time = time.time()
    segment_tree = SegmentTree([1] * num)  # You can adjust input array as needed
    end_time = time.time()      # Measure end time
    build_time = end_time - start_time # Calculate build time
    segment_tree_build_timings.append(build_time) # Store build time
    print(f"Segment Tree Build time for {num} elements: {build_time:.6f} seconds") # Print build time
    print()

    # Generate range queries and measure query time for segment tree
    query_ranges = [(np.random.randint(0, num - 1), np.random.randint(0, num - 1)) for _ in range(num_queries)]
    total_query_time = 0
    for query_range in query_ranges:    # Repeat the experiment num_queries times
        total_query_sum = 0
        start_time = time.time()
        for i in range(query_range[0], query_range[1] + 1):     # Query each index in the range
          total_query_sum += segment_tree.arr[i]                # Add the value at the index to the total
        end_time = time.time()                                  # Measure end time
        query_time = end_time - start_time                      # Calculate the elapsed time
        total_query_time += query_time                          # Add the elapsed time to the total
    average_query_time = total_query_time / num_queries         # Calculate the average query time
    segment_tree_query_timings.append(average_query_time)       # Store the average query time
    print(f"Query time for {num} elements: {average_query_time:.6f} seconds")

    # Measure segment tree update time
    total_update_time = 0
    for i in range(num):
        start_time = time.time()
        segment_tree.update(0, 0, num - 1, i, 2)  # Update index i with value 2
        end_time = time.time()
        update_time = end_time - start_time
        total_update_time += update_time
    average_update_time = total_update_time / num
    update_timings.append(average_update_time)      # Store the average update time
    print(f"Update time for {num} elements: {average_update_time:.6f} seconds")

    # Measure insertion performance
    insert_time = measure_insertion_performance(intervals, num_iterations) # Measure insertion performance
    insert_timings.append(insert_time)                                      # Store the average insertion time
    print(f"Insertion time for {num} intervals: {insert_time:.6f} seconds") 
    
    # Measure deletion performance
    delete_time = measure_deletion_performance(intervals, num_iterations)       
    delete_timings.append(delete_time)                                          
    print(f"Deletion time for {num} intervals: {delete_time:.6f} seconds")
    
    # Measure query performance for overlapping intervals
    tree = IntervalTree(intervals)                                      # Build the interval tree
    query_intervals = [Interval(i-0.5, i+0.5) for i in range(num)]      # Generate query intervals
    query_overlap_time = measure_query_overlap_performance(tree, query_intervals, num_iterations)   # Measure query performance
    query_overlap_timings.append(query_overlap_time)        # Store the average query time
    print(f"Query Overlap time for {num} intervals: {query_overlap_time:.6f} seconds")
    
    # Measure query performance for containing a point
    query_points = [i + 0.5 for i in range(num)]                # Generate query points
    query_point_time = measure_query_point_performance(tree, query_points, num_iterations)      # Measure query performance
    query_point_timings.append(query_point_time)
    print(f"Query Point time for {num} intervals: {query_point_time:.6f} seconds")
    
    # Calculate the expected O(log N) time
    expected_time = np.log2(num) * (insert_time + delete_time) / (2 * np.log2(2))
    expected_timings.append(expected_time)
    print(f"Expected time for {num} intervals: {expected_time:.6f} seconds")
    print()

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(num_intervals, insert_timings, marker='o', label='Insertion')
plt.plot(num_intervals, delete_timings, marker='o', label='Deletion')
plt.plot(num_intervals, query_overlap_timings, marker='o', label='Query Overlap')
plt.plot(num_intervals, query_point_timings, marker='o', label='Query Point')
plt.plot(num_intervals, expected_timings, linestyle='dashed', label='Expected O(log N)')
plt.xlabel('Number of Intervals')
plt.ylabel('Average Time (seconds)')
plt.title('Interval Tree Performance')
plt.legend()
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.grid(True)
plt.show()


# Plot segment tree build and query performance in Figure 2
plt.figure(figsize=(10, 6))

# Plot segment tree build performance
plt.plot(num_intervals, segment_tree_build_timings, marker='o', label='Segment Tree Build')
plt.plot(num_intervals, segment_tree_query_timings, marker='o', label='Segment Tree Query')
plt.plot(num_intervals, update_timings, marker='o', label='Segment Tree Update')
plt.plot(num_intervals, expected_timings, linestyle='dashed', label='Expected O(log N) Build')
plt.xlabel('Number of Elements')
plt.ylabel('Time (seconds)')
plt.title('Segment Tree Performance')
plt.legend()
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.grid(True)


plt.tight_layout()
plt.show()

# Calculate efficiency
efficiency_insertion = [insert_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_deletion = [delete_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_query_overlap = [query_overlap_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_query_point = [query_point_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate segment tree build efficiencies
segment_tree_build_efficiencies = [segment_tree_build_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate efficiency for segment tree query
efficiency_segment_tree_query = [segment_tree_query_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

#Calculate efficiency for segment tree update
efficiency_update = [update_timings[i] / expected_timings[i] for i in range(len(num_intervals))]


# Print efficiency for each method
print("Efficiency for Interval Tree Insertion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_insertion[i]:.3f}")

print("\nEfficiency for Interval Tree Deletion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_deletion[i]:.3f}")

print("\nEfficiency for Interval Tree Query Overlap:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_query_overlap[i]:.3f}")

print("\nEfficiency for Interval Tree Query Point:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_query_point[i]:.3f}")

# Print segment tree build efficiencies
print()
print("Efficiency for Segment Tree Build:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {segment_tree_build_efficiencies[i]:.3f}")
print()

# Print efficiency for segment tree query
print("Efficiency for Segment Tree Query:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_segment_tree_query[i]:.3f}")

# Print efficiency for segment tree update
print() 
print("Efficiency for Segment Tree Update:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_update[i]:.3f}")

