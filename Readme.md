# IPv4 Fragmentation and Routing

This project implements IPv4 packet fragmentation and routing using Dijkstra's algorithm. The program is designed to simulate how IPv4 packets are fragmented when the payload size exceeds the Maximum Transmission Unit (MTU) and how the shortest path is calculated for each fragment in a network topology.

## Features

1. **Dynamic Topology Setup**:

   - Users can define a custom network topology by specifying nodes and edges.
   - Alternatively, a predefined topology can be used.

2. **IPv4 Packet Fragmentation**:

   - The program calculates the number of fragments required based on the payload size and MTU.
   - Each fragment includes the IPv4 header size (20 bytes by default).

3. **Shortest Path Calculation**:

   - Dijkstra's algorithm is used to find the shortest path between the source and destination nodes for each fragment.

4. **Error Handling**:
   - Handles cases where no path exists between the source and destination nodes.

## How It Works

### Classes

1. **Graph**:

   - Represents the network topology.
   - Stores nodes, edges, and distances between nodes.

2. **IPv4Fragmenter**:
   - Handles IPv4 fragmentation and routing.
   - Contains methods for setting up the topology, calculating shortest paths, and fragmenting packets.

### Key Methods

1. **`setup_topology()`**:

   - Allows users to define a custom network topology by specifying nodes and edges interactively.

2. **`use_predefined_topology()`**:

   - Sets up a predefined topology with fixed nodes and edges.

3. **`dijkstra(source, destination)`**:

   - Implements Dijkstra's algorithm to find the shortest path between the source and destination nodes.
   - Returns the shortest distance and the path as a list of nodes.

4. **`fragment_packet(payload_size, mtu, source, destination)`**:
   - Calculates the number of fragments required based on the payload size and MTU.
   - Finds the shortest path for each fragment and returns a list of fragment details.

### Example Workflow

1. **Topology Setup**:

   - The user chooses between a predefined topology or a custom topology.
   - Nodes and edges are defined interactively for custom topology.

2. **Input Details**:

   - The user specifies the source and destination nodes, payload size, and MTU.

3. **Fragmentation and Routing**:

   - The program calculates the number of fragments and their sizes.
   - Dijkstra's algorithm is used to find the shortest path for each fragment.

4. **Output**:
   - Displays the total number of fragments, their sizes, paths, and distances.

### Sample Output

```
Use predefined topology (p) or create custom (c)? p
Enter source node: A
Enter destination node: F
Enter payload size (in bytes): 3000
Enter MTU (in bytes): 1500

----- IPv4 Fragmentation Results -----
Total number of fragments: 2

Fragment 1:
  Size: 1500 bytes
  Path: A -> B -> D -> F
  Total distance: 17

Fragment 2:
  Size: 1520 bytes
  Path: A -> B -> D -> F
  Total distance: 17
```

## Requirements

- Python 3.x
- Standard Python libraries (`heapq`, `math`)

## How to Run

1. Clone or download the repository.
2. Run the `IPv4.py` script:
   ```
   python IPv4.py
   ```
3. Follow the prompts to set up the topology, input payload size, MTU, and source/destination nodes.

## Notes

- The IPv4 header size is fixed at 20 bytes.
- The program assumes bidirectional edges in the topology.
- If no path exists between the source and destination, the program will notify the user.
