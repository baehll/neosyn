from heapq import merge
from itertools import islice

def create_comment(igcomment):
    parent = {
        "text": igcomment["text"],
        "from": igcomment["from"],
        "timestamp": igcomment["timestamp"],
        "text": igcomment["text"],
        "like_count": igcomment["like_count"],
        "id": igcomment["id"],
        "media": igcomment["media"]["id"],
        "replies": []
    }
    if "replies" in igcomment:
        parent["replies"] = [create_comment(r) for r in igcomment["replies"]["data"]]
    return parent

def max_timestamp(node):
    if not node['replies']:
        return node['timestamp']
    return max(node['timestamp'], max(child['timestamp'] for child in node['replies']))

def traverse_pre_order_gen(node):
    if not isinstance(node, dict):
        raise TypeError(f"Expected node to be a dict, got {type(node).__name__} instead")
    yield node
    for child in node['replies']:
        yield from traverse_pre_order_gen(child)

def traverse_post_order_gen(node):
    if not isinstance(node, dict):
        raise TypeError(f"Expected node to be a dict, got {type(node).__name__} instead")
    for child in node['replies']:
        yield from traverse_post_order_gen(child)
    yield node
    
def merge_sorted_trees_gen(trees, traversal_fn):
    # Create a list of tuples (max_timestamp, tree) for sorting
    sorted_trees = sorted(
        ((max_timestamp(tree), tree) for _, forest in trees for tree in forest),
        key=lambda x: x[0],
        reverse=True
    )
    # Extract only the trees in sorted order
    sorted_trees = [tree for _, tree in sorted_trees]
    return iter(sorted_trees)

def get_sorted_slice(data, traversal_fn, start, end):
    # Flatten the top-level structure to work with individual trees within each list
    all_trees = [tree for _, forest in data for tree in forest]
    merged_sorted_gen = merge_sorted_trees_gen(data, traversal_fn)
    sliced_trees = list(islice(merged_sorted_gen, start, end))
    return sliced_trees

def add_tree(id_to_node, trees, tree_tuple):
    trees.append(tree_tuple)
    for node in tree_tuple[1]:
        assign_ids_and_store(id_to_node, node)
    
def remove_tree(id_to_node, trees, tree_id):
    trees[:] = [(tid, tree) for tid, tree in trees if tid != tree_id]
    # Remove nodes associated with the tree_id from id_to_node
    ids_to_remove = [id for id, node in id_to_node.items() if node["id"] == tree_id]
    for id in ids_to_remove:
        del id_to_node[id]
        
def assign_ids_and_store(id_to_node, node):
    id = node["id"]
    id_to_node[id] = node
    for r in node["replies"]:
        assign_ids_and_store(id_to_node, r)
        
def convert_lists_to_tuples(data):
    return [tuple([item[0], item[1]]) for item in data]