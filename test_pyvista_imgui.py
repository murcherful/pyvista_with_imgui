import sys
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import pyvista as pv
import time
import pyautogui
from threading import Thread

screen_width, screen_height = pyautogui.size()

font_scale = 1.75
size = 1500, 1000
background_color = [1, 1, 1]

class PyVistaWin:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = screen_height
        self.h = screen_height
        # self.full_screen = False        # abort
        self.is_open = False
        self.thread = None
        self.shpere_radius = 1.0
    
    def reset_window(self):
        self.x = 0
        self.y = 0
        self.w = screen_height
        self.h = screen_height

    def close(self):
        self.is_open = False
        self.thread = None

    def loop_core(self):

        # your pyvista code here

        self.is_open = True

        self.plotter = pv.Plotter()
        self.window = self.plotter.render_window
        self.window.SetBorders(0)
        self.window.SetSize(self.w, self.h)
        self.window.SetPosition(self.x, self.y)

        sphere = pv.Sphere(radius=1) 
        self.plotter.add_mesh(sphere, name='data', cmap='gist_ncar')
        self.plotter.show(interactive_update=True)
        # main pyvista loop
        while True:
            if not self.is_open:
                self.plotter.close()
                break 
            # your operation here or your models here
            new_sphere = pv.Sphere(radius=self.shpere_radius)
            self.plotter.add_mesh(new_sphere, name='data', cmap='gist_ncar')
            self.window.SetSize(self.w, self.h)
            self.window.SetPosition(self.x, self.y)
            self.plotter.update()
            time.sleep(0.02)

    def open(self):
        if self.is_open:
            return
        self.thread = Thread(target=self.loop_core)
        self.thread.start()



def main():
    global font_scale, background_color

    # pygame init, see: https://github.com/pyimgui/pyimgui/blob/master/doc/examples/integrations_pygame.py
    pygame.init()
    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption('Demo')
    
    # imgui init
    imgui.create_context()
    impl = PygameRenderer()
    # imgui window setting
    io = imgui.get_io()
    io.display_size = size

    # pyvista rendering window
    pv_win = PyVistaWin()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pv_win.close()
                time.sleep(0.5)
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        is_expand, show_custom_window = imgui.begin("Render Window Settings", False)
        imgui.set_window_font_scale(font_scale)
        if is_expand:
            expanded, visible = imgui.collapsing_header("Position", flags=imgui.TREE_NODE_DEFAULT_OPEN)
            if expanded:
                changed, pv_win.x = imgui.slider_int("Position X", pv_win.x, 0, screen_width)
                changed, pv_win.y = imgui.slider_int("Position Y", pv_win.y, 0, screen_height)
            expanded, visible = imgui.collapsing_header("Size", flags=imgui.TREE_NODE_DEFAULT_OPEN)
            if expanded:
                changed, pv_win.w = imgui.slider_int("Width", pv_win.w, 0, screen_width)
                changed, pv_win.h = imgui.slider_int("Height", pv_win.h, 0, screen_height)
            # clicked, pv_win.full_screen = imgui.checkbox("Fullscreen", pv_win.full_screen)

        imgui.begin_group()
        clicked = imgui.button("Open")
        if clicked:
            pv_win.open()
        imgui.same_line()
        clicked = imgui.button("Close")
        if clicked:
            pv_win.close()
        imgui.same_line()
        clicked = imgui.button("Reset Window")
        if clicked:
            pv_win.reset_window()
        imgui.end_group()
        imgui.end()

        is_expand, show_custom_window = imgui.begin("Imgui Settings", False)
        imgui.set_window_font_scale(font_scale)
        if is_expand:
            changed, font_scale = imgui.slider_float("Font Scale", font_scale, 0.1, 5)
            changed, background_color = imgui.color_edit3('Background Color', *background_color)
            clicked = imgui.button("Reset Settings")
            if clicked:
                font_scale = 1.75
                background_color = [1, 1, 1]
        imgui.end()

        # your gui here
        is_expand, show_custom_window = imgui.begin("Test Change Sphere", False)
        imgui.set_window_font_scale(font_scale)
        if is_expand:
            changed, pv_win.shpere_radius = imgui.slider_float("Radius", pv_win.shpere_radius, 0.1, 10)
        imgui.end()

        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL sufraces
        # gl.glClearColor(0, 0, 0, 1)
        gl.glClearColor(background_color[0], background_color[1], background_color[2], 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()


if __name__ == "__main__":
    main()