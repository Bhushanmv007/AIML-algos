import math

class Node:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label
        self.children = {}

def calculate_entropy(data):
    num_instances = len(data)
    label_counts = {}
    for instance in data:
        label = instance[-1]
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1
    entropy = 0
    for label in label_counts:
        probability = label_counts[label] / num_instances
        entropy -= probability * math.log2(probability)
    return entropy

def split_data(data, attribute_index):
    split_data_dict = {}
    for instance in data:
        attribute_value = instance[attribute_index]
        if attribute_value not in split_data_dict:
            split_data_dict[attribute_value] = []
        split_data_dict[attribute_value].append(instance)
    return split_data_dict

def choose_best_attribute(data, attributes):
    best_attribute = None
    best_entropy = float('inf')
    for attribute_index in range(len(attributes) - 1):  # Exclude the label attribute
        attribute_values = set([instance[attribute_index] for instance in data])
        entropy = 0
        for value in attribute_values:
            subset_data = [instance for instance in data if instance[attribute_index] == value]
            entropy += (len(subset_data) / len(data)) * calculate_entropy(subset_data)
        if entropy < best_entropy:
            best_entropy = entropy
            best_attribute = attributes[attribute_index]
    return best_attribute

def id3(data, attributes):
    labels = [instance[-1] for instance in data]
    if len(set(labels)) == 1:
        return Node(label=labels[0])
    if len(attributes) == 1:
        return Node(label=max(set(labels), key=labels.count))
    best_attribute = choose_best_attribute(data, attributes)
    node = Node(attribute=best_attribute)
    attribute_values = set([instance[attributes.index(best_attribute)] for instance in data])
    for value in attribute_values:
        subset_data = [instance for instance in data if instance[attributes.index(best_attribute)] == value]
        if not subset_data:
            node.children[value] = Node(label=max(set(labels), key=labels.count))
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_attribute]
            node.children[value] = id3(subset_data, remaining_attributes)
    return node

# Example usage
data = [
    # input dataset
]

attributes = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'PlayTennis']

decision_tree = id3(data, attributes)

def tree_to_dict(node, indent=0):
    if node.label is not None:
        return f"{'  ' * indent}Predict: {node.label}"
    else:
        tree_dict = f"{'  ' * indent}{node.attribute}:\n"
        for value, child in node.children.items():
            subtree = tree_to_dict(child, indent + 1)
            tree_dict += f"{'  ' * (indent + 1)}{value} -> {subtree}\n"
        return tree_dict

print(tree_to_dict(decision_tree))

