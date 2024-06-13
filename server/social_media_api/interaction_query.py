from heapq import merge
from itertools import islice

def create_comment(igcomment):
    if "replies" in igcomment:
        replies = [create_comment(r) for r in igcomment["replies"]["data"]]
    else:
        replies = []
    return {
        "text": igcomment["text"],
        "from": igcomment["from"],
        "timestamp": igcomment["timestamp"],
        "text": igcomment["text"],
        "like_count": igcomment["like_count"],
        "id": igcomment["id"],
        "replies": replies
    }

def max_timestamp(node):
    if not node['replies']:
        return node['timestamp']
    return max(node['timestamp'], max(child['timestamp'] for child in node['replies']))

def traverse_pre_order_gen(node):
    yield node
    for child in node['replies']:
        yield from traverse_pre_order_gen(child)

def traverse_post_order_gen(node):
    for child in node['children']:
        yield from traverse_post_order_gen(child)
    yield node

def merge_sorted_trees_gen(trees, traversal_fn):
    sorted_generators = (sorted(traversal_fn(tree), key=max_timestamp, reverse=True) for tree in trees)
    return merge(*sorted_generators, key=max_timestamp, reverse=True)

def get_sorted_slice(trees, traversal_fn, start, end):
    merged_sorted_gen = merge_sorted_trees_gen(trees, traversal_fn)
    sliced_nodes = list(islice(merged_sorted_gen, start, end))
    return sliced_nodes