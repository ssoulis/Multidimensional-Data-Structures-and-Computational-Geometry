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

start_time = time.time()  

# Create a list to store line segments
line_segments = []

start_time = time.time()

# Sort line segments by their x-coordinates
event_queue = SortedDict()
for segment in line_segments:
    x_coords = [point[0] for point in segment.coords]
    min_x = min(x_coords)
    max_x = max(x_coords)
    event_queue[min_x] = ("left", segment)
    event_queue[max_x] = ("right", segment)

# Dictionary to store overlapping segments
overlapping_segments = {}



# Active segments in the sweep line algorithm
active_segments = set()

# Sweep line algorithm
for x, (event_type, segment) in event_queue.items():
    if event_type == "left":
        for active_segment in active_segments:
            if segment.intersects(active_segment):
                overlap = segment.intersection(active_segment)
                if isinstance(overlap, LineString):
                    if segment not in overlapping_segments:
                        overlapping_segments[segment] = []
                    overlapping_segments[segment].append(active_segment)
        active_segments.add(segment)
    else:
        active_segments.remove(segment)




# Dictionary to store overlapping grouped by line segments
overlapping_groups = {}

# Iterate over each polygon
for i, coords1 in enumerate(polygon_coords):
    for j, coords2 in enumerate(polygon_coords):
        if i != j:
            for line_segment1 in [LineString([coords1[k], coords1[(k + 1) % len(coords1)]]) for k in range(len(coords1))]:
                for line_segment2 in [LineString([coords2[l], coords2[(l + 1) % len(coords2)]]) for l in range(len(coords2))]:
                    if line_segment1.intersects(line_segment2):
                        overlap = line_segment1.intersection(line_segment2)
                        if isinstance(overlap, LineString):
                            segment_pair = (line_segment1, line_segment2)
                            if segment_pair not in overlapping_groups:
                                overlapping_groups[segment_pair] = set()
                            overlapping_groups[segment_pair].add(i)
                            overlapping_groups[segment_pair].add(j)

# Stop measuring the execution time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"\nElapsed Time: {elapsed_time:.6f} seconds")
print()

# Print the overlapping line segments and the polygons that share them
for segment_pair, polygon_indices in overlapping_groups.items():
    line_segment1, line_segment2 = segment_pair
    start_point1, end_point1 = line_segment1.coords[0], line_segment1.coords[-1]
    start_point2, end_point2 = line_segment2.coords[0], line_segment2.coords[-1]
    
    print(f"Overlapping Line Segment: {start_point1} to {end_point1} and {start_point2} to {end_point2}")

    polygon_names_str = ', '.join([polygon_names[i] for i in polygon_indices])
    print(f"  Polygons sharing adjacent borders: {polygon_names_str}\n")

# Define names for each polygon
polygon_names = ['Polygon A', 'Polygon B', 'Polygon C', 'Polygon D', 'Polygon E', 'Polygon F', 'Polygon G', 'Polygon H']

# Define colors for each polygon
polygon_colors = ['green', 'blue', 'purple', 'cyan', 'red', 'yellow', 'orange', 'pink']


# Print the overlapping line segments and the polygons that share them
for segment_pair, polygon_indices in overlapping_segments.items():
    line_segment1, line_segment2 = segment_pair
    start_point1, end_point1 = line_segment1.coords[0], line_segment1.coords[-1]
    start_point2, end_point2 = line_segment2.coords[0], line_segment2.coords[-1]
    
    print(f"Overlapping Line Segment: {start_point1} to {end_point1} and {start_point2} to {end_point2}")

    polygon_names_str = ', '.join([polygon_names[i] for i in polygon_indices])
    print(f"  Polygons sharing adjacent borders: {polygon_names_str}\n")

# Create a larger figure and axis for visualization
fig, ax = plt.subplots(figsize=(10, 10))

# Plot each polygon with its respective color and label
for polygon, color, name in zip(polygons, polygon_colors, polygon_names):
    x, y = polygon.exterior.xy
    ax.fill(x, y, color=color, alpha=0.5)
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.annotate(f'({xi:.1f},{yi:.1f})', (xi, yi), textcoords="offset points", xytext=(0, 5), ha='center')
    centroid = polygon.centroid
    ax.text(centroid.x, centroid.y, name, fontsize=10, ha='center', va='center')

# Plot overlapping line segments with black lines
for segment_pair, polygon_indices in overlapping_groups.items():
    line_segment1, line_segment2 = segment_pair
    x_coords = [line_segment1.coords[0][0], line_segment1.coords[1][0], line_segment2.coords[0][0], line_segment2.coords[1][0]]
    y_coords = [line_segment1.coords[0][1], line_segment1.coords[1][1], line_segment2.coords[0][1], line_segment2.coords[1][1]]
    ax.plot(x_coords, y_coords, color='black', linewidth=2)

# Set axis equal, turn off axis, and display the plot
ax.set_aspect('equal')
ax.axis('off')
plt.show()