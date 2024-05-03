# Sort by str id
# Examples:
#   add_node('A', ['B', 'C'])
#   add_node('G<A,B>', ['A', 'B'])
class TopologicalSort:
    # Parent node -> Child nodes
    nodes: dict[str, list[str]]

    # Child node -> Parent nodes
    to_nodes: dict[str, list[str]]

    # Result
    sorted_nodes: list[str]

    def __init__(self):
        self.nodes = {}
        self.to_nodes = {}
        self.sorted_nodes = []

    def add_node(self, name: str, childs: list[str]):
        self.nodes.setdefault(name, []).extend(childs)

        self.to_nodes.setdefault(name, [])
        for child in childs:
            self.to_nodes.setdefault(child, []).append(name)

    @staticmethod
    def get_generic(type_name):
        # todo: make multiple nested types
        left_bracket = type_name.find('<')
        right_bracket = type_name.rfind('>')

        generic_args = []

        if left_bracket < right_bracket:
            generic_args = list(map(str.strip, type_name[left_bracket + 1:right_bracket].split(",")))
            type_name = type_name[:left_bracket]

        return type_name, generic_args

    def make_sort(self) -> list[str]:
        self.sorted_nodes.clear()

        while len(self.sorted_nodes) < len(self.nodes):
            v = [child_node_name for child_node_name, parent_node_names in self.to_nodes.items() if
                 not parent_node_names]
            if not v:
                raise RuntimeError("Cyclic dependency")

            for parent_node_name in v:
                # New sorted node
                self.sorted_nodes.append(parent_node_name)

                # Remove links
                self.to_nodes.pop(parent_node_name)

                if parent_node_name not in self.nodes:
                    raise RuntimeError(f"Undefined parent message: {parent_node_name}")

                for child_node_name in self.nodes[parent_node_name]:
                    self.to_nodes[child_node_name].remove(parent_node_name)

        return self.sorted_nodes