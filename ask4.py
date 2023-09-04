from sortedcontainers import SortedDict
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import time

# Define the vertices for polygons in 2D space
polygon_coords = [                       
    [(0, 0), (20, -20), (40, 0), (20, 20)],                 # Quadrilateral (4 sides)
    [(0, 0), (-20, 20), (-40, 0)],                         # Triangle (3 sides)                          
    [(0, 0), (20, 20), (20, 40), (-20, 30), (-20, 20)],     # Pentagon (5 sides)
    [(-60,0), (-50,-20),(-30,-20), (-20, 0)],              # Quadrilateral (4 sides)
    [(-20,20),(-20,30),(0,35),(-30,60)],                    # Quadrilateral (4 sides)           
    [(-120,70),(-90,55),(-70,70)],                          # Triangle (3 sides)
    [(-110,40),(-70,40) ,(-60,55),(-70,80),(-70,70)],       # Pentagon (5 sides)
    [(-90,70),(-70,70),(-70,90),(-90,90)]                   # Quadrilateral (4 sides)
]




# Define names for each polygon
polygon_names = ['Polygon A', 'Polygon B', 'Polygon C', 'Polygon D', 'Polygon E', 'Polygon F', 'Polygon G', 'Polygon H']

# Define colors for each polygon
polygon_colors = ['green', 'blue', 'purple', 'cyan', 'red', 'yellow', 'orange', 'pink']

# Create Shapely Polygon objects
polygons = [Polygon(coords) for coords in polygon_coords]     

start_time = time.time()                        # Start measuring the execution time

# Create a list to store line segments
line_segments = []

# Iterate over each polygon
for coords in polygon_coords:                            # Iterate over each polygon
    num_points = len(coords)                             # Number of vertices in the polygon
    for i in range(num_points):                          # Iterate over each vertex
        # Extract two consecutive vertices to define a line segment
        start_point = coords[i]                          # Current vertex
        end_point = coords[(i + 1) % num_points]         # Wrap around to the first vertex for the last segment
        
        # Create a LineString object from the two vertices
        line_segment = LineString([start_point, end_point])
        
        # Append the LineString to the list of line segments
        line_segments.append(line_segment)

# Dictionary to store overlapping points grouped by line segments
overlapping_groups = {}

# Start measuring the execution time


# Compare each line segment with all other line segments
for i, line_segment1 in enumerate(line_segments):                               # Iterate over each line segment
    for j, line_segment2 in enumerate(line_segments):                           # Iterate over each line segment
        if i != j and line_segment1.intersects(line_segment2):                  # Check if the line segments intersect
            overlap = line_segment1.intersection(line_segment2)                 # Find the intersection of the line segments
            if isinstance(overlap, LineString):                                 # Check if the intersection is a line segment
                start_point = overlap.coords[0]                                 # Start point of the line segment
                end_point = overlap.coords[-1]                                  # End point of the line segment
                if (start_point, end_point) not in overlapping_groups:          # Check if the line segment is already in the dictionary
                    overlapping_groups[(start_point, end_point)] = []           # Add the line segment to the dictionary
                overlapping_groups[(start_point, end_point)].append((line_segment1, line_segment2)) # Add the line segment pair to the dictionary

# Stop measuring the execution time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"\nElapsed Time: {elapsed_time:.6f} seconds")
print()

# Print the overlapping line segments and the polygons that share them
for segment_pair, overlapping_segments in overlapping_groups.items():           # Iterate over each overlapping line segment
    start_point, end_point = segment_pair                                       # Start and end points of the line segment
    print(f"Overlapping Line Segment: {start_point} to {end_point}")            # Print the line segment

    for line_segment_pair in overlapping_segments:                              # Iterate over each pair of line segments
        polygon_indices = []                                                    # List to store the indices of polygons that share the line segment pair
        for line_segment in line_segment_pair:                                  # Iterate over each line segment in the pair
            # Find the index of the line segment in line_segments
            index = line_segments.index(line_segment)                          
            
            # Find the polygons that share this line segment    
            for i, coords in enumerate(polygon_coords):                         # Iterate over each polygon
                if line_segment in [LineString([coords[j], coords[(j + 1) % len(coords)]]) for j in range(len(coords))]:        # Iterate over each line segment in the polygon
                    polygon_indices.append(i)                                   # Add the index of the polygon to the list
        
        polygon_names_str = ', '.join([polygon_names[i] for i in polygon_indices])      # Convert the list of polygon indices to a string
        print(f"  Polygons with adjacent borders: {polygon_names_str}")                 # Print the list of polygons that share the line segment pair
        print()



# Create a larger figure and axis for visualization
fig, ax = plt.subplots(figsize=(10, 10))

# Plot each polygon with its respective color and label
for polygon, color, name in zip(polygons, polygon_colors, polygon_names):               # Iterate over each polygon
    x, y = polygon.exterior.xy                                                          # Extract the x and y coordinates of the polygon
    ax.fill(x, y, color=color, alpha=0.5)                                               # Plot the polygon                     
    for i, (xi, yi) in enumerate(zip(x, y)):                                            # Iterate over each vertex in the polygon
        ax.annotate(f'({xi:.1f},{yi:.1f})', (xi, yi), textcoords="offset points", xytext=(0, 5), ha='center')   # Annotate the vertex with its coordinates
    centroid = polygon.centroid                                                         # Find the centroid of the polygon
    ax.text(centroid.x, centroid.y, name, fontsize=10, ha='center', va='center')

# Plot overlapping line segments with black lines
for segment_pair, _ in overlapping_groups.items():
    x_coords = [segment_pair[0][0], segment_pair[1][0]]
    y_coords = [segment_pair[0][1], segment_pair[1][1]]
    ax.plot(x_coords, y_coords, color='black',linestyle='dashed', label='Dashed Line', linewidth=2)

ax.set_aspect('equal')
plt.axis('on')  # Turn off axis
plt.show()

