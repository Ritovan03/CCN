import heapq
import math

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}
    
    def add_node(self, value):
        self.nodes.add(value)
        if value not in self.edges:
            self.edges[value] = []
    
    def add_edge(self, from_node, to_node, distance):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance

class IPv4Fragmenter:
    """
    Class to handle IPv4 fragmentation and routing via Dijkstra's algorithm.
    The implementation supports dynamic topology changes and recalculates the shortest path
    for each fragment.
    """
    
    def __init__(self):
        self.graph = None
        self.header_size = 20  # IPv4 header size in bytes
    
    def setup_topology(self):
        """Set up the network topology based on user input."""
        self.graph = Graph()
        
        num_nodes = int(input("Enter number of nodes in the topology: "))
        
        print("Enter nodes (e.g., A, B, C, ...): ")
        for i in range(num_nodes):
            node = input(f"Node {i+1}: ")
            self.graph.add_node(node)
        
        num_edges = int(input("Enter number of edges: "))
        
        print("Enter edges as 'source destination weight' (e.g., A B 5): ")
        for i in range(num_edges):
            edge = input(f"Edge {i+1}: ").split()
            source, destination, weight = edge[0], edge[1], int(edge[2])
            self.graph.add_edge(source, destination, weight)
    
    def use_predefined_topology(self):
        """Use the predefined topology from the assignment."""
        self.graph = Graph()
        
        # Add nodes
        for node in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.graph.add_node(node)
        
        # Add edges with their weights
        edges = [
            ('A', 'B', 7),
            ('A', 'C', 12),
            ('B', 'C', 2),
            ('B', 'D', 9),
            ('C', 'E', 10),
            ('D', 'F', 1),
            ('E', 'D', 4),
            ('E', 'F', 5)
        ]
        
        for source, destination, weight in edges:
            self.graph.add_edge(source, destination, weight)
    
    def dijkstra(self, source, destination):
        """
        Implements Dijkstra's algorithm to find the shortest path.
        
        Args:
            source: Starting node
            destination: Target node
        
        Returns:
            Tuple of (shortest distance, path as a list of nodes)
        """
        if source not in self.graph.nodes or destination not in self.graph.nodes:
            return float('infinity'), []
        
        # Initialize distances with infinity for all nodes except the source
        distances = {node: float('infinity') for node in self.graph.nodes}
        distances[source] = 0
        
        # Dictionary to store the previous node in the optimal path
        previous = {node: None for node in self.graph.nodes}
        
        # Priority queue to store (distance, node) pairs
        priority_queue = [(0, source)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # If we reached the destination, we can terminate
            if current_node == destination:
                break
            
            # If we've already found a better path to the current node, skip
            if current_distance > distances[current_node]:
                continue
            
            # Check all neighboring nodes
            for neighbor in self.graph.edges[current_node]:
                distance = current_distance + self.graph.distances[(current_node, neighbor)]
                
                # If we found a better path to the neighbor, update
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Reconstruct the path
        path = []
        current = destination
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        # Reverse the path to go from source to destination
        path.reverse()
        
        # If the destination is not reachable, return empty path
        if distances[destination] == float('infinity'):
            return float('infinity'), []
        
        return distances[destination], path
    
    def fragment_packet(self, payload_size, mtu, source, destination):
        """
        Fragment an IPv4 packet based on MTU and calculate the shortest path for each fragment.
        
        Args:
            payload_size: Size of the payload in bytes
            mtu: Maximum Transmission Unit in bytes
            source: Source node
            destination: Destination node
        
        Returns:
            List of tuples (fragment_number, fragment_size, path, distance)
        """
        # Calculate the maximum payload size per fragment
        max_payload_per_fragment = mtu - self.header_size
        
        # Calculate the number of fragments needed
        num_fragments = math.ceil(payload_size / max_payload_per_fragment)
        
        fragments = []
        remaining_payload = payload_size
        
        for i in range(num_fragments):
            # Calculate current fragment size
            fragment_payload_size = min(max_payload_per_fragment, remaining_payload)
            fragment_total_size = fragment_payload_size + self.header_size
            
            # Find the shortest path for this fragment
            distance, path = self.dijkstra(source, destination)
            
            if path:  # If a path exists
                fragments.append({
                    'fragment_number': i + 1,
                    'fragment_size': fragment_total_size,
                    'path': path,
                    'distance': distance
                })
                
                remaining_payload -= fragment_payload_size
            else:
                print(f"No path found from {source} to {destination}. Cannot send fragment {i+1}.")
        
        return fragments

def main():
    """Main function to run the IPv4 fragmenter."""
    fragmenter = IPv4Fragmenter()
    
    # Ask if user wants to use predefined topology or custom topology
    topology_choice = input("Use predefined topology (p) or create custom (c)? ").lower()
    
    if topology_choice == 'p':
        fragmenter.use_predefined_topology()
    else:
        fragmenter.setup_topology()
    
    # Get source and destination nodes
    source = input("Enter source node: ")
    destination = input("Enter destination node: ")
    
    # Get payload and MTU details
    payload_size = int(input("Enter payload size (in bytes): "))
    mtu = int(input("Enter MTU (in bytes): "))
    
    # Fragment the packet
    fragments = fragmenter.fragment_packet(payload_size, mtu, source, destination)
    
    # Display fragmentation results
    print("\n----- IPv4 Fragmentation Results -----")
    if fragments:
        print(f"Total number of fragments: {len(fragments)}")
        for frag in fragments:
            print(f"\nFragment {frag['fragment_number']}:")
            print(f"  Size: {frag['fragment_size']} bytes")
            print(f"  Path: {' -> '.join(frag['path'])}")
            print(f"  Total distance: {frag['distance']}")
    else:
        print("No fragments were created.")

if __name__ == "__main__":
    main()