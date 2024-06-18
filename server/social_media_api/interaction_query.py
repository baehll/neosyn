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
    sorted_generators = (
        sorted(traversal_fn(tree), key=max_timestamp, reverse=True)
        for tree in trees
    )
    merged = merge(*sorted_generators, key=max_timestamp, reverse=True)
    return merged

def get_sorted_slice(data, traversal_fn, start, end):
    # Flatten the top-level structure to work with individual trees within each list
    all_trees = [tree for sublist in data for tree in sublist]
    merged_sorted_gen = merge_sorted_trees_gen(all_trees, traversal_fn)
    sliced_nodes = list(islice(merged_sorted_gen, start, end))
    return sliced_nodes