class Node:
    def __init__(self, name):
        self.name = name
        self.interfaces = {}

    def add_interface(self, interface, neighbor):
        self.interfaces[interface] = neighbor


def dfs(node, visited, path, all_paths):
    visited[node.name] = True
    path.append(node.name)

    for interface, neighbor in node.interfaces.items():
        if not visited[neighbor]:
            dfs(neighbor, visited, path, all_paths)

    if len(node.interfaces) == 0:  # Node is a leaf
        all_paths.append(list(path))

    path.pop()
    visited[node.name] = False


def generate_paths(nodes):
    all_paths = []
    visited = {node: False for node in nodes}

    for node in nodes:
        if not visited[node]:
            dfs(node, visited, [], all_paths)

    return all_paths


def write_paths_to_file(paths, filename):
    with open(filename, 'w') as file:
        for path in paths:
            file.write(' -> '.join(path) + '\n')


if __name__ == '__main__':
    # Create nodes
    n1 = Node('n1')
    n2 = Node('n2')
    n3 = Node('n3')
    n4 = Node('n4')
    n5 = Node('n5')
    n6 = Node('n6')
    n7 = Node('n7')
    n8 = Node('n8')
    n9 = Node('n9')
    n10 = Node('n10')
    n11 = Node('n11')
    n12 = Node('n12')
    n13 = Node('n13')
    n14 = Node('n14')
    n15 = Node('n15')
    n16 = Node('n16')
    n17 = Node('n17')

    # Add interfaces
    n1.add_interface('eth0', n12)
    n1.add_interface('eth1', n13)
    n1.add_interface('eth2', n3)
    n1.add_interface('eth3', n4)

    n2.add_interface('eth0', n11)
    n2.add_interface('eth1', n1)
    n2.add_interface('eth2', n5)

    n3.add_interface('eth0', n1)
    n3.add_interface('eth1', n7)
    n3.add_interface('eth2', n4)

    n4.add_interface('eth0', n3)
    n4.add_interface('eth1', n6)
    n4.add_interface('eth2', n1)

    n5.add_interface('eth0', n15)
    n5.add_interface('eth2', n2)
    n5.add_interface('eth3', n9)
    n5.add_interface('eth4', n6)

    n6.add_interface('eth0', n8)
    n6.add_interface('eth1', n7)
    n6.add_interface('eth2', n5)
    n6.add_interface('eth3', n9)
    n6.add_interface('eth4', n4)

    n7.add_interface('eth0', n14)
    n7.add_interface('eth1', n3)
    n7.add_interface('eth2', n8)
    n7.add_interface('eth3', n6)

    n8.add_interface('eth0', n7)
    n8.add_interface('eth1', n10)
    n8.add_interface('eth2', n6)

    n9.add_interface('eth0', n5)
    n9.add_interface('eth1', n6)
    n9.add_interface('eth2', n10)

    n10.add_interface('eth0', n16)
    n10.add_interface('eth1', n8)
    n10.add_interface('eth2', n9)
    n10.add_interface('eth3', n17)

    n11.add_interface('eth0', n2)

    n12.add_interface('eth0', n1)

    n13.add_interface('eth0', n1)

    n14.add_interface('eth0', n7)

    n15.add_interface('eth0', n5)

    n16.add_interface('eth0', n10)

    n17.add_interface('eth0', n10)

    # Generate paths
    nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17]
    paths = generate_paths(nodes)

    # Write paths to a file
    write_paths_to_file(paths, 'netconfig.txt')
