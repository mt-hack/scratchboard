'''
Showcase of Kivy Features
=========================

This showcases many features of Kivy. You should see a
menu bar across the top with a demonstration area below. The
first demonstration is the accordion layout. You can see, but not
edit, the kv language code for any screen by pressing the bug or
'show source' icon. Scroll through the demonstrations using the
left and right icons in the top right or selecting from the menu
bar.

The file showcase.kv describes the main container, while each demonstration
pane is described in a separate .kv file in the data/screens directory.
The image data/background.png provides the gradient background while the
icons in data/icon directory are used in the control bar. The file
data/faust_github.jpg is used in the Scatter pane. The icons are
from `http://www.gentleface.com/free_icon_set.html` and licensed as
Creative Commons - Attribution and Non-commercial Use Only; they
sell a commercial license.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/showcase on your Android device.

'''

# encoding: utf-8

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.core.window import Window

from kivy.uix.behaviors import DragBehavior
from kivy.config import Config

import requests
import re
import urllib
import base64
import hashlib
import binascii
import copy

#Window.size = (1366, 768)
#Window.fullscreen = 'auto'
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
#Config.set('graphics', 'resizable', True)
#Config.set('graphics', 'minimum_width', '700')
#Config.set('graphics', 'minimum_height', '600')

datas = []
data_set = {}
text_set = {}

kit = []
offset_x = [0.1, 0.4, 0.7]
offset_y = [ y*0.18-0.1 for y in range(5, 0, -1)]

scratchwindow = None
scratchboard = None
sidebar = None
boardText = None

class CustomDropDown(DropDown):
    def do(self, layout):
        dropdown = CustomDropDown()
        mainbutton = Button(text='Hello', size_hint=(None, None))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #layout.add_widget(dropdown)

class RootWidget(Screen):
    def on_spinner_select(self, text):
        print (text)
    def do(self):
        print("hello world")

class Component(DragBehavior, BoxLayout):
    def on_touch_up(self, touch):
        if self.center_x > scratchboard.x and self.center_x < scratchboard.right \
            and self.center_y > scratchboard.y and self.center_y < scratchboard.top:
            print("Hello")
            boardText.text = ''
            #touch.pos = (touch.ox, touch.oy)
            #scratchwindow.remove_widget(sidebar)
            #scratchwindow.add_widget(origin_sidebar)
        return super(Component, self).on_touch_up(touch)

class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)

class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def create_selector(self, layout):
        request_spinner = Spinner(
            text='<request>',
            values=['POST', 'GET'],
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .08, 'center_y': .95}
        )

        parameter_spinner = Spinner(
            text='<parameter>',
            values=['URL', 'user-agent', 'Referer', 'cookie'],
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .23, 'center_y': 0.95}
        )

        crypto_spinner = Spinner(
            text='<crypto>',
            values=['URLEncode', 'e_base64', 'e_md5', 'e_hex', 'URLDecode', 'd_base64', 'd_hex'],
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .38, 'center_y': .95}
        )

        def visible(self):
            try:
                for i in range(len(kit)):
                    if self == kit[i][0]:
                        if kit[i][1].background_color == [0,0,0,0]:
                            kit[i][1].background_color = [1,1,1,1]
                            kit[i][1].foreground_color = [0,0,0,1]
                        else:
                            kit[i][1].background_color = [0,0,0,0]
                            kit[i][1].foreground_color = [0,0,0,0]
                        return
            except:
                print("failed")

        def show_kit(spinner, text):
            global kit
            if len(kit) >= 15:
                print("Too many!!")
                return

            pos_x = offset_x[len(kit)//5]
            pos_y = offset_y[len(kit)%5]
            gap = 0.25
            slider_len  = .15
            slider_len2 = .1
            if text == "POST" or text == "GET":
                B1 = Button(text = text, size_hint=(None, None), pos_hint={'center_x': pos_x, 'center_y': pos_y}, height=30, width=80)
                B1.bind(on_press=visible);
                T1 = TextInput(text='Response...', multiline=True, size_hint=(None, None), pos_hint={'center_x': pos_x + gap, 'center_y': pos_y}, height=100, width=500, background_color=[0,0,0,0], foreground_color=[0,0,0,0])
                layout.add_widget(B1)
                layout.add_widget(T1)
                if len(kit) == 0:
                    kit.append([B1, T1])
                else:
                    S1 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y+0.1})
                    layout.add_widget(S1)
                    if len(kit)%5 != 4:
                        if len(kit)%5 == 0:
                            S1.size_hint = (slider_len2, slider_len2)
                            S1.pos_hint = {'center_x': pos_x, 'center_y': pos_y+0.07}
                        kit.append([B1, T1, S1])
                    else:
                        S2 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y-0.07})
                        layout.add_widget(S2)
                        kit.append([B1, T1, S1, S2])

                spinner.text = "<request>" 

            elif text == "URL" or text == "user-agent" or text == "Referer" or text == "cookie":
                B1 = Button(text = text, size_hint=(None, None), pos_hint={'center_x': pos_x, 'center_y': pos_y}, height=30, width=80)
                B1.bind(on_press=visible)
                T1 = TextInput(text='', multiline=True, size_hint=(None, None), pos_hint={'center_x': pos_x + gap, 'center_y': pos_y}, height=100, width=500,background_color=[0,0,0,0], foreground_color=[0,0,0,0])
                layout.add_widget(B1)
                layout.add_widget(T1)
                if len(kit) == 0:
                    kit.append([B1, T1])
                else:
                    S1 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y+0.1})
                    layout.add_widget(S1)
                    if len(kit)%5 != 4:
                        if len(kit)%5 == 0:
                            S1.size_hint = (slider_len2, slider_len2)
                            S1.pos_hint = {'center_x': pos_x, 'center_y': pos_y+0.07}
                        kit.append([B1, T1, S1])
                    else:
                        S2 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y-0.07})
                        layout.add_widget(S2)
                        kit.append([B1, T1, S1, S2])

                spinner.text = "<parameter>"
            elif text == "URLEncode" or text == "URLDecode" or text[0] == 'e' or text[0] == 'd':
                B1 = Button(text = text, size_hint=(None, None), pos_hint={'center_x': pos_x, 'center_y': pos_y}, height=30, width=80)
                B1.bind(on_press=visible)
                T1 = TextInput(text='', multiline=True, size_hint=(None, None), pos_hint={'center_x': pos_x + gap, 'center_y': pos_y}, height=100, width=500,background_color=[0,0,0,0], foreground_color=[0,0,0,0])
                layout.add_widget(B1)
                layout.add_widget(T1)
                if len(kit) == 0:
                    kit.append([B1, T1])
                else:
                    S1 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y+0.1})
                    layout.add_widget(S1)
                    if len(kit)%5 != 4:
                        if len(kit)%5 == 0:
                            S1.size_hint = (slider_len2, slider_len2)
                            S1.pos_hint = {'center_x': pos_x, 'center_y': pos_y+0.07}
                        kit.append([B1, T1, S1])
                    else:
                        S2 = Slider(orientation='vertical', value=0, min=0, max=0, size_hint=(slider_len,slider_len), pos_hint={'center_x': pos_x, 'center_y': pos_y-0.07})
                        layout.add_widget(S2)
                        kit.append([B1, T1, S1, S2])

                spinner.text = "<crypto>"

        def remove_one(self):
            global kit
            if len(kit) == 0:
                return
            
            for widget in kit[-1]:
                layout.remove_widget(widget)
            kit.remove(kit[-1])

        def start(self):
            headers_ = {}
            params = []
            url = ""
            output = ""
            for i in range(len(kit)):
                input = kit[i][1].text if kit[i][1].text != "" else output
                if kit[i][0].text == 'POST' or kit[i][0].text == 'GET':
                    try:
                        if kit[i][0].text[0] == 'P':
                            r = requests.post(url, headers=headers_, data=params, timeout=5)
                        else:
                            r = requests.get(url, headers=headers_, timeout=5)

                        r.encoding = 'utf-8'
                        print(r.encoding)
                        print(r.text)
                        print(headers_)
                        kit[i][1].text = bytes(r.text, 'utf-8')
                        params = []
                        headers_ = {}
                        url = ""
                    except:
                        print("Invalid argument")

                elif kit[i][0].text == 'URL' or kit[i][0].text == "user-agent" or kit[i][0].text == "Referer" or kit[i][0].text == "cookie":
                    if kit[i][0].text == "URL":
                        url = kit[i][1].text
                    else:
                        headers_[kit[i][0].text] = kit[i][1].text

                elif kit[i][0].text == "URLEncode" or kit[i][0].text == "URLDecode" or kit[i][0].text[0] == 'e' or kit[i][0].text[0] == 'd':
                    if kit[i][0].text == "URLEncode":
                        kit[i][1].text = urllib.parse.quote(input)
                    elif kit[i][0].text == "URLDecode":
                        kit[i][1].text = urllib.parse.unquote(input)
                    elif kit[i][0].text == 'e_base64':
                        kit[i][1].text = base64.b64encode(bytes(input, 'utf-8'))
                    elif kit[i][0].text == 'e_md5':
                        m = hashlib.md5()
                        m.update(bytes(input, 'utf-8'))
                        kit[i][1].text = m.hexdigest()
                    elif kit[i][0].text == 'e_hex':
                        kit[i][1].text = binascii.hexlify(bytes(input, 'utf-8'))
                    elif kit[i][0].text == 'd_base64':
                        print(input)
                        kit[i][1].text = base64.b64decode(bytes(input, 'utf-8'))
                    elif kit[i][0].text == 'd_hex':
                        kit[i][1].text = binascii.unhexlify(bytes(input, 'utf-8'))
                
                output = kit[i][1].text

        request_spinner.bind(text=show_kit)
        parameter_spinner.bind(text=show_kit)
        crypto_spinner.bind(text=show_kit)
        layout.add_widget(request_spinner)
        layout.add_widget(parameter_spinner)
        layout.add_widget(crypto_spinner)

        clear = Button(size_hint=(None, None), pos_hint={'center_x': 0.75, 'center_y': 0.95}, height=30, width=80, text='Clear')
        clear.bind(on_press=remove_one)
        layout.add_widget(clear)
        test = Button(size_hint=(None, None), pos_hint={'center_x': 0.93, 'center_y': 0.95}, height=30, width=80, text='test')
        test.bind(on_press=start)
        layout.add_widget(test)

    def init_scratch(self, window, board, text, toolbox):
        global scratchboard, sidebar, scratchwindow, boardText
        scratchwindow = window
        scratchboard = board
        sidebar = toolbox
        boardText = text

    def build(self):
        self.title = 'SCRATCHED BOARD'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = [
            "SCRATCH BOARD", 'send packets', "Note", "Encode", "Scratch"
        ]
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def send_get_request(self, url, user_agent, referer, cookie, output):
        print("sending......")
        headers_ = {}
        if user_agent.text:
            headers_['user-agent'] = user_agent.text
        if referer.text:
            headers_['Referer'] = referer.text
        if cookie.text:
            headers_['cookies'] = cookie.text
        try:
            r = requests.get(url.text, headers = headers_, timeout=5)
            r.encoding = 'utf-8'
            output.foreground_color = (0, 0, 0, 1)
            output.text = r.text
        except:
            print("Invalid Parameters !")
            output.foreground_color = (1, 0, 0, 1)
            output.text = "Invalid Parameters !"
        
    def send_post_request(self, url, user_agent, referer, cookie, output):
        print("sending......")
        headers_ = {}
        params = {}
        if user_agent.text:
            headers_['user-agent'] = user_agent.text
        if referer.text:
            headers_['Referer'] = referer.text
        if cookie.text:
            headers_['cookies'] = cookie.text
        try:
            r = requests.post(URL.text, headers = headers_, data=params, timeout=5)
            r.encoding = 'utf-8'
            output.foreground_color = (0, 0, 0, 1)
            output.text = r.text
        except:
            print("Invalid Parameters !")
            output.foreground_color = (1, 0, 0, 1)
            output.text = "Invalid Parameters !"

    # Deprecated
    def showcase_boxlayout(self, layout):
        def getPostData(self):
            try:
                global datas
                datas = []
                html = requests.get(URL.text).text
                pos = 0
                while pos != -1:
                        pos1 = html.find('<input')
                        pos2 = html.find('<textarea')
                        if pos1 == -1:
                            pos = pos2
                        elif pos2 == -1:
                            pos = pos1
                        else:
                            pos = min(pos1, pos2)

                        pos_end = html[pos:].find('>')
                        name = re.search("name[^\S]*=[^\S]*[\'\"][\w]*[\'\"]", html[pos:pos+pos_end+1])
                        if name:
                            name = name.group().replace('\'', '\"').split('\"')[1]
                            datas.append(name)
                        html = html[pos+pos_end+1:]
            except:
                print("Invalid URL")
            
            # add box for each data
            for i, data in enumerate(datas):
                data_set[i] = Label(text = data, size_hint=(None, None), x=130, y=230-i*50, height=30, width=80)
                layout.add_widget(data_set[i])
                text_set[i] = TextInput(text='', multiline=False, x = 200, y=230-i*50,size_hint=(None, None), height=30, width=300)
                layout.add_widget(text_set[i])


        def do_something(self):
            print("sending......")
            print(user_agent.text)
            headers_ = {}
            if user_agent.text:
                headers_['user-agent'] = user_agent.text
            if Referer.text:
                headers_['Referer'] = Referer.text
            if cookie.text:
                headers_['cookies'] = cookie.text

            print(datas)
            params = {}
            for i, d in enumerate(datas):
            	params[d] = text_set[i].text

            print(params)

            
            try:
                r = requests.post(URL.text, headers = headers_, data=params, timeout=5)
                r.encoding = 'utf-8'
                print(r.text)
            except:
                print("Invalid Parameters !")
        
        URL = TextInput(text='', multiline=False, x = 150, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URL)
        user_agent = TextInput(text='', multiline=False, x = 150, y=385,size_hint=(None, None), height=30, width=300)
        layout.add_widget(user_agent)
        Referer = TextInput(text='', multiline=False, x = 150, y=335,size_hint=(None, None), height=30, width=300)
        layout.add_widget(Referer)
        cookie = TextInput(text='', multiline=False, x = 150, y=285,size_hint=(None, None), height=30, width=300)
        layout.add_widget(cookie)
        confirm = Button(size_hint=(None, None), x=650, y=50, height=30, width=80, text='send')
        layout.add_widget(confirm)
        confirm.bind(on_press=do_something)
        postData = Button(size_hint=(None, None),x=60,y=230,height=40,width=80,text='Post')
        layout.add_widget(postData)
        postData.bind(on_press=getPostData)
    
    def do_url_encode(self, input, answer_label):
        answer = urllib.parse.quote(input.text)
        answer_label.text = str(answer)

    def do_base64encode(self, input, answer_label):            
        answer = base64.b64encode(bytes(input.text, 'utf-8'))
        answer_label.text = answer.decode('utf-8')
        
    def do_md5encode(self, input, answer_label):
        m = hashlib.md5()
        m.update(bytes(input.text, 'utf-8'))
        answer = m.hexdigest()
        answer_label.text = str(answer)

    def do_hexencode(self, input, answer_label):
        try:
            answer = binascii.hexlify(bytes(input.text, 'utf-8'))
            answer_label.text = answer.decode('utf-8')
        except:
            print("[hex] Invalid input")
    
    def search_source_code(self, layout):
        def search(self):
            try:
                code = requests.get(URL.text, timeout=5).text()
                print(code)
            except:
                print("Invlid URL")

        confirm = Button(size_hint=(None, None), x=320, y=200, width=100, height=33, text='search')
        confirm.bind(on_press=search)
        layout.add_widget(confirm)
        URL = TextInput(text='', multiline=False, x = 140, y=255,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URL)

    def do_base64decode(self, input, answer_label):
        try:        
            answer = base64.b64decode(bytes(input.text, 'utf-8'))
            answer = answer.decode('utf-8')
        except:
            answer = "Invalid Input!!!"
        answer_label.text = answer

    def do_md5decode(self, input, answer_label):
        m = hashlib.md5()
        m.update(bytes(input.text, 'utf-8'))
        answer = m.hexdigest()
        answer_label.text = str(answer)

    def do_hexdecode(self, input, answer_label):
        try:
            answer = binascii.unhexlify(bytes(input.text, 'utf-8'))
            answer = answer.decode('utf-8')
        except:
            answer = "Invalid Input!!!"
            print("[hex] Invalid input")
        answer_label.text = answer
    def showcase_gridlayout(self, layout):
        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    ShowcaseApp().run()
