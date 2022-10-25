import dearpygui.dearpygui as dpg
from editor import add_node

tags = []
moving = None
moving_end = None
shift = False

directions = [(1, 0), (0, 1), (0.70710678118, 0.70710678118)]

def len(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def start_draw():
    pos = dpg.get_drawing_mouse_pos()
    tags.append(dpg.draw_line(p1 = pos, p2 = pos, parent='drawlist', color=(0, 0 , 0)))
    dpg.hide_item('start_draw')
    dpg.show_item('draw')
    print(tags)

def get_closest(p1, p2):
    projection = 0
    res = None
    for d in directions:
        vec = (p2[0] - p1[0], p2[1] - p1[1])
        prj = (vec[0] * d[0] + vec[1] * d[1])/len((0, 0), d)
        print(prj)
        if prj != 0 and abs(prj) > abs(projection) :
            projection = prj
            res = (p1[0]+d[0]*projection, p1[1]+d[1]*projection)
    return res

def draw():
    pos = dpg.get_drawing_mouse_pos()
    if shift:
        p1 = dpg.get_item_configuration(tags[-1])['p1']
        if res :=  get_closest(p1, pos):
            pos = res
    dpg.configure_item(tags[-1], p2 = pos)

# @staticmethod
# def link_callback(sender, app_data):
#     dpg.add_node_link(app_data[0], app_data[1], parent=sender)
#     left = get_node_dbl(app_data[0])
#     right = get_node_dbl(app_data[1])
#     print(left, right)

def end_draw():
    dpg.hide_item('draw')
    dpg.hide_item('end_draw')
    add_node()
    # with dpg.node(label=f'line {len(tags)}', parent='node editor', tag=f'node{len(tags)}'):
    #     with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=f'nodeinp{len(tags)}'):
    #         ...
    #     with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=f'nodeoutp{len(tags)}'):
    #         ...
    #     with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static, tag=f'attribute{len(tags)}'):
    #         inp = dpg.add_input_double(label=f'length', width=150, tag=f'inp{len(tags)}')
    #         button = dpg.add_button(label=f'line')
    #         mv = dpg.add_button(label=f'move', callback=press_move, user_data=tags[-1])
    #         # dpg.add_button(label=f'delete', callback = delete, user_data=[inp, button, mv, tags[-1]])
    #         dpg.add_button(label=f'delete', callback = delete, user_data=[f'node{len(tags)}'])

def press_move(sender, app_data, user_data):
    moving = user_data
    dpg.show_item('start_move')

def start_move():
    conf = dpg.get_item_configuration(moving)
    p1, p2 = conf['p1'], conf['p2']
    pos = dpg.get_drawing_mouse_pos()
    if len(p1, pos) <= len(p2, pos):
        moving_end = 'p1'
    else:
        moving_end = 'p2'

    dpg.show_item('move')
    dpg.show_item('end_move')
    dpg.hide_item('start_move')

def move():
    pos = dpg.get_drawing_mouse_pos()
    par = {moving_end: pos}
    dpg.configure_item(moving, **par)

def end_move():
    dpg.hide_item('move')
    dpg.hide_item('end_move')

def shift_down():
    shift = True

def shift_release():
    shift = False

def delete(sender, app_data, user_data):
    for i in user_data:
        dpg.delete_item(i)
    # dpg.delete_item(sender)
    del tags[-1]

def add_line():
    dpg.show_item('start_draw')
    dpg.show_item('end_draw')