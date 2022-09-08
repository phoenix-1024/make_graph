import numpy as np
from scipy import interpolate 

class Node:
    def __init__(self, name):
        self.name = name
        self.connection = set()


class Graph:
    def __init__(self, graph_dict: dict):
        self.all_nodes_dict = {}
        self.add_to_graph(graph_dict)


    def add_to_graph(self, graph_dict: dict):
        for key, value in graph_dict.items():
            if key not in self.all_nodes_dict:
                self.all_nodes_dict[key] = Node(key)
            if type(value) == list:
                for item in value:
                    if item not in self.all_nodes_dict:
                        self.all_nodes_dict[item] = Node(item)
                    self.connect(self.all_nodes_dict[key], self.all_nodes_dict[item])

            elif type(value) == dict:
                self.add_to_graph(value)
            elif type(value) == str:
                if value not in self.all_nodes_dict:
                    self.all_nodes_dict[value] = Node(value)
                self.connect(self.all_nodes_dict[key], self.all_nodes_dict[item])
            else:
                raise ValueError("value must be list or str")

    def connect(self, node1, node2):
        node1.connection.add(node2)
        node2.connection.add(node1)
        
    def print_graph(self):
        for key, value in self.all_nodes_dict.items():
            print(key)
            print("connection:")
            for item in value.connection:
                print(item.name)
            print("#"*10)

    def get_node(self, name):
        return self.all_nodes_dict[name]

    def draw_circular_graph(self,plt):
        angels = np.linspace(0, 2 * np.pi, len(self.all_nodes_dict), endpoint=False)
        x = np.cos(angels)*10
        y = np.sin(angels)*10
        # x_inner = np.cos(angels)*9
        # y_inner = np.sin(angels)*9
        for i, (key, value) in enumerate(self.all_nodes_dict.items()):
            plt.scatter(x[i], y[i], c="yellow", s=100)
            plt.text(x[i], y[i], key, fontsize=15,color="red")
            
            for item in value.connection:
                line = self.make_inner_line([x[i], x[list(self.all_nodes_dict.keys()).index(item.name)]],
                         [y[i], y[list(self.all_nodes_dict.keys()).index(item.name)]])
                plt.plot(line[0], line[1], c="black")

        plt.show()

    def make_inner_line(self, pair_x, pair_y):
        ''' 
        The function make_spine takes a set of control points and returns a set of points that define a B-spline curve.
        
        '''
        # Convert the control points to a numpy array
        
        x=np.array([pair_x[0],pair_x[0]*0.5,0,pair_x[1]*0.5,pair_x[1]]) # adding 0 to curve the line
        y=np.array([pair_y[0],pair_y[0]*0.5,0,pair_y[1]*0.5,pair_y[1]]) # adding *0.5 to give extra space between nodes

        # uncomment both lines for a closed curve
        #x=np.append(x,[x[0]])  
        #y=np.append(y,[y[0]])

        l=len(x)  

        t=np.linspace(0,1,l-2,endpoint=True)
        t=np.append([0,0,0],t)
        t=np.append(t,[1,1,1])

        tck=[t,[x,y],3]
        u3=np.linspace(0,1,(max(l*2,70)),endpoint=True)
        out = interpolate.splev(u3,tck)
        return out


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    a = {
        "a": ["b", "c","p","q","r"],
        "b": ["d", "a"],
        "c": ["a", "d"],
        "d": ["j", "k"]
    }
    graph = Graph(a)
    # graph.print_graph()
    # f = graph.get_node("f")
    # print(f.name)
    # print(f"connections of f: {[item.name for item in f.connection]}")
    print("Graph made successfully")
    graph.draw_circular_graph(plt)
    print("called draw_circular_graph")
    # plt.show()