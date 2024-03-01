class TreeNode:
    def __init__(self, attribute=None, threshold=None, label=None):
        self.attribute = attribute
        self.threshold = threshold
        self.label = label
        self.left_child = None
        self.right_child = None


def gini_index(data):
    num_instances = len(data)
    if num_instances == 0:
        return 0
    label_counts = {}
    for instance in data:
        label = instance[-1]
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1
    gini = 1
    for count in label_counts.values():
        probability = count / num_instances
        gini -= probability ** 2
    return gini


def split_data(data, attribute_index, threshold):
    left_child, right_child = [], []
    for instance in data:
        if instance[attribute_index] <= threshold:
            left_child.append(instance)
        else:
            right_child.append(instance)
    return left_child, right_child


def find_best_split(data):
    best_attribute_index = None
    best_threshold = None
    best_gini = float('inf')
    num_attributes = len(data[0]) - 1
    for attribute_index in range(num_attributes):
        attribute_values = sorted(set(instance[attribute_index] for instance in data))
        for i in range(len(attribute_values) - 1):
            threshold = (attribute_values[i] + attribute_values[i + 1]) / 2
            left_child, right_child = split_data(data, attribute_index, threshold)
            gini = (len(left_child) / len(data)) * gini_index(left_child) + \
                   (len(right_child) / len(data)) * gini_index(right_child)
            if gini < best_gini:
                best_gini = gini
                best_attribute_index = attribute_index
                best_threshold = threshold
    return best_attribute_index, best_threshold


def cart(data, depth=0, max_depth=2):
    labels = [instance[-1] for instance in data]
    if depth == max_depth or len(set(labels)) == 1:
        return TreeNode(label=max(set(labels), key=labels.count))
    attribute_index, threshold = find_best_split(data)
    if attribute_index is None:
        return TreeNode(label=max(set(labels), key=labels.count))

    # Build the root node with exactly two branches
    node = TreeNode(attribute=attribute_index, threshold=threshold)
    left_child, right_child = split_data(data, attribute_index, threshold)
    node.left_child = cart(left_child, depth + 1, max_depth)
    node.right_child = cart(right_child, depth + 1, max_depth)

    return node


def tree_to_str(node, indent=0):
    if node.label is not None:
        return f"{'  ' * indent}Class: {node.label}\n"
    else:
        tree_str = ""
        tree_str += f"{'  ' * indent}Attribute: {node.attribute}, Threshold: {node.threshold}\n"
        tree_str += tree_to_str(node.left_child, indent + 1)
        tree_str += tree_to_str(node.right_child, indent + 1)
        return tree_str


# Sample dataset
data = [
    # input dataset
]

# Build decision tree
decision_tree = cart(data)

# Print tree structure
tree_str = tree_to_str(decision_tree)
print(tree_str)
