import dearpygui.dearpygui as dpg
import line
from collections import defaultdict


connections = defaultdict(set)


def get_node_dbl(io):
    node = dpg.get_item_parent(io)
    children = dpg.get_item_children(node, 1)
    dbl = dpg.get_item_children(children[2], 1)[0]
    return dbl


def link_callback(sender, app_data):
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    left = get_node_dbl(app_data[0])
    right = get_node_dbl(app_data[1])
    connections[left].add(right)
    print(dpg.get_value(left), dpg.get_value(right))


def add_node():
    with dpg.node(label=f'line {len(line.tags)}', parent='node editor', tag=f'node{len(line.tags)}'):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=f'nodeinp{len(line.tags)}'):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f'nodeoutp{len(line.tags)}'):
            ...
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static, tag=f'attribute{len(line.tags)}'):
            inp = dpg.add_input_double(label=f'length', width=150, tag=f'inp{len(line.tags)}')
            button = dpg.add_button(label=f'line')
            mv = dpg.add_button(label=f'move', callback=line.press_move, user_data=line.tags[-1])
            dpg.add_button(label=f'delete', callback = line.delete, user_data=[line.tags[-1], f'node{len(line.tags)}'])
            # dpg.add_button(label=f'delete', callback = line.delete, user_data=[f'node{len(line.tags)}'])