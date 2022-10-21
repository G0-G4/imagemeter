import dearpygui.dearpygui as dpg
import random

dpg.create_context()

def line_len(line_tag):
    l = dpg.get_item_configuration(line_tag)
    return ((l['p1'][0] - l['p2'][0])**2 + (l['p1'][1] - l['p2'][1])**2)**0.5

width, height, channels, data = dpg.load_image("3.png")
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")

lines = []
line_tags = []
CURR = -1
line_data = {}
def down():
    global CURR
    lines.append([dpg.get_drawing_mouse_pos()])
    CURR = dpg.draw_line(lines[-1][0], dpg.get_drawing_mouse_pos(), color=(0, 0, 0, 255), parent='drawlist')

    dpg.hide_item('down')
    dpg.show_item('drag')

def drag():
    dpg.configure_item(CURR, p2 = dpg.get_drawing_mouse_pos())

def up():
    dpg.hide_item('drag')
    lines[-1].append(dpg.get_drawing_mouse_pos())
    print(dpg.get_drawing_mouse_pos())
    dpg.hide_item('up')
    tag = dpg.draw_line(*lines[-1], color=(255, 0, 0, 255), thickness=3, parent='drawlist')
    line_tags.append(tag)
    inp = dpg.add_input_double(parent='lines', label=f'len line{len(lines)} cm')
    dpg.add_button(parent='lines', label=f'line{len(lines)}', callback=line_button_press, user_data={
        'len': line_len(tag),
        'inp': inp})

def line_button_press(sender, app_data, user_data):
    global line_data
    if line_data:
        len_cm = dpg.get_value(line_data['inp'])/line_data['len'] * user_data['len']
        dpg.set_value(user_data['inp'], len_cm)
        line_data = {}
    else:
        line_data = user_data

with dpg.handler_registry(tag="down"):
    dpg.add_mouse_down_handler(callback=down)
with dpg.handler_registry(tag="up"):
    dpg.add_mouse_release_handler(callback=up)
with dpg.handler_registry(tag="drag"):
    dpg.add_mouse_drag_handler(callback=drag)
dpg.hide_item('down')
dpg.hide_item('drag')
dpg.hide_item('up')


def add_line():
    dpg.show_item('down')
    dpg.show_item('up')


with dpg.window(label="view", tag='view'):
    with dpg.drawlist(tag='drawlist', width=width*2, height=height*2, parent='view'):
        dpg.draw_image("texture_tag", pmin = (50, 50), pmax=(width, height), uv_min = (0, 0), uv_max = (1, 1))
with dpg.window(label="lines", tag='lines'):
    dpg.add_button(label='add line', callback=add_line)

dpg.set_primary_window('view', True)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()