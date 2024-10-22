# Multidimensional Data Structures and Computational Geometry

## Project Overview

This project involves the development and performance analysis of geometric multidimensional structures, focusing on key data structures used in computational geometry and spatial queries. It implements various algorithms to solve problems such as trajectory queries, interval and stabbing queries, convex hull computation, and line segment intersection detection. The work is grounded in both theoretical principles and practical applications, such as Geographic Information Systems (GIS).

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)


## Features

1. **3D R-trees for Spatio-Temporal Queries**:
   - Indexes moving objects' trajectories in the plane using 3D R-trees for points of the form (x, y, t).
   - Supports spatio-temporal trajectory queries for efficient analysis.

2. **Interval and Segment Trees**:
   - Implements interval trees for interval queries.
   - Implements segment trees for stabbing queries.
   - Performance analysis of basic operations (insert, delete, query) on both structures.

3. **Convex Hull Algorithm**:
   - Computes convex hulls in two dimensions, identifying the outermost boundary enclosing a set of points.

4. **Line Segment Intersection**:
   - Implements algorithms for detecting intersections between rectilinear segments in 2D.
   - Commonly used in applications such as map overlay for Geographic Information Systems (GIS).

## Prerequisites

- Basic understanding of:
  - Data Structures
  - Algorithms and Complexity
  - Databases
  - Object-Oriented Programming
  - Functional Programming

## Installation

### 1. Clone the Repository

To download the code, you can use Git. Open a terminal and execute the following command to clone the repository to your local machine:

```bash
git clone https://github.com/ssoulis/Multidimensional-Data-Structures-and-Computational-Geometry.git
```
After cloning, navigate into the project directory:
``` bash
cd Multidimensional-Data-Structures-and-Computational-Geometry
```
### 2. Install Dependencies

Once you have cloned the repository, you will need to install the required Python libraries. You can do this by running the following commands:
```bash
pip install Rtree
pip install intervaltree
pip install matplotlib
pip install numpy
```
Make sure you have Python installed on your system. If you don’t have Python installed, download it from the official website: https://www.python.org/downloads/.

## Usage

Once the repository has been cloned and the necessary libraries are installed, you can run the scripts.

For example, to run the convex hull implementation, use the following command:
``` bash
python convex_hull.py
```
You can similarly run other files by replacing convex_hull.py with the desired script filename.

## Results
The performance of the different structures is analyzed, providing insights into their computational efficiency and usability for various geometric queries. Graphs and tables are generated using matplotlib to visualize performance metrics.












