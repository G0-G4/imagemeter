import dearpygui.dearpygui as dpg
import random
import line, editor


dpg.create_context()

with dpg.handler_registry(tag="start_draw"):
    dpg.add_mouse_down_handler(callback=line.start_draw)
with dpg.handler_registry(tag="end_draw"):
    dpg.add_mouse_release_handler(callback=line.end_draw)
with dpg.handler_registry(tag="draw"):
    dpg.add_mouse_drag_handler(callback=line.draw)

with dpg.handler_registry(tag="start_move"):
    dpg.add_mouse_down_handler(callback=line.start_move)
with dpg.handler_registry(tag="move"):
    dpg.add_mouse_drag_handler(callback=line.move)
with dpg.handler_registry(tag="end_move"):
    dpg.add_mouse_release_handler(callback=line.end_move)

dpg.hide_item('start_draw')
dpg.hide_item('draw')
dpg.hide_item('end_draw')
dpg.hide_item('start_move')
dpg.hide_item('move')
dpg.hide_item('end_move')


with dpg.handler_registry(tag="keyboard"):
    dpg.add_key_down_handler(callback=line.shift_down)
    dpg.add_key_release_handler(callback=line.shift_release)

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
    dpg.add_button(label='add line', callback=line.add_line)
    with dpg.node_editor(tag='node editor', callback=editor.link_callback):
        ...

dpg.set_primary_window('view', True)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()