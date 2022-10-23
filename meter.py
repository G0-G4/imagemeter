import dearpygui.dearpygui as dpg
import random

class Line():

    tags = []
    moving = None
    moving_end = None
    shift = False

    directions = [(1, 0), (0, 1), (0.70710678118, 0.70710678118)]


    @staticmethod
    def len(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    @staticmethod
    def start_draw():
        pos = dpg.get_drawing_mouse_pos()
        Line.tags.append(dpg.draw_line(p1 = pos, p2 = pos, parent='drawlist', color=(0, 0 , 0)))
        dpg.hide_item('start_draw')
        dpg.show_item('draw')
        print(Line.tags)

    @staticmethod
    def get_closest(p1, p2):
        projection = 0
        res = None
        for d in Line.directions:
            vec = (p2[0] - p1[0], p2[1] - p1[1])
            prj = (vec[0] * d[0] + vec[1] * d[1])/Line.len((0, 0), d)
            print(prj)
            if prj != 0 and abs(prj) > abs(projection) :
                projection = prj
                res = (p1[0]+d[0]*projection, p1[1]+d[1]*projection)
        return res

    @staticmethod
    def draw():
        pos = dpg.get_drawing_mouse_pos()
        if Line.shift:
            p1 = dpg.get_item_configuration(Line.tags[-1])['p1']
            if res :=  Line.get_closest(p1, pos):
                pos = res
        dpg.configure_item(Line.tags[-1], p2 = pos)

    @staticmethod
    def end_draw():
        dpg.hide_item('draw')
        dpg.hide_item('end_draw')
        inp = dpg.add_input_double(parent='lines', label=f'len line{len(Line.tags)}')
        button = dpg.add_button(parent='lines', label=f'line{len(Line.tags)}')
        mv = dpg.add_button(parent='lines', label=f'move line{len(Line.tags)}', callback=Line.press_move, user_data=Line.tags[-1])
        dpg.add_button(parent='lines', label=f'delete{len(Line.tags)}', callback = Line.delete, user_data=[inp, button, mv, Line.tags[-1]])

    @staticmethod
    def press_move(sender, app_data, user_data):
        Line.moving = user_data
        dpg.show_item('start_move')

    @staticmethod
    def start_move():
        conf = dpg.get_item_configuration(Line.moving)
        p1, p2 = conf['p1'], conf['p2']
        pos = dpg.get_drawing_mouse_pos()
        if Line.len(p1, pos) <= Line.len(p2, pos):
            Line.moving_end = 'p1'
        else:
            Line.moving_end = 'p2'

        dpg.show_item('move')
        dpg.show_item('end_move')
        dpg.hide_item('start_move')

    @staticmethod
    def move():
        pos = dpg.get_drawing_mouse_pos()
        par = {Line.moving_end: pos}
        dpg.configure_item(Line.moving, **par)

    @staticmethod
    def end_move():
        dpg.hide_item('move')
        dpg.hide_item('end_move')

    @staticmethod
    def shift_down():
        Line.shift = True

    @staticmethod
    def shift_release():
        Line.shift = False

    @staticmethod
    def delete(sender, app_data, user_data):
        for i in user_data:
            dpg.delete_item(i)
        dpg.delete_item(sender)
        del Line.tags[-1]

    @staticmethod
    def add_line():
        dpg.show_item('start_draw')
        dpg.show_item('end_draw')


dpg.create_context()

with dpg.handler_registry(tag="start_draw"):
    dpg.add_mouse_down_handler(callback=Line.start_draw)
with dpg.handler_registry(tag="end_draw"):
    dpg.add_mouse_release_handler(callback=Line.end_draw)
with dpg.handler_registry(tag="draw"):
    dpg.add_mouse_drag_handler(callback=Line.draw)

with dpg.handler_registry(tag="start_move"):
    dpg.add_mouse_down_handler(callback=Line.start_move)
with dpg.handler_registry(tag="move"):
    dpg.add_mouse_drag_handler(callback=Line.move)
with dpg.handler_registry(tag="end_move"):
    dpg.add_mouse_release_handler(callback=Line.end_move)

dpg.hide_item('start_draw')
dpg.hide_item('draw')
dpg.hide_item('end_draw')
dpg.hide_item('start_move')
dpg.hide_item('move')
dpg.hide_item('end_move')


with dpg.handler_registry(tag="keyboard"):
    dpg.add_key_down_handler(callback=Line.shift_down)
    dpg.add_key_release_handler(callback=Line.shift_release)

width, height, channels, data = dpg.load_image("109763.jpg")
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")



# def line_button_press(sender, app_data, user_data):
#     global line_data
#     if line_data:
#         len_cm = dpg.get_value(line_data['inp'])/line_data['len'] * user_data['len']
#         dpg.set_value(user_data['inp'], len_cm)
#         line_data = {}
#     else:
#         line_data = user_data



with dpg.window(label="view", tag='view'):
    with dpg.drawlist(tag='drawlist', width=width*2, height=height*2, parent='view'):
        dpg.draw_image("texture_tag", pmin = (50, 50), pmax=(width, height), uv_min = (0, 0), uv_max = (1, 1))
with dpg.window(label="lines", tag='lines'):
    dpg.add_button(label='add line', callback=Line.add_line)

dpg.set_primary_window('view', True)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()