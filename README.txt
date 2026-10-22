Beam Calculator

by Oliver Brooks
10/10/2026

Overview:
    A basic script designed to display and calculate the moment and centroid for 2D sheet metal beam geometries. 
    It uses a sheet metal approximation effectively distributing area over a line based on a specified sheet thickness.


Geometry input:
    1.  A sketch object must be defined with a constant sheet thickness. For example:

        s = Sketch(0.8) # Creates Sketch called s with a thickness of 0.8 units


    2.  Vertices and edges can be added using inbuilt Sketch methods:

        s.add_vertices([[x1,y1], # Vertex 0 (at coordinates x1, y1)
                        [x2,y2], # Vertex 1
                        [x3,y3], # Vertex 2           
                        ... 
                        ])

        s.add_edges([[0,1], # Joins vertex 0 and vertex 1
                    [0,2], # Joins vertex 0 and 2
                    ...
                    ])

        
    3.  Geometry can be displayed using the function:

        run(s) # Displays geometry, along with calculated centroid and moment


Further Work:
    This program is effective at calculating the 2nd moment of area of a given sheet metal geometry, however it currently lacks mvp UI and support.
    I have created the following inbuilt Sketch methods, to be used in future for creating a beam creation UI:
    
    add_vertices(verts)

    add_edges(edges)

    move_vertex(i, x, y) # Moves vertex i to coordinates (x, y)

    delete_vertex(i) # Deletes vertex i, and neighboring edges

    delete_edge(i) # Deletes edge

    merge_vertices(a, b, x, y) # merges vertex a and vertex b, placing new vertex at (x,y)
 
    split_edge(i) # Splits edge i into two edges connected by a vertex at the original midpoint

    print_info() # Displays Sketch info

    draw(ax, selected) # Displays current sketch using MatPlotLib

    calculate(self) # Returns Centroid and 2nd moment of area
    
    
Note: I have already made a basic attempt at implementing a geometry input UI. 
The current program allows the user to select and deselect vertices with mouse clicks, and it allows the user to move the selection via the keystroke "m".
(After pressing m, the user can click a location relative to the beam's centroid, and the selected vertices will displace by that amount)
