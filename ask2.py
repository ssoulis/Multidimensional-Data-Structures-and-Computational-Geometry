from intervaltree import Interval, IntervalTree
import time
import numpy as np
import matplotlib.pyplot as plt

num_iterations = 10         # Number of iterations to repeat the experiment

# Class to represent a segment tree
class SegmentTree:
    def __init__(self, arr):                                     # Constructor
        self.arr = arr                                           # Store the input array
        self.tree = [0] * (4 * len(arr))                         # Assuming maximum tree size
        self.build_tree(0, 0, len(arr) - 1)                      # Build the segment tree
        
    # funtion Build the segment tree
    def build_tree(self, node, start, end):                     # node is the index of the current node in the tree
        if start == end:                                        # Base case                
            self.tree[node] = self.arr[start]                   # Store value in tree node
        else:                                                   # Recursive step
            mid = (start + end) // 2                            # Calculate the mid point
            self.build_tree(2 * node + 1, start, mid)           # Build left subtree
            self.build_tree(2 * node + 2, mid + 1, end)         # Build right subtree
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2] # Store the sum of the left and right subtrees in the current node

    # Function to update the segment tree
    def update(self, node, start, end, index, value):   
        if start == end:                                        # Base case
            self.arr[index] = value                             # Update the array
            self.tree[node] = value                             # Update the tree node
        else:
            mid = (start + end) // 2                            # Calculate the mid point
            if index <= mid:
                self.update(2 * node + 1, start, mid, index, value)                     # Update the left subtree   
            else:
                self.update(2 * node + 2, mid + 1, end, index, value)                   # Update the right subtree
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]         # Update the current node


    def query(self, node, start, end, left, right):
        if left > end or right < start:                             # If the query range is outside the current node range
            return 0                                                # Return 0
        if left <= start and right >= end:                                  # If the query range is inside the current node range
            return self.tree[node]                                          # Return the value of the current node
        
        mid = (start + end) // 2                                            # Calculate the mid point
        left_sum = self.query(2 * node + 1, start, mid, left, right)        # Query the left subtree
        right_sum = self.query(2 * node + 2, mid + 1, end, left, right)     # Query the right subtree
        return left_sum + right_sum                                         # Return the sum of the left and right subtree



    def measure_build_time(self, num_iterations):
        timings = []                                                        # List to store timings

        for _ in range(num_iterations):                                     # Repeat the experiment num_iterations times
            start_time = time.time()                                        # Measure start time
            self.build_tree(0, 0, len(self.arr) - 1)                        # Build the segment tree
            end_time = time.time()                                          # Measure end time

            elapsed_time = end_time - start_time                            # Calculate the elapsed time
            timings.append(elapsed_time)                                    # Store the elapsed time

        average_time = np.mean(timings)                                     # Calculate the average time
        return average_time                                                 # Return the average time

    def measure_insertion_time(self, num_iterations):
        timings = []

        for _ in range(num_iterations):
            start_time = time.time()
            
            # Perform insertion operation (update all elements)
            for i in range(len(self.arr)):                                      # Repeat the experiment num_iterations times
                self.update(0, 0, len(self.arr) - 1, i, self.arr[i])            # Insert the interval and update the tree

            end_time = time.time()                                              # Measure end time
            elapsed_time = end_time - start_time                                # Calculate the elapsed time
            timings.append(elapsed_time)                                        # Store the elapsed time

        average_time = np.mean(timings)                                         # Calculate the average time
        return average_time 
    
    def measure_deletion_time(self, intervals, num_iterations):                 # num_iterations is the number of times to repeat the experiment
        timings = []                                                            # List to store timings 

        for _ in range(num_iterations):                                         # Repeat the experiment num_iterations times
            start_time = time.time()                                            # Measure start time
            
            # Build the segment tree with the intervals
            self.build_tree(0, 0, len(intervals) - 1)                           # Build the segment tree
            
            # Perform deletion operation (remove all intervals)
            for interval in intervals:
                self.update(0, 0, len(intervals) - 1, interval[0], 0)           # Update with 0 to simulate deletion

            end_time = time.time()
            elapsed_time = end_time - start_time
            timings.append(elapsed_time)

        average_time = np.mean(timings)
        return average_time
    

    def measure_query_time(self, num_iterations, query_ranges):
        timings = []

        for _ in range(num_iterations):
            total_query_time = 0

            for query_range in query_ranges:  # Repeat the experiment num_iterations times
                start_time = time.time()

                for left, right in query_range:
                    self.query(0, 0, len(self.arr) - 1, left, right)  # Query the tree

                end_time = time.time()
                query_time = end_time - start_time
                total_query_time += query_time

            average_query_time = total_query_time / len(query_ranges)
            timings.append(average_query_time)

        average_time = np.mean(timings)
        return average_time

    def measure_update_time(self, num_iterations, indices, values):
        timings = []

        for _ in range(num_iterations):                                 # Repeat the experiment num_iterations times
            start_time = time.time()                                    # Measure start time

            for index, value in zip(indices, values):                   # Update each interval
                self.update(0, 0, len(self.arr) - 1, index, value)      # Update the tree

            end_time = time.time()                                      # Measure end time
            elapsed_time = end_time - start_time                        # Calculate the elapsed time
            timings.append(elapsed_time)                                # Store the elapsed time    

        average_time = np.mean(timings)
        return average_time
   
# Function to measure interval tree build time
def measure_interval_tree_build_performance(interval_list, num_iterations):
    timings = []
    
    for _ in range(num_iterations):                         # Repeat the experiment num_iterations times
        start_time = time.time()                            # Measure start time
        tree = IntervalTree(interval_list)                  # Build the interval tree
        end_time = time.time()                              # Measure end time
        
        elapsed_time = end_time - start_time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings)
    return average_time

# Function to measure insertion performance of segment tree
def measure_insertion_performance(interval_list, num_iterations):    # num_iterations is the number of times to repeat the experiment
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

# Function to measure deletion performance for interval tree
def measure_deletion_performance(interval_list, num_iterations): # num_iterations is the number of times to repeat the experiment
    timings = []
    tree = IntervalTree()

        
    for _ in range(num_iterations): # Repeat the experiment num_iterations times
        for interval in interval_list:  # Insert each interval into the tree
            tree.add(interval)          # Insert the interval
        
        start_time = time.time()        # Measure start time
        for interval in interval_list:  # Delete each interval from the tree
            tree.remove(interval)       # Delete the interval
        end_time = time.time()          # Measure end time
        
        elapsed_time = end_time - start_time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings)     # Calculate the average time
    return average_time

def measure_interval_tree_update_time(interval_list, num_iterations):
    timings = []
    
    for _ in range(num_iterations):
        tree = IntervalTree(interval_list)  # Build the initial interval tree
        start_time = time.time()
        
        for i, interval in enumerate(interval_list):                                    # Update each interval
            updated_interval = Interval(interval.begin + 0.5, interval.end + 0.5)       # Update the interval
            tree.remove(interval)                                                       # Remove the old interval from the tree
            tree.add(updated_interval)                                                  # Add the updated interval back to the tree
            interval_list[i] = updated_interval                                         # Update the interval list
            
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        timings.append(elapsed_time)
    
    average_time = np.mean(timings)
    return average_time




# Function to measure query performance for overlapping intervals
def measure_query_overlap_performance(tree, query_intervals, num_iterations):    # num_iterations is the number of times to repeat the experiment
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

# Function to measure query performance for containing a point on interval tree
def measure_query_point_performance(tree, query_points, num_iterations):   # num_iterations is the number of times to repeat the experiment
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

 #num_queries = 100 # Number of range queries to test

insert_timings = []                     # List to store insertion timings
delete_timings = []                     # List to store deletion timings
interval_update_timings = []            # List to store interval tree update timings
query_overlap_timings = []              # List to store query overlap timings
query_point_timings = []                # List to store query point timings
expected_timings = []                   # List to store expected O(log N) timings
interval_tree_build = []                # List to store interval tree build timings
segment_tree_build_timings = []         # List to store segment tree build timings
segment_tree_insert_timings = []        # List to store segment tree insertion timings
segment_tree_query_timings = []         # List to store segment tree query timings
segment_tree_deletion_timings = []      # List to store segment tree query timings
update_timings = []                     # List to store segment tree update timings






    # Measure performance for each number of intervals
for num in num_intervals:
    intervals = [Interval(i, i+1) for i in range(num)]  # Generate intervals

    segment_tree = SegmentTree([0] * num) # Create a segment tree with num elements
    

    # Measure segment tree build time using the new function
    build_time = segment_tree.measure_build_time(num_iterations)
    segment_tree_build_timings.append(build_time)
    print(f"Segment Tree Build time for {num} elements: {build_time:.6f} seconds")

    # Measure segment tree insertion time using the new function
    insertion_time = segment_tree.measure_insertion_time(num_iterations)
    segment_tree_insert_timings.append(insertion_time)
    print(f"Segment Tree Insertion time for {num} elements: {insertion_time:.6f} seconds")

    # Measure segment tree deletion time using the new function
    deletion_time = segment_tree.measure_deletion_time(intervals, num_iterations)
    segment_tree_deletion_timings.append(deletion_time)
    print(f"Segment Tree Deletion time for {num} intervals: {deletion_time:.6f} seconds")



    # Measure segment tree query time using the new function
    query_ranges = [[(i, i+1)] for i in range(num)]
    query_time = segment_tree.measure_query_time(num_iterations, query_ranges)
    segment_tree_query_timings.append(query_time)
    print(f"Segment Tree Query time for {num} intervals: {query_time:.6f} seconds")

    # Measure segment tree update time using the new function
    indices = [i for i in range(num)]
    values = [1] * num
    update_time = segment_tree.measure_update_time(num_iterations, indices, values)
    update_timings.append(update_time)
    print(f"Segment Tree Update time for {num} intervals: {update_time:.6f} seconds")

    # Measure interval tree build performance
    interval_tree_build_time = measure_interval_tree_build_performance(intervals, num_iterations)
    print(f"Interval Tree Build time for {num} intervals: {interval_tree_build_time:.6f} seconds")
    interval_tree_build.append(interval_tree_build_time)  # Store interval tree build time

    # Measure interval tree insertion performance
    insert_time = measure_insertion_performance(intervals, num_iterations) # Measure insertion performance
    insert_timings.append(insert_time)                                      # Store the average insertion time
    print(f"Insertion time for {num} intervals: {insert_time:.6f} seconds") 
    
    # Measure interval tree deletion performance
    delete_time = measure_deletion_performance(intervals, num_iterations)       
    delete_timings.append(delete_time)                                          
    print(f"Deletion time for {num} intervals: {delete_time:.6f} seconds")

    # Measure interval tree update performance
    interval_tree_update_time = measure_interval_tree_update_time(intervals, num_iterations)
    interval_update_timings.append(interval_tree_update_time)
    print(f"Interval Tree Update time for {num} intervals: {interval_tree_update_time:.6f} seconds")
    

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

# Plot the results of Interval tree
plt.figure(figsize=(10, 8))
plt.plot(num_intervals, insert_timings, marker='o', label='Insertion')
plt.plot(num_intervals, delete_timings, marker='o', label='Deletion')
plt.plot(num_intervals, query_overlap_timings, marker='o', label='Query Overlap')
plt.plot(num_intervals, query_point_timings, marker='o', label='Query Point')
plt.plot(num_intervals, expected_timings, linestyle='dashed', label='Expected O(log N)')
plt.plot(num_intervals, interval_tree_build, marker='o', label='Build')
plt.plot(num_intervals, interval_update_timings, marker='o', label='Update')
plt.xlabel('Number of Intervals')
plt.ylabel('Average Time (seconds)')
plt.title('Interval Tree Performance')
plt.legend()
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.grid(True)
plt.tight_layout()
plt.show()


# Plot segment tree build and query performance in Figure 2
plt.figure(figsize=(10, 8))

# Plot segment tree build performance
plt.plot(num_intervals, segment_tree_build_timings, marker='o', label='Segment Tree Build')
plt.plot(num_intervals, segment_tree_query_timings, marker='o', label='Segment Tree Query')
plt.plot(num_intervals, segment_tree_insert_timings, marker='o', label='Segment Tree Insertion')
plt.plot(num_intervals, segment_tree_deletion_timings, marker='o', label='Segment Tree Deletion')
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
efficiency_build = [interval_tree_build[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_insertion = [insert_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_deletion = [delete_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
eficienency_update = [interval_update_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_query_overlap = [query_overlap_timings[i] / expected_timings[i] for i in range(len(num_intervals))]
efficiency_query_point = [query_point_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate segment tree build efficiencies
segment_tree_build_efficiencies = [segment_tree_build_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate segment tree insertion efficiencies
segment_tree_insert_efficiencies = [segment_tree_insert_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate segment tree deletion efficiencies
segment_tree_query_delete_efficiencies = [segment_tree_deletion_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

# Calculate efficiency for segment tree query
efficiency_segment_tree_query = [segment_tree_query_timings[i] / expected_timings[i] for i in range(len(num_intervals))]

#Calculate efficiency for segment tree update
efficiency_update = [update_timings[i] / expected_timings[i] for i in range(len(num_intervals))]


# Print efficiency for each method of Interval Tree
print("\nEfficiency for Interval Tree Build: ")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_build[i]:.3f}")
   

print("\nEfficiency for Interval Tree Insertion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_insertion[i]:.3f}")

print("\nEfficiency for Interval Tree Deletion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {efficiency_deletion[i]:.3f}")

print("\nEfficiency for Interval Tree Update:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {eficienency_update[i]:.3f}")

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

# Print segment tree insertion efficiencies
print("Efficiency for Segment Tree Insertion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {segment_tree_insert_efficiencies[i]:.3f}")
print()

# Print segment tree deletion efficiencies
print("Efficiency for Segment Tree Deletion:")
for i in range(len(num_intervals)):
    print(f"Num Intervals: {num_intervals[i]}, Efficiency: {segment_tree_query_delete_efficiencies[i]:.3f}")
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


# Create a bar chart to compare execution times
algorithms = ["IntervalBuild","SegmentBuild", "IntervalInsert","SegmentInsert", "IntervalDelete","SegmentDelete", "IntervalUpdate","SegmentUpdate", "IntervalQuery", "SegmentQuery"]           
times = [interval_tree_build[-1], segment_tree_build_timings[-1], insert_timings[-1], segment_tree_insert_timings[-1], delete_timings[-1], segment_tree_deletion_timings[-1], interval_update_timings[-1], update_timings[-1], query_overlap_timings[-1], segment_tree_query_timings[-1]]

plt.figure(figsize=(10, 8))
plt.bar(algorithms, times, color=['red', 'green'])
plt.xlabel('Algorithms')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison of Interval and Segment trees for 10000 intervals')
plt.show()