import math

class TreeNode:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label
        self.children = {}

def entropy(data):
    num_instances = len(data)
    label_counts = {}
    for instance in data:
        label = instance[-1]
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1
    entropy = 0
    for count in label_counts.values():
        probability = count / num_instances
        entropy -= probability * math.log2(probability)
    return entropy

def info_gain(data, attribute_index):
    attribute_values = set([instance[attribute_index] for instance in data])
    info_gain_val = entropy(data)
    for value in attribute_values:
        subset_data = [instance for instance in data if instance[attribute_index] == value]
        info_gain_val -= (len(subset_data) / len(data)) * entropy(subset_data)
    return info_gain_val

def choose_best_attribute(data, attributes):
    best_attribute = None
    best_info_gain = float('-inf')
    for attribute_index in range(len(attributes) - 1):  # Exclude the label attribute
        attribute_info_gain = info_gain(data, attribute_index)
        if attribute_info_gain > best_info_gain:
            best_info_gain = attribute_info_gain
            best_attribute = attributes[attribute_index]
    return best_attribute

def split_data(data, attribute_index):
    split_data_dict = {}
    for instance in data:
        attribute_value = instance[attribute_index]
        if attribute_value not in split_data_dict:
            split_data_dict[attribute_value] = []
        split_data_dict[attribute_value].append(instance)
    return split_data_dict

def c45(data, attributes):
    labels = [instance[-1] for instance in data]
    if len(set(labels)) == 1:
        return TreeNode(label=labels[0])
    if len(attributes) == 1:
        return TreeNode(label=max(set(labels), key=labels.count))
    best_attribute = choose_best_attribute(data, attributes)
    node = TreeNode(attribute=best_attribute)
    attribute_values = set([instance[attributes.index(best_attribute)] for instance in data])
    for value in attribute_values:
        subset_data = [instance for instance in data if instance[attributes.index(best_attribute)] == value]
        if not subset_data:
            node.children[value] = TreeNode(label=max(set(labels), key=labels.count))
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_attribute]
            node.children[value] = c45(subset_data, remaining_attributes)
    return node

def tree_to_str(node, indent=0):
    if node.label is not None:
        return f"{'  ' * indent}Class: {node.label}\n"
    else:
        tree_str = f"{'  ' * indent}Attribute: {node.attribute}\n"
        for value, child in node.children.items():
            subtree = tree_to_str(child, indent + 1)
            tree_str += f"{'  ' * (indent + 1)}Value: {value}\n"
            tree_str += subtree
        return tree_str

# Example usage
data = [
    #input dataset
]

attributes = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'PlayTennis']

decision_tree = c45(data, attributes)

tree_str = tree_to_str(decision_tree)

print(tree_str)
