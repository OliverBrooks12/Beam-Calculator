import numpy as np
import matplotlib.pyplot as plt

# All dimensions in mm


class Sketch:
    def __init__(self, thickness):
        self.vertices = np.empty((0,2), dtype = float)
        self.edges = np.empty((0,2), dtype = int)
        self.thickness = thickness
        self.centroid = None
        self.area = 0
        self.I_x = 0
        self.I_y = 0
    
    def add_vertices(self, verts): # verts is a list of 2-long coords
        self.vertices = np.vstack([self.vertices, [verts[i] for i in range(len(verts))]])
        return len(self.vertices) - 1

    def add_edges(self, edges):
        self.edges = np.vstack([self.edges, [edges[i] for i in range(len(edges))]])

    def move_vertex(self, i, x, y):
        self.vertices[i] = [x, y]

    def delete_vertex(self, i):

        connected = np.any(self.edges == i, axis=1) # Finds edges containing vertex
        self.edges = self.edges[~connected] # Deletes edges
        self.edges[self.edges > i] -= 1 # Reduces the indices greater than the deleted vertex
        self.vertices = np.delete(self.vertices, i, axis = 0) # Delete Vertex

    def delete_edge(self, i):
        self.edges = np.vstack([self.edges[:i],self.edges[i+1:]])

    def merge_vertices(self, a, b, x, y):
        a, b = sorted([a,b])
        merge_edge = np.where(np.all(np.sort(self.edges, axis=1) == [a, b], axis=1))[0] # Finds edge joining a and b
        if merge_edge.size > 0:
            self.delete_edge(merge_edge[0])

        verts = np.unique(self.edges[np.any(self.edges == a, axis=1)])
        
        verts = verts[verts != a]
        
        self.delete_vertex(a)
        verts = [x-1 if x > a else x for x in verts]
    
        b -= 1 # Don't mind the BandAid,

        for vert in verts:
            self.add_edges(vert, b)

        self.move_vertex(b, x, y)
 
    def split_edge(self, i):
        v1, v2 = self.edges[i]
        ybar = (self.vertices[v2,1] + self.vertices[v1,1]) / 2
        xbar = (self.vertices[v2,0] + self.vertices[v1,0]) / 2
        print(xbar, ybar)
        
        self.delete_edge(i)
        self.add_vertices([xbar,ybar])
        v_new = len(self.vertices)-1
        self.add_edges([[v1,v_new],[v2,v_new]])
    
    def print_info(self):
        print('Sketch information:')
        print(f'Thickness: {self.thickness}')

        print('\nVertices:')
        for i, vert in enumerate(self.vertices):
            print(f"{i} - ({vert[0]}, {vert[1]})")

        print('\nEdges:')
        for i, edge in enumerate(self.edges):
            print(f"{i} - ({edge[0]}, {edge[1]})")

        print(' ')

    def draw(self, ax, selected):

        for a, b in self.edges:
            p1 = self.vertices[a]
            p2 = self.vertices[b]

            ax.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                'b-',
                linewidth=1
            )


        ax.scatter(


            self.vertices[selected == 1,0],
            self.vertices[selected == 1,1],
            color = 'b',
            linewidths=0.5
        )

        #for i, (x, y) in enumerate(self.vertices):
            #ax.annotate(f'({x}, {y})', (x+0.01,y+0.01), fontsize=0)

        if self.centroid:
            ax.axvline(self.centroid[0], color='y', linestyle='--', linewidth=1)
            ax.axhline(self.centroid[1], color='y', linestyle='--', linewidth=1)
            ax.plot(self.centroid[0], self.centroid[1], 'ro', markersize=5, markeredgewidth=2)
            ax.plot(self.centroid[0], self.centroid[1], 'k+', markersize=6, markeredgewidth=1.5)
            ax.annotate(f'({self.centroid[0]:.2f}, {self.centroid[1]:.2f})', (self.centroid[0]+0.1,self.centroid[1]+0.1))
            
        ax.set_aspect('equal')
        ax.grid(True)
        

    def calculate(self):
        self.area = 0
        ybar_A = 0
        xbar_A = 0
        self.I_x = 0
        self.I_y = 0
        for edge in self.edges:
            # Calculates parameters based on edge. Approximation assumes sufficiently thin material is effectively a line.
            dx = self.vertices[edge[1], 0] - self.vertices[edge[0], 0]
            dy = self.vertices[edge[1], 1] - self.vertices[edge[0], 1]
            dist = (dx**2 + dy**2)**0.5
            a = dist * self.thickness
            ybar = (self.vertices[edge[1], 1] + self.vertices[edge[0], 1]) / 2
            xbar = (self.vertices[edge[1], 0] + self.vertices[edge[0], 0]) / 2

            self.area += a
            ybar_A += ybar * a
            xbar_A += xbar * a

        self.centroid = [xbar_A / self.area, ybar_A / self.area]

        for edge in self.edges:
            # Calculates parameters based on edge. Approximation assumes sufficiently thin material is effectively a line.
            dx = self.vertices[edge[1], 0] - self.vertices[edge[0], 0]
            dy = self.vertices[edge[1], 1] - self.vertices[edge[0], 1]
            dist = (dx**2 + dy**2)**0.5
            a = dist * self.thickness
            # ybar and xbar below are relative to centroid
            ybar = (self.vertices[edge[1], 1] + self.vertices[edge[0], 1]) / 2 - self.centroid[1]
            xbar = (self.vertices[edge[1], 0] + self.vertices[edge[0], 0]) / 2 - self.centroid[0]

            self.I_x += a * (dy**2 / 12 + ybar**2)
            self.I_y += a * (dx**2 / 12 + xbar**2)

        return self.area, self.centroid, [self.I_x, self.I_y]


def get_properties(s): # Calculate area, centroid, and 2nd moment
    print("Calculating ...\n")

    area, [x_centroid, y_centroid], [I_x, I_y] = s.calculate()

    print(f'Area: {area} mm^2')
    print(f'Centroid is at ({x_centroid}, {y_centroid})')
    print(f'I_x = {I_x:.4f} mm^4')
    print(f'I_y = {I_y:.4f} mm^4\n')


def run(s):
    fig, (ax, info) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

    click_range = 1.5

    global selected
    selected = np.zeros(len(s.vertices))
    global moving
    moving = False


    def update():
        s.calculate()
        
        ax.clear()
        s.draw(ax, selected)

        info.clear()
        info.axis('off')
        info.text(0, 1, f"Sheet Thickness = {s.thickness:.4f} mm\n"
                        f"Area: {s.area:.4f} mm^2\n"
                        f"Centroid Location: ({s.centroid[0]:.4f}, {s.centroid[1]:.4f})\n"
                        f"I_x: {s.I_x:.4f} mm^4\n"
                        f"I_y: {s.I_y:.4f} mm^4",
                va='top', fontsize=12)

        ax.set_aspect('equal')
        fig.canvas.draw_idle()

    def on_click(event):
        x_m, y_m = event.xdata, event.ydata

        global moving
        if moving:
            s.vertices[[True if selected[x] else False for x in range(len(s.vertices))]] += [x_m-s.centroid[0],y_m-s.centroid[1]] # Adds mouse position to selected vertices
            moving = False

        for i, [x, y] in enumerate(s.vertices):
            dist = ((x_m - x)**2 + (y_m - y)**2)**0.5
            if dist < click_range:
                if selected[i]:
                    selected[i] = 0
                else:
                    selected[i] = 1
        update()

        


    def on_key(event):
        key = event.key
        if key == 'm':
            global moving
            moving = True


    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)

    
    #get_properties(s)
    update()
    plt.show()


s = Sketch(0.8) # 0.77 mm thickness

s.add_vertices([
    [0, 73.54], [17.23, 73.54], [0, 0.77], [10, 0.77],
    [45, 73.54], [55, 73.54], [10, 1.54], [0, 1.54],
    [55, 72.77], [45, 72.77], [90, 0.77], [100, 0.77],
    [100, 73.54], [82, 73.54], [100, 1.54], [90, 1.54],
    [0, 0], [100, 0],
    [0, 74.31], [100, 74.31]
])

s.add_edges([
    [0, 1], [0, 2], [2, 3],
    [4, 5], [4, 6], [6, 7],
    [8, 9], [8, 10], [10, 11],
    [12, 13], [12, 14], [14, 15],
    [16, 17],
    [18, 19]
])


run(s)