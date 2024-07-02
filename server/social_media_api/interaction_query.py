from heapq import merge
from itertools import islice
from dateutil import parser as date_parser

def create_comment(igcomment):
    parent = {
        "text": igcomment.get("text"),
        "from": igcomment.get("from"),
        "timestamp": igcomment["timestamp"],
        "like_count": igcomment["like_count"],
        "id": igcomment["id"],
        "media": igcomment["media"]["id"],
        "replies": []
    }
    if "replies" in igcomment:
        parent["replies"] = [create_comment(r) for r in reversed(igcomment["replies"]["data"])]
    return parent
    
def merge_sorted_trees_gen(merged_trees, sort_order='new'):
    def get_sort_key(node):
        #timestamps = [date_parser.isoparse(n['timestamp']) for n in traversal_fn(node)]
        if sort_order == 'new' or sort_order == "old":
            if node['replies']:
                return date_parser.isoparse(node['replies'][-1]['timestamp'])
            return date_parser.isoparse(node['timestamp'])
        elif sort_order == "most_interaction" or sort_order == "least_interaction":
            return 1 + len(node["replies"])
        else:
            raise ValueError("sort_order must be 'new' or 'old'")
    
    sorted_trees = sorted(
        merged_trees,
        key=lambda comment_chain: get_sort_key(comment_chain),
        reverse=(sort_order == 'new' or sort_order == "most_interaction")
    )
    return iter(sorted_trees)

def get_sorted_list(data, sort_order="new"):
    merged_trees = []
    for t in data:
        merged_trees.extend(t[1])
    merge_sorted_gen = merge_sorted_trees_gen(merged_trees, sort_order)
    return merge_sorted_gen

def get_sorted_slice(merged_sorted_gen, start, end):
    sliced_nodes = list(islice(merged_sorted_gen, start, end))
    return sliced_nodes

# def get_sorted_slice(data, start, end, sort_order='new'):
#     merged_trees = []
#     for t in data:
#         merged_trees.extend(t[1])
#     merged_sorted_gen = merge_sorted_trees_gen(merged_trees, sort_order)
#     sliced_nodes = list(islice(merged_sorted_gen, start, end))
#     return sliced_nodes

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