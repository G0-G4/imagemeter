import dearpygui.dearpygui as dpg
import line
from collections import defaultdict


parent_to_children = defaultdict(set)
child_to_parent = dict()

flt = 0
px = 1

def add(parent, child):
    parent_to_children[parent].add(child)
    child_to_parent[child] = parent

def remove(parent, child):
    parent_to_children[parent].remove(child)
    if len(parent_to_children[parent]) == 0:
        del parent_to_children[parent]
    del child_to_parent[child]

def get_node_elt(node, i):
    children = dpg.get_item_children(node, 1) # get children from slot 1 (mvNode_Attr_Static)
    elt = dpg.get_item_children(children[2], 1)[i] # get i child of node attribute (float input)
    return elt

def delete_node(sender, app_data, user_data):
    node, l = user_data
    if node in child_to_parent:
        par = child_to_parent[node]
        del child_to_parent[node]
        parent_to_children[par].remove(node)
        if len(parent_to_children[par]) == 0:
            del parent_to_children[par]
    elif node in parent_to_children:
        children = parent_to_children[node]
        del parent_to_children[node]
        for ch in children:
            del child_to_parent[ch]
    dpg.delete_item(node)
    dpg.delete_item(l)
    del line.tags[-1]

def recalculate(parent_node, child_node):
    left_flt = get_node_elt(parent_node, flt)
    left_px, right_px = get_node_elt(parent_node, px), get_node_elt(child_node, px)
    left_px = float(dpg.get_value(left_px))
    right_px = float(dpg.get_value(right_px))
    len_cm = -1
    if left_px != 0:
        len_cm = dpg.get_value(left_flt)/left_px * right_px
    return len_cm 

def link_callback(sender, app_data):
    parent_node, child_node = dpg.get_item_parent(app_data[0]), dpg.get_item_parent(app_data[1]) # # search for node from input or output
    if child_node in child_to_parent or parent_node in child_to_parent or child_node in parent_to_children:
        return
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    right_flt = get_node_elt(child_node, flt)
    len_cm = recalculate(parent_node, child_node)
    add(parent_node, child_node)
    dpg.set_value(right_flt, len_cm)

def delink_callback(sender, app_data):
    conf = dpg.get_item_configuration(app_data)
    parent_node, child_node = dpg.get_item_parent(conf['attr_1']), dpg.get_item_parent(conf['attr_2'])
    remove(parent_node, child_node)
    dpg.delete_item(app_data)

def input_update(sender, app_data, user_data):
    node = user_data
    for child_node in parent_to_children[node]:
        right_flt = get_node_elt(child_node, flt)
        len_cm = recalculate(node, child_node)
        dpg.set_value(right_flt, len_cm)
    if node in child_to_parent:
        parent_node = child_to_parent[node]
        right_flt = get_node_elt(node, flt)
        len_cm = recalculate(parent_node, node)
        dpg.set_value(right_flt, len_cm)

def add_node():
    node_tag = dpg.generate_uuid()
    with dpg.node(tag=node_tag, label=f'line {node_tag}', parent='node editor'):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_input_float(label=f'length', width=150, callback=input_update, user_data=node_tag)
            px = dpg.add_text()
            dpg.add_button(label=f'move', callback=line.press_move, user_data=(line.tags[-1], px, node_tag))
            dpg.add_button(label=f'delete', callback = delete_node, user_data=(node_tag, line.tags[-1]))
    return px