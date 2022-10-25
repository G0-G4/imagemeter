import dearpygui.dearpygui as dpg
from editor import add_node, input_update

tags = []
moving = None
moving_end = None
PX = None
shift = False
parent_node = None

directions = [(1, 0), (0, 1), (0.70710678118, 0.70710678118)]

def length(p1, p2):
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
        prj = (vec[0] * d[0] + vec[1] * d[1])/length((0, 0), d)
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

def end_draw():
    dpg.hide_item('draw')
    dpg.hide_item('end_draw')
    px = add_node()
    conf = dpg.get_item_configuration(tags[-1])
    dpg.set_value(px, length(conf['p1'], conf['p2']))

def press_move(sender, app_data, user_data):
    global moving, PX, parent_node
    moving, PX, parent_node = user_data
    print('PX', PX)
    dpg.show_item('start_move')

def start_move():
    global moving_end
    conf = dpg.get_item_configuration(moving)
    p1, p2 = conf['p1'], conf['p2']
    pos = dpg.get_drawing_mouse_pos()
    if length(p1, pos) <= length(p2, pos):
        moving_end = 'p1'
    else:
        moving_end = 'p2'

    dpg.show_item('move')
    dpg.show_item('end_move')
    dpg.hide_item('start_move')

def move():
    global moving_end, PX, parent_node
    pos = dpg.get_drawing_mouse_pos()
    par = {moving_end: pos}
    conf = dpg.get_item_configuration(moving)
    dpg.configure_item(moving, **par)
    print(PX, length(conf['p1'], conf['p2']))
    dpg.set_value(PX, length(conf['p1'], conf['p2']))
    input_update(None, None, parent_node)

def end_move():
    dpg.hide_item('move')
    dpg.hide_item('end_move')

def shift_down():
    global shift
    shift = True

def shift_release():
    global shift
    shift = False

def delete(sender, app_data, user_data):
    for i in user_data:
        dpg.delete_item(i)
    del tags[-1]

def add_line():
    dpg.show_item('start_draw')
    dpg.show_item('end_draw')