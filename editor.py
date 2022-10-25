import dearpygui.dearpygui as dpg
import line
from collections import defaultdict


parent_to_children = defaultdict(set)
child_to_parent = dict()

def add(parent, child):
    parent_to_children[parent].add(child)
    child_to_parent[child] = parent

def get_node_flt(node):
    children = dpg.get_item_children(node, 1) # get children from slot 1 (mvNode_Attr_Static)
    flt = dpg.get_item_children(children[2], 1)[0] # get 0 child of node attribute (float input)
    return flt

def get_px(node):
    children = dpg.get_item_children(node, 1)
    px = dpg.get_item_children(children[2], 1)[1]
    return px

def recalculate(parent_node, child_node):
    left = get_node_flt(parent_node)
    left_px, right_px = get_px(parent_node), get_px(child_node)
    left_px = float(dpg.get_value(left_px))
    right_px = float(dpg.get_value(right_px))
    len_cm = dpg.get_value(left)/left_px * right_px
    return len_cm

def link_callback(sender, app_data):
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    parent_node, child_node = dpg.get_item_parent(app_data[0]), dpg.get_item_parent(app_data[1]) # # search for node from input or output
    right = get_node_flt(child_node)
    len_cm = recalculate(parent_node, child_node)
    add(parent_node, child_node)
    dpg.set_value(right, len_cm)

def input_update(sender, app_data, user_data):
    print(sender, app_data, user_data)
    node = user_data
    for child_node in parent_to_children[node]:
        right = get_node_flt(child_node)
        len_cm = recalculate(node, child_node)
        dpg.set_value(right, len_cm)
    if node in child_to_parent:
        left = get_node_flt(child_to_parent[node])
        len_cm = recalculate(node, child_to_parent[node])
        dpg.set_value(left, len_cm)


def add_node():
    with dpg.node(label=f'line {len(line.tags)}', parent='node editor', tag=f'node{len(line.tags)}'):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=f'nodeinp{len(line.tags)}'):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f'nodeoutp{len(line.tags)}'):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static, tag=f'attribute{len(line.tags)}'):
            dpg.add_input_float(label=f'length', width=150, tag=f'inp{len(line.tags)}', callback=input_update, user_data=f'node{len(line.tags)}')
            px = dpg.add_text(tag=f'px{len(line.tags)}')
            dpg.add_button(label=f'move', callback=line.press_move, user_data=(line.tags[-1], px, f'node{len(line.tags)}'))
            dpg.add_button(label=f'delete', callback = line.delete, user_data=(line.tags[-1], f'node{len(line.tags)}'))
            # dpg.add_button(label=f'delete', callback = line.delete, user_data=[f'node{len(line.tags)}'])
    return px