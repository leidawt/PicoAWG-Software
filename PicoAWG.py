"""
PicoAWG V1.0
leida_wt
2023.06.18

https://docs.python.org/3/library/tk.html
https://www.pytk.net/tkinter-helper
"""
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import tkinter.messagebox
import tkinter as tk

# matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

# driver
from picoawg_driver import Pico
# sys
import os
import csv


class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}

    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_tabs_lixb1dlt"] = self.__tk_tabs_lixb1dlt(self)
        self.widget_dic["tk_label_frame_liy6ifpl"] = self.__tk_label_frame_liy6ifpl(
            self)
        self.widget_dic["tk_label_frame_liy6lwhq"] = self.__tk_label_frame_liy6lwhq(
            self)
        self.widget_dic["tk_frame_liy7292o"] = self.__tk_frame_liy7292o(self)
        self.widget_dic["tk_label_liy72kbn"] = self.__tk_label_liy72kbn(self)
        self.preview_fig = Figure(figsize=(3, 3), dpi=80)
        self.preview_canvas = FigureCanvasTkAgg(
            self.preview_fig, master=self.widget_dic["tk_frame_liy7292o"])

    def __win(self):
        self.title("PicoAWG")
        # 设置窗口大小、居中
        width = 522
        height = 419
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 自动隐藏滚动条
    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def __tk_label_liy72kbn(self, parent):
        label = Label(parent, text="波形预览", anchor="center", )
        label.place(x=10, y=180, width=65, height=30)
        return label

    def __tk_tabs_lixb1dlt(self, parent):
        frame = Notebook(parent)

        self.widget_dic["tk_tabs_lixb1dlt_0"] = self.__tk_frame_lixb1dlt_0(
            frame)
        frame.add(self.widget_dic["tk_tabs_lixb1dlt_0"], text="Sine")

        self.widget_dic["tk_tabs_lixb1dlt_1"] = self.__tk_frame_lixb1dlt_1(
            frame)
        frame.add(self.widget_dic["tk_tabs_lixb1dlt_1"], text="Pulse")

        self.widget_dic["tk_tabs_lixb1dlt_2"] = self.__tk_frame_lixb1dlt_2(
            frame)
        frame.add(self.widget_dic["tk_tabs_lixb1dlt_2"], text="Noise")

        self.widget_dic["tk_tabs_lixb1dlt_3"] = self.__tk_frame_lixb1dlt_3(
            frame)
        frame.add(self.widget_dic["tk_tabs_lixb1dlt_3"], text="Sinc")

        self.widget_dic["tk_tabs_lixb1dlt_4"] = self.__tk_frame_lixb1dlt_4(
            frame)
        frame.add(self.widget_dic["tk_tabs_lixb1dlt_4"], text="Arb")

        frame.place(x=10, y=10, width=266, height=151)
        return frame

    def __tk_frame_lixb1dlt_0(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=10, width=266, height=151)

        self.widget_dic["tk_label_liy7jm6i"] = self.__tk_label_liy7jm6i(frame)
        return frame

    def __tk_label_liy7jm6i(self, parent):
        label = Label(parent, text="Sinusoidal", anchor="center", )
        label.place(x=80, y=50, width=82, height=30)
        return label

    def __tk_frame_lixb1dlt_1(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=10, width=266, height=151)

        self.widget_dic["tk_label_liy7kwgm"] = self.__tk_label_liy7kwgm(frame)
        self.widget_dic["tk_label_liy7ldin"] = self.__tk_label_liy7ldin(frame)
        self.widget_dic["tk_label_liy7ley6"] = self.__tk_label_liy7ley6(frame)
        self.widget_dic["tk_input_liy7mlu3"] = self.__tk_input_liy7mlu3(frame)
        self.widget_dic["tk_label_liy7n487"] = self.__tk_label_liy7n487(frame)
        self.widget_dic["tk_input_liy7njo4"] = self.__tk_input_liy7njo4(frame)
        self.widget_dic["tk_input_liy7nliu"] = self.__tk_input_liy7nliu(frame)
        self.widget_dic["tk_label_liy7nnsc"] = self.__tk_label_liy7nnsc(frame)
        self.widget_dic["tk_label_liy7np7k"] = self.__tk_label_liy7np7k(frame)
        return frame

    def __tk_label_liy7kwgm(self, parent):
        label = Label(parent, text="上升时间", anchor="center", )
        label.place(x=10, y=10, width=55, height=30)
        return label

    def __tk_label_liy7ldin(self, parent):
        label = Label(parent, text="下降时间", anchor="center", )
        label.place(x=10, y=50, width=55, height=30)
        return label

    def __tk_label_liy7ley6(self, parent):
        label = Label(parent, text="高值时间", anchor="center", )
        label.place(x=10, y=90, width=55, height=30)
        return label

    def __tk_input_liy7mlu3(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=10, width=110, height=30)
        ipt.insert(0, "10")
        return ipt

    def __tk_label_liy7n487(self, parent):
        label = Label(parent, text="%", anchor="center", )
        label.place(x=190, y=10, width=25, height=30)
        return label

    def __tk_input_liy7njo4(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=50, width=110, height=30)
        ipt.insert(0, "10")
        return ipt

    def __tk_input_liy7nliu(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=90, width=110, height=30)
        ipt.insert(0, "80")
        return ipt

    def __tk_label_liy7nnsc(self, parent):
        label = Label(parent, text="%", anchor="center", )
        label.place(x=190, y=50, width=25, height=30)
        return label

    def __tk_label_liy7np7k(self, parent):
        label = Label(parent, text="%", anchor="center", )
        label.place(x=190, y=90, width=25, height=30)
        return label

    def __tk_frame_lixb1dlt_2(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=10, width=266, height=151)

        self.widget_dic["tk_select_box_liy7o0pw"] = self.__tk_select_box_liy7o0pw(
            frame)
        self.widget_dic["tk_label_liy7o9bs"] = self.__tk_label_liy7o9bs(frame)
        return frame

    def __tk_select_box_liy7o0pw(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("均匀分布", "高斯分布")
        cb.place(x=90, y=20, width=150, height=30)
        cb.current(0)
        return cb

    def __tk_label_liy7o9bs(self, parent):
        label = Label(parent, text="类型", anchor="center", )
        label.place(x=20, y=20, width=50, height=30)
        return label

    def __tk_frame_lixb1dlt_3(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=10, width=266, height=151)

        self.widget_dic["tk_label_liy7r83y"] = self.__tk_label_liy7r83y(frame)
        self.widget_dic["tk_input_liy7rheh"] = self.__tk_input_liy7rheh(frame)
        return frame

    def __tk_label_liy7r83y(self, parent):
        label = Label(parent, text="宽度", anchor="center", )
        label.place(x=20, y=20, width=50, height=30)
        return label

    def __tk_input_liy7rheh(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=90, y=20, width=100, height=30)
        ipt.insert(0, "0.005")
        return ipt

    def __tk_frame_lixb1dlt_4(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=10, width=266, height=151)

        self.widget_dic["tk_text_liy7tt5n"] = self.__tk_text_liy7tt5n(frame)
        # self.widget_dic["tk_button_liy7twqn"] = self.__tk_button_liy7twqn(
        #     frame)
        self.widget_dic["tk_label_liy8gin4"] = self.__tk_label_liy8gin4(frame)
        return frame

    def __tk_text_liy7tt5n(self, parent):
        text = Text(parent)
        text.place(x=10, y=36, width=230, height=80)
        text.insert(INSERT, "./arb_wave.csv")

        return text

    # def __tk_button_liy7twqn(self, parent):
    #     btn = Button(parent, text="加载", takefocus=False,)
    #     btn.place(x=190, y=50, width=50, height=30)
    #     return btn

    def __tk_label_liy8gin4(self, parent):
        label = Label(parent, text="路径/数据", anchor="center", )
        label.place(x=4, y=9, width=63, height=25)
        return label

    def __tk_label_frame_liy6ifpl(self, parent):
        frame = LabelFrame(parent,)

        frame.configure(text="设备连接")
        frame.place(x=290, y=230, width=221, height=150)

        self.widget_dic["tk_select_box_liy6xbef"] = self.__tk_select_box_liy6xbef(
            frame)
        self.widget_dic["tk_button_liy6xsyl"] = self.__tk_button_liy6xsyl(
            frame)
        self.widget_dic["tk_button_liy6y5pw"] = self.__tk_button_liy6y5pw(
            frame)
        self.widget_dic["tk_button_liy700e8"] = self.__tk_button_liy700e8(
            frame)
        self.widget_dic["tk_label_liy70c1g"] = self.__tk_label_liy70c1g(frame)
        return frame

    def __tk_select_box_liy6xbef(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("")
        cb.place(x=10, y=10, width=125, height=30)
        return cb

    def __tk_button_liy6xsyl(self, parent):
        btn = Button(parent, text="连接", takefocus=False,)
        btn.place(x=150, y=8, width=50, height=30)
        return btn

    def __tk_button_liy6y5pw(self, parent):
        btn = Button(parent, text="复位", takefocus=False,)
        btn.place(x=90, y=60, width=50, height=30)
        return btn

    def __tk_button_liy700e8(self, parent):
        btn = Button(parent, text="断开", takefocus=False,)
        btn.place(x=150, y=60, width=50, height=30)
        return btn

    def __tk_label_liy70c1g(self, parent):
        label = Label(parent, text="未连接", anchor="center", )
        label.place(x=20, y=60, width=50, height=30)
        return label

    def __tk_label_frame_liy6lwhq(self, parent):
        frame = LabelFrame(parent,)

        frame.configure(text="波形参数")
        frame.place(x=290, y=10, width=221, height=187)

        self.widget_dic["tk_input_liy6r6p7"] = self.__tk_input_liy6r6p7(frame)
        self.widget_dic["tk_label_liy6rwjx"] = self.__tk_label_liy6rwjx(frame)
        self.widget_dic["tk_label_liy6s46m"] = self.__tk_label_liy6s46m(frame)
        self.widget_dic["tk_label_liy6sg07"] = self.__tk_label_liy6sg07(frame)
        self.widget_dic["tk_input_liy6snys"] = self.__tk_input_liy6snys(frame)
        self.widget_dic["tk_input_liy6sqzb"] = self.__tk_input_liy6sqzb(frame)
        self.widget_dic["tk_label_liy6svie"] = self.__tk_label_liy6svie(frame)
        self.widget_dic["tk_label_liy6t7a1"] = self.__tk_label_liy6t7a1(frame)
        self.widget_dic["tk_label_liy6tlfq"] = self.__tk_label_liy6tlfq(frame)
        self.widget_dic["tk_button_liy71fq2"] = self.__tk_button_liy71fq2(
            frame)
        return frame

    def __tk_input_liy6r6p7(self, parent):
        ipt = Entry(parent,)
        ipt.place(x=80, y=10, width=100, height=30)
        ipt.insert(0, "1e5")
        return ipt

    def __tk_label_liy6rwjx(self, parent):
        label = Label(parent, text="频率", anchor="center", )
        label.place(x=20, y=10, width=50, height=30)
        return label

    def __tk_label_liy6s46m(self, parent):
        label = Label(parent, text="幅值", anchor="center", )
        label.place(x=20, y=50, width=50, height=30)
        return label

    def __tk_label_liy6sg07(self, parent):
        label = Label(parent, text="偏置", anchor="center", )
        label.place(x=20, y=90, width=50, height=30)
        return label

    def __tk_input_liy6snys(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=50, width=100, height=30)
        ipt.insert(0, "2")
        return ipt

    def __tk_input_liy6sqzb(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=90, width=100, height=30)
        ipt.insert(0, "0")
        return ipt

    def __tk_label_liy6svie(self, parent):
        label = Label(parent, text="Hz", anchor="center", )
        label.place(x=186, y=10, width=30, height=30)
        return label

    def __tk_label_liy6t7a1(self, parent):
        label = Label(parent, text="Vpp", anchor="center", )
        label.place(x=186, y=50, width=30, height=30)
        return label

    def __tk_label_liy6tlfq(self, parent):
        label = Label(parent, text="V", anchor="center", )
        label.place(x=186, y=90, width=30, height=30)
        return label

    def __tk_button_liy71fq2(self, parent):
        btn = Button(parent, text="运行", takefocus=False,)
        btn.place(x=20, y=130, width=194, height=30)
        return btn

    def __tk_frame_liy7292o(self, parent):
        frame = Frame(parent,)
        frame.place(x=10, y=220, width=267, height=182)

        return frame


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    # def press_load(self, evt):
    #     print("<Button-1>事件未处理", evt)

    def press_connect(self, evt):
        if not self.pico.is_open():
            self.pico.connect(win.widget_dic["tk_select_box_liy6xbef"].get())
            self.widget_dic["tk_label_liy70c1g"]["text"] = "已连接"
        else:
            return

    def press_reset(self, evt):
        self.pico.reset()

    def press_disconnect(self, evt):
        self.pico.disconnect()
        self.widget_dic["tk_label_liy70c1g"]["text"] = "未连接"

    def press_run(self, evt):
        # type
        wave_type = self.widget_dic["tk_tabs_lixb1dlt"].tab(
            self.widget_dic["tk_tabs_lixb1dlt"].select(), "text")
        # common
        freq = self.widget_dic["tk_input_liy6r6p7"].get()
        amplitude = self.widget_dic["tk_input_liy6snys"].get()
        offset = self.widget_dic["tk_input_liy6sqzb"].get()
        # pulse
        risetime = float(self.widget_dic["tk_input_liy7mlu3"].get())/100
        falltime = float(self.widget_dic["tk_input_liy7njo4"].get())/100
        uptime = float(self.widget_dic["tk_input_liy7nliu"].get())/100
        # noise
        quality = self.widget_dic["tk_select_box_liy7o0pw"].current()
        quality = [1, 10][quality]
        # sinc
        width = self.widget_dic["tk_input_liy7rheh"].get()
        # arb
        arb_data = self.widget_dic["tk_text_liy7tt5n"].get("1.0", "end-1c")

        try:
            # if given path, load it first
            if os.path.exists(arb_data):
                with open(arb_data, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    arb_data = [float(row['value']) for row in reader]
            else:
                reader = csv.DictReader(arb_data.splitlines())
                arb_data = [float(row['value']) for row in reader]
            arb_data = np.array(arb_data)
        except:
            tk.messagebox.showwarning(
                title='Warning', message='Unsupported data type.')
            return
        # print(arb_data)

        wave_args = {
            "freq": freq,
            "amplitude": amplitude,
            "offset": offset,
            "risetime": risetime,
            "falltime": falltime,
            "uptime": uptime,
            "quality": quality,
            "width": width
        }
        print(wave_type)
        print(wave_args)

        # preview
        self.preview_fig.clear()
        self.preview_fig.add_subplot(111).plot(
            self.pico.get_preview_data(wave_type, wave_args, arb_data))
        self.preview_canvas.draw()
        self.preview_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # set device
        if not self.pico.is_open():
            tk.messagebox.showwarning(
                title='Warning', message='Device offline. Connect it first.')
            return
        self.pico.set_wave(wave_type, wave_args, arb_data)

    def __event_bind(self):
        # self.widget_dic["tk_button_liy7twqn"].bind(
        #     '<Button-1>', self.press_load)
        self.widget_dic["tk_button_liy6xsyl"].bind(
            '<Button-1>', self.press_connect)
        self.widget_dic["tk_button_liy6y5pw"].bind(
            '<Button-1>', self.press_reset)
        self.widget_dic["tk_button_liy700e8"].bind(
            '<Button-1>', self.press_disconnect)
        self.widget_dic["tk_button_liy71fq2"].bind(
            '<Button-1>', self.press_run)


if __name__ == "__main__":
    pico = Pico()
    win = Win()
    win.pico = pico
    win.iconbitmap("icon.ico")

    retry = True
    while retry:
        try:
            devices, pico_device = pico.list_ports()
            win.widget_dic["tk_select_box_liy6xbef"]["values"] = devices
            win.widget_dic["tk_select_box_liy6xbef"].current(devices.index(
                pico_device))
            win.press_connect(None)
            break
        except:
            retry = tk.messagebox.askokcancel(
                title='Warning', message='No pico device founded, retry?')

    win.mainloop()
