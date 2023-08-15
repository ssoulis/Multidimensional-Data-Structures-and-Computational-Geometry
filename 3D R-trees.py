from rtree import index
import matplotlib.pyplot as plt
import random
import math

class MovingObject:
    def __init__(self, object_id, x, y, start_time, end_time): #constructor
        self.object_id = object_id      # Unique identifier for the object
        self.x = x                      # X coordinate of the object
        self.y = y                      # Y coordinate of the object
        self.start_time = start_time    # Start time of the object trajectory
        self.end_time = end_time        # End time of the object trajectory

p = index.Property()                    # Create a new property object
p.dimension = 3                         # Use 3D for spatial dimensions plus time  
idx = index.Index(properties=p)         # Create a new index

num_objects = 200                       # Number of moving objects
moving_objects = []                     # List of moving objects

for i in range(num_objects):            # Generate random moving objects
    object_id = i                       # Unique identifier for the object
    x = random.uniform(0, 100)          # X coordinate of the object
    y = random.uniform(0, 100)          # Y coordinate of the object
    start_time = random.uniform(0, 100)             # Start time of the object trajectory
    end_time = start_time + random.uniform(0, 10)   # End time of the object trajectory
    moving_objects.append(MovingObject(object_id, x, y, start_time, end_time))          # Create a new moving object
    idx.insert(                 # Insert the object into the index
        object_id,
        (x, y, start_time, x, y, end_time)
    )

def nearest_neighbor_query(query_x, query_y, query_time):           # Nearest neighbor query
    query_range = 5  # Adjust this value based on your desired query range

    # Calculate a tighter bounding box based on the query range
    x_min = query_x - query_range   # Minimum x value
    x_max = query_x + query_range   # Maximum x value
    y_min = query_y - query_range   # Minimum y value
    y_max = query_y + query_range   # Maximum y value
    time_min = query_time           # Minimum time value
    time_max = query_time           # Maximum time value

    best_distance = float('inf')    # Initialize the best distance variable
    nearest_object = None           # Initialize the nearest object variable

    for obj_id in idx.intersection((x_min, y_min, time_min, x_max, y_max, time_max)):       # Iterate through all objects in the index
        obj = moving_objects[obj_id]                                            # Get the object from the list of moving objects
        distance = math.sqrt((query_x - obj.x)**2 + (query_y - obj.y)**2)       # Calculate the distance between the query point and the object
        if distance < best_distance:        # If the distance is better than the previous best distance
            best_distance = distance        # Update the best distance
            nearest_object = obj            # Update the nearest object 

    return nearest_object                   # Return the nearest object



# Example nearest neighbor queries
queries = [
    (50, 60, 30),
    (20, 70, 10),
    (80, 40, 50),
    (90, 90, 80),
    (30, 40, 70)
]

for query_x, query_y, query_time in queries:        # Iterate through all queries
    nearest_obj = nearest_neighbor_query(query_x, query_y, query_time)  # Perform a nearest neighbor query
    if nearest_obj:         # If a nearest object is found
        print(f"Nearest object to point ({query_x}, {query_y}) at time {query_time}: Object {nearest_obj.object_id}")
    else:
        print(f"No nearest object found for query at point ({query_x}, {query_y}) and time {query_time}.")


    #range query
def range_query(query_x_min, query_y_min, query_z_min, query_x_max, query_y_max, query_z_max, query_time_min, query_time_max):
    result_trajectories = []    # Initialize the result trajectories list

    query_box = (query_x_min, query_y_min, query_z_min, query_x_max, query_y_max, query_z_max)  # Create a query box

    for obj_id in idx.intersection(query_box):  # Iterate through all objects in the index
        obj = moving_objects[obj_id]            # Get the object from the list of moving objects
        if query_time_min <= obj.start_time <= query_time_max or query_time_min <= obj.end_time <= query_time_max:  # If the object trajectory intersects with the query time interval
            result_trajectories.append(obj)     # Add the object to the result trajectories list

    return result_trajectories



# Example nearest neighbor queries
queries = [
    (50, 60, 30),           # (x, y, time)
    (20, 70, 10),
    (80, 40, 50),
    (90, 90, 80),
    (30, 40, 70)
]

for query_x, query_y, query_time in queries:    # Iterate through all queries
    nearest_obj = nearest_neighbor_query(query_x, query_y, query_time)  # Perform a nearest neighbor query
    if nearest_obj:
        print(f"Nearest object to point ({query_x}, {query_y}) at time {query_time}: Object {nearest_obj.object_id}")   
        print(f"    Trajectory: Start time {nearest_obj.start_time}, End time {nearest_obj.end_time}")
    else:
        print(f"No nearest object found for query at point ({query_x}, {query_y}) and time {query_time}.")

# Example range query
query_x_min = 40            
query_x_max = 80
query_y_min = 20
query_y_max = 70
query_z_min = 0
query_z_max = 100
query_time_min = 20
query_time_max = 60

# Perform a range query
result_trajectories = range_query(query_x_min, query_y_min, query_z_min, query_x_max, query_y_max, query_z_max, query_time_min, query_time_max)

# Print the results
if result_trajectories:
    print("Trajectories that intersect with the query region and time interval:")
    print(f"Selected range is x from {query_x_min} to {query_x_max}, y from {query_y_min} to {query_y_max}, z from {query_z_min} to {query_z_max}, and time from {query_time_min} to {query_time_max}.")
    for traj in result_trajectories:
        print(f"Trajectory of object {traj.object_id}")
        print(f"    Start time {traj.start_time}, End time {traj.end_time}")
else:
    print("No trajectories found for the given query.")


def intersection_query():               # Intersection query
    intersecting_trajectories = []      # Initialize the intersecting trajectories list

    for i in range(len(moving_objects)):                    # Iterate through all objects in the list
        for j in range(i + 1, len(moving_objects)):         # Iterate through all objects after the current object
            obj1 = moving_objects[i]                        # Get the first object
            obj2 = moving_objects[j]                        # Get the second object    

            if (
                obj1.start_time <= obj2.end_time and         # If the trajectories intersect
                obj1.end_time >= obj2.start_time and         
                obj1.x <= obj2.x and obj1.y <= obj2.y and    
                obj1.x + (obj1.end_time - obj1.start_time) * (obj2.x - obj1.x) / (obj2.end_time - obj2.start_time) >= obj2.x and # 
                obj1.y + (obj1.end_time - obj1.start_time) * (obj2.y - obj1.y) / (obj2.end_time - obj2.start_time) >= obj2.y       
            ):
                intersecting_trajectories.append((obj1, obj2))      # Add the intersecting trajectories to the list

    return intersecting_trajectories

# Example intersection query
intersection_results = intersection_query()     # Perform an intersection query

if intersection_results:                        # If intersecting trajectories are found
    print("Intersecting trajectories:")
    for traj1, traj2 in intersection_results:
        print(f"Trajectory of object {traj1.object_id} intersects with trajectory of object {traj2.object_id}")
        print(f"    Trajectory 1: Start time {traj1.start_time}, End time {traj1.end_time}")
        print(f"    Trajectory 2: Start time {traj2.start_time}, End time {traj2.end_time}")
else:
    print("No intersecting trajectories found.")




for query_x, query_y, query_time in queries:    # Iterate through all queries
    nearest_obj = nearest_neighbor_query(query_x, query_y, query_time)  # Perform a nearest neighbor query
    result_trajectories = range_query(query_x - 5, query_y - 5, 0, query_x + 5, query_y + 5, 100, query_time, query_time)   # Perform a range query
    
    plt.figure(figsize=(8, 6))          # Create a new figure

    for obj in moving_objects:          # Iterate through all objects
        plt.plot(obj.x, obj.y, marker='o', markersize=5, label=f'Object {obj.object_id}')
    
    if nearest_obj:                     # If a nearest object is found
        plt.plot(nearest_obj.x, nearest_obj.y, marker='x', markersize=10, label='Nearest Neighbor', color='red')
    
    for traj in result_trajectories:    # Iterate through all result trajectories
        plt.plot(traj.x, traj.y, marker='s', markersize=7, label=f'Result Trajectory {traj.object_id}', color='green')
    
    plt.plot(query_x, query_y, marker='*', markersize=10, label='Query Point', color='purple')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Query at Point ({query_x}, {query_y}) and Time {query_time}')
    plt.legend()
    plt.grid()
    plt.show()
    
