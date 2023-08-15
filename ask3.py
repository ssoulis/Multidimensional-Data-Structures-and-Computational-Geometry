import math
import matplotlib.pyplot as plt
import time
import random

def orientation(p, q, r):
    # To find orientation of ordered triplet (p, q, r).
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])     #determine whether three points are collinear, clockwise, or counterclockwise in order
    if val == 0:        # colinear
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise is 1 or Counterclockwise  is 2

def graham_scan(points):        #graham scan algorithm
    n = len(points)             #number of points
    if n < 3:                   #if less than 3 points return points
        return points           #return points
    
    # Find the point with the lowest y-coordinate (and leftmost if tied)
    lowest = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort the points based on polar angle with respect to the lowest point
    sorted_points = sorted(points, key=lambda p: (math.atan2(p[1] - lowest[1], p[0] - lowest[0]), p))
    
    # Consider the first three points and initialize the stack
    convex_hull = [sorted_points[0], sorted_points[1]]


    # Build the convex hull
    for i in range(2, n):                           #for every point
        while len(convex_hull) > 1 and orientation(convex_hull[-2], convex_hull[-1], sorted_points[i]) != 2:    #while the last 2 points and the current point are not clockwise
            convex_hull.pop()                       #pop the last point
        convex_hull.append(sorted_points[i])        #append the current point
    
    return convex_hull                              #return the convex hull



def jarvis_march(points):                           #jarvis march algorithm
    n = len(points)                                 #number of points
    if n < 3:                                       #if less than 3 points return points
        return points                               #return points             
    
    hull = []                                       #initialize hull
    
    leftmost = min(points, key=lambda p: p[0])      #find the leftmost point
    hull.append(leftmost)                           #append the leftmost point
    
    current = leftmost                              #current point is the leftmost point
    while True:                                     #while true
        next_point = points[0]                      #next point is the first point
        for point in points[1:]:                    #for every point
            if point == current:                    #if the point is the current point continue
                continue                            #continue
            turn = orientation(current, next_point, point)    #find the orientation of the current point, the next point and the point
            if turn == 2 or (turn == 0 and distance(current, point) > distance(current, next_point)):       #if the point is counterclockwise or the point is colinear and the distance of the point from the current point is greater than the distance of the next point from the current point
                next_point = point          #the next point is the point
        if next_point == leftmost:          #if the next point is the leftmost point break
            break   
        hull.append(next_point)             #append the next point
        current = next_point                #the current point is the next point
    
    return hull                             #return the hull

def distance(p, q):                         #distance between 2 points
    return (q[0] - p[0])**2 + (q[1] - p[1])**2        # calculate the squared Euclidean distance between two points

def quickhull(points):                      #quickhull algorithm
    if len(points) <= 3:                    #if less than 3 points
        return points           
    
    leftmost = min(points, key=lambda p: p[0])          #find the leftmost point
    rightmost = max(points, key=lambda p: p[0])         #find the rightmost point
    convex_hull = [leftmost, rightmost]                 #initialize the convex hull
    
    points_above = [p for p in points if orientation(leftmost, rightmost, p) == 1]          #find the points above the line
    points_below = [p for p in points if orientation(leftmost, rightmost, p) == 2]          #find the points below the line
    
    quickhull_recursive(convex_hull, points_above, leftmost, rightmost)        #call the recursive function for the points above the line
    quickhull_recursive(convex_hull, points_below, rightmost, leftmost)        #call the recursive function for the points below the line
    
    return convex_hull

def quickhull_recursive(convex_hull, points, p1, p2):           #recursive function for quickhull
    if not points:                                              #if there are no points return
        return
    
    farthest = max(points, key=lambda p: quickhull_distance(p1, p2, p))         #find the farthest point from the line
    convex_hull.insert(convex_hull.index(p2), farthest)                         #insert the farthest point to the convex hull

    points_above = [p for p in points if orientation(p1, farthest, p) == 1]     #find the points above the line
    points_below = [p for p in points if orientation(farthest, p2, p) == 1]     #find the points below the line
    
    quickhull_recursive(convex_hull, points_above, p1, farthest)                #call the recursive function for the points above the line
    quickhull_recursive(convex_hull, points_below, farthest, p2)                #call the recursive function for the points below the line

def quickhull_distance(p1, p2, p):                                              #distance between a point and a line
    return abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1]))             #calculate the distance between a point and a line


# Example inputs
example_points = [
    [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)],
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (1, 5), (5, 1)],
]



# Calculate and print convex hulls using αλλ algorithms for each example
for i, points in enumerate(example_points, start=1):
    print(f"Example {i} - Input Points:", points)
    
    graham_hull = graham_scan(points)
    print(f"Graham Scan Convex Hull:", graham_hull)
    
    jarvis_hull = jarvis_march(points)
    print(f"Jarvis March Convex Hull:", jarvis_hull)

    quickhull_hull = quickhull(points)
    print(f"Quickhull Convex Hull:", quickhull_hull)
    
    print()




# Generate a large dataset of random points
large_dataset = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(1000)]

# Measure and print execution times for each algorithm using the large dataset
print("Large Dataset - Number of Points:", len(large_dataset))


# Visualize all examples in separate subplots

num_examples = len(example_points)                      #number of examples
rows = math.ceil(num_examples / 2)                      #number of rows

plt.figure(figsize=(12, 8))                             #figure size         

for i, points in enumerate(example_points, start=1):    #for every example
    plt.subplot(rows, 2, i)                             #subplot             
    
    convex_hull = graham_scan(points)                   #call the graham scan algorithm
    
    # Plot input points
    x, y = zip(*points)                                         #x and y coordinates             
    plt.scatter(x, y, color='blue', label='Input Points')       #plot the points
    
    # Plot convex hull points
    x_hull, y_hull = zip(*convex_hull)                          #x and y coordinates of the convex hull
    plt.plot(x_hull + (x_hull[0],), y_hull + (y_hull[0],), color='red', label='Convex Hull')        #plot the convex hull
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Example {i}')
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()

# Visualize convex hulls using Jarvis March in separate subplots
num_examples = len(example_points)                               #number of examples               
rows = math.ceil(num_examples / 2)                               #number of rows                  

plt.figure(figsize=(12, 8))                                      #figure size                                

for i, points in enumerate(example_points, start=1):             #for every example
    plt.subplot(rows, 2, i)                                      #subplot 
    
    hull = jarvis_march(points)                                  #call the jarvis march algorithm
    
    # Plot input points
    x, y = zip(*points)
    plt.scatter(x, y, color='blue', label='Input Points')
    
    # Plot convex hull points
    x_hull, y_hull = zip(*hull)
    plt.plot(x_hull + (x_hull[0],), y_hull + (y_hull[0],), color='green', label='Jarvis Hull')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Example {i} (Jarvis March)')
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()

# Visualize convex hulls using Quickhull in separate subplots
num_examples = len(example_points)
rows = math.ceil(num_examples / 2)

plt.figure(figsize=(12, 8))

for i, points in enumerate(example_points, start=1):
    plt.subplot(rows, 2, i)
    
    hull = quickhull(points)
    
    # Plot input points
    x, y = zip(*points)
    plt.scatter(x, y, color='blue', label='Input Points')
    
    # Plot convex hull points
    x_hull, y_hull = zip(*hull)
    plt.plot(x_hull + (x_hull[0],), y_hull + (y_hull[0],), color='purple', label='Quickhull Hull')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Example {i} (Quickhull)')
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()



# Visualize convex hulls using all three algorithms in separate plots
num_examples = 2  # we'll show only 2 examples due to space constraints
rows = math.ceil(num_examples / 2)

plt.figure(figsize=(12, 8))

# Example 1: Randomly generated points
points = large_dataset
plt.subplot(rows, 2, 1)


# Plot input points
x, y = zip(*points)
plt.scatter(x, y, color='blue', label='Input Points')

# Graham Scan
start_time_graham = time.time()                         #start time
graham_hull = graham_scan(points)                       #call the graham scan algorithm
graham_time = time.time() - start_time_graham           #end time - start time

# Jarvis March
start_time_jarvis = time.time()
jarvis_hull = jarvis_march(points)
jarvis_time = time.time() - start_time_jarvis

# Quickhull
start_time_quickhull = time.time()
quickhull_hull = quickhull(points)
quickhull_time = time.time() - start_time_quickhull

# Plot convex hull points for all algorithms
x_graham, y_graham = zip(*graham_hull)              #x and y coordinates of the graham hull
plt.plot(x_graham + (x_graham[0],), y_graham + (y_graham[0],), color='red', label='Graham Hull')

x_jarvis, y_jarvis = zip(*jarvis_hull)              #x and y coordinates of the jarvis hull
plt.plot(x_jarvis + (x_jarvis[0],), y_jarvis + (y_jarvis[0],), color='green', label='Jarvis Hull')

x_quickhull, y_quickhull = zip(*quickhull_hull)     #x and y coordinates of the quickhull hull
plt.plot(x_quickhull + (x_quickhull[0],), y_quickhull + (y_quickhull[0],), color='purple', label='Quickhull Hull')

plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Example 1 - Large Dataset (1000 points)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# Create a bar chart to compare execution times
algorithms = ["Graham Scan", "Jarvis March", "Quickhull"]           
times = [graham_time, jarvis_time, quickhull_time]

plt.bar(algorithms, times, color=['red', 'green', 'purple'])
plt.xlabel('Algorithms')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison for Convex Hull Algorithms')
plt.show()

# Print the slowest and the fastest algorithms
algorithm_times = {"Graham Scan": graham_time, "Jarvis March": jarvis_time, "Quickhull": quickhull_time}
slowest_algorithm = max(algorithm_times, key=algorithm_times.get)
fastest_algorithm = min(algorithm_times, key=algorithm_times.get)

print("Algorithm Execution Times:")
for algorithm, time in algorithm_times.items():
    print(f"{algorithm}: {time:.6f} seconds")

print()
print(f"The slowest algorithm is {slowest_algorithm}.")         
print(f"The fastest algorithm is {fastest_algorithm}.")

# Calculate and print how much faster the fastest algorithm is compared to the slowest algorithm
speedup_factor = algorithm_times[slowest_algorithm] / algorithm_times[fastest_algorithm]
print(f"{fastest_algorithm} is {speedup_factor:.2f} times faster than {slowest_algorithm}.")

