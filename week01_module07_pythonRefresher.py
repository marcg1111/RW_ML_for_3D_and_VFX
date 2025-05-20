import array

my_list = [1, 2, 3, 4, 5]
print(type(my_list))

my_array = array.array('i', [1, 2, 3, 4, 5]);
print(my_array[0]);

#containers

#n- dimensional arrays --> tensors (each dimentsion has same amount of elements!)
my_tensor = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]];

#graphs
# A graph is a data structure that consists of vertices (nodes) connected by edges
# Here's an example of an undirected graph using a dictionary (adjacency list)
graph = {
    'A': ['B', 'C'],    # Node A is connected to B and C
    'B': ['A', 'D'],    # Node B is connected to A and D
    'C': ['A', 'D'],    # Node C is connected to A and D
    'D': ['B', 'C']     # Node D is connected to B and C
}

# Function to add an edge to the graph
def add_edge(graph, node1, node2):
    if node1 not in graph:
        graph[node1] = []
    if node2 not in graph:
        graph[node2] = []
    graph[node1].append(node2)
    graph[node2].append(node1)  # For undirected graph

# Function to display the graph
def display_graph(graph):
    for node in graph:
        print(f"Node {node} is connected to: {graph[node]}")

# Let's add a new edge and display the graph
add_edge(graph, 'D', 'E')  # Adding a new node E connected to D
print("Graph structure:")
display_graph(graph)

#linked lists
# A linked list is a sequential data structure where each element points to the next element
# First, let's create a Node class that will represent each element in our linked list
class Node:
    def __init__(self, data):
        self.data = data    # The actual data stored in the node
        self.next = None    # Reference to the next node

class LinkedList:
    def __init__(self):
        self.head = None    # The first node in the linked list

    def append(self, data):
        new_node = Node(data)
        
        # If the list is empty, make the new node the head
        if self.head is None:
            self.head = new_node
            return

        # Otherwise, traverse to the end and add the new node
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        print("Linked List:", " -> ".join(map(str, elements)))

# Let's create and demonstrate a linked list
my_linked_list = LinkedList()
my_linked_list.append(1)    # Add some numbers
my_linked_list.append(2)
my_linked_list.append(3)
my_linked_list.append(4)

# Display the linked list
my_list.display()    # Will show: Linked List: 1 -> 2 -> 3 -> 4

#trees

#sets
c = set();
c.add(1);
c.add(2);

#hashmaps
h = {"key1": "value1", "key2": "value2"};
