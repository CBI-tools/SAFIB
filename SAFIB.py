from autoscript_sdb_microscope_client import SdbMicroscopeClient
from autoscript_sdb_microscope_client.enumerations import *
from autoscript_sdb_microscope_client.structures import *
import math, os, json, time, threading
import tkinter as tk
import tkinter.filedialog as tkf
from PIL import Image, ImageDraw


def point_input_ui():
    win = Point_input()
    win.mainloop()


def test_mill_angle(content):
    try:
        if float(content) > 0 and float(content) < 28:
            return True
        else:
            return False
    except:
        return False


def test_float(content):
    try:
        if float(content) > 0:
            return True
        else:
            return False
    except:
        return False


def test_center_x(content):
    try:
        float(content)
        return True
    except:
        return False


def test_thickness(content):
    try:
        if float(content) > 0.5:
            return True
        else:
            return False
    except:
        return False

class Point_input:
    def __init__(self, root=tk.Tk()):
        #for button control
        self.__button_group_list = []
        #for map canvas point control
        #self.__canv_points = {}

        # build window __main_win
        self.__main_win = root
        self.__main_win.title("auto slice point_input")
        self.__main_win.overrideredirect(True)
        test_mill_angle_TMD = self.__main_win.register(test_mill_angle)
        test_float_TMD = self.__main_win.register(test_float)
        # build frame main at row 0 in __main_win
        self.__frame_main = tk.Frame(self.__main_win)
        self.__frame_main.grid(row=0)
        # build button "open folder" at row 0, column 0 in __frame_main
        self.__button_open_folder = tk.Button(self.__frame_main,text="user_folder",command=self._open_folder_dialg)
        self.__button_open_folder.grid(row=0,column=0)
        self.__button_group_list.append(self.__button_open_folder)
        # build label "open folder" at row 0, column 1-4 in __frame_main
        self.__label_open_folder_txt = tk.StringVar()
        self.__label_open_folder = tk.Label(self.__frame_main,textvariable=self.__label_open_folder_txt)
        self.__label_open_folder.grid(row=0,column=1,columnspan=4)
        # build button "set reference" at row 1, column0-1 in __frame_main
        self.__button_set_ref = tk.Button(self.__frame_main,text="set reference",command=self._set_ref_point)
        self.__button_set_ref.grid(row=1,column=0,columnspan=2)
        self.__button_group_list.append(self.__button_set_ref)
        #build button "take map" at row 1, column 2 in __frame_main
        self.__button_take_map = tk.Button(self.__frame_main, text="take map image", command=self._take_e_map)
        self.__button_take_map.grid(row=1, column=2)
        self.__button_group_list.append(self.__button_take_map)
        # build button "load map" at row 1, column3 in __frame_main
        self.__button_load_map = tk.Button(self.__frame_main, text="load map", command=self._load_e_map)
        self.__button_load_map.grid(row=1, column=3)
        self.__button_group_list.append(self.__button_load_map)
        # build button "load points" at row 1, column 3 in __frame_main
        #self.__button_load_point = tk.Button(self.__frame_main, text="load points", command=self._load_points)
        #self.__button_load_point.grid(row=1, column=4)
        #self.__button_group_list.append(self.__button_load_point)
        # build button "clear all" at row 1, column5 in __frame_main
        #self.__button_clear_point = tk.Button(self.__frame_main, text="clear all points", command=self._clear_all_points)
        #self.__button_clear_point.grid(row=1, column=5)
        #self.__button_group_list.append(self.__button_clear_point)
        # build label "points" at row 2, column 1-5 in __frame_main
        tk.Label(self.__frame_main,text="name, stage_x, stage_y, stage_z, milling_angle, thinned").grid(row=2,column=0,columnspan=4)
        # build frame "points" at row 3, column 0-5 in __frame_main
        self.__frame_points = tk.Frame(self.__frame_main)
        self.__frame_points.grid(row=3,column=0,columnspan=6)
        # build listbox "points" at row in __frame_points
        self.__scrollbar_points = tk.Scrollbar(self.__frame_points)
        self.__scrollbar_points.pack(side=tk.RIGHT,fill=tk.Y)
        self.__listbox_points = tk.Listbox(self.__frame_points,width=80,height=10,selectmode=tk.SINGLE,yscrollcommand=self.__scrollbar_points.set)
        self.__listbox_points.pack(side=tk.LEFT,fill=tk.BOTH)
        self.__scrollbar_points.config(command=self.__listbox_points.yview)
        # build frame "settings" at row 4 in __main_win
        self.__frame_settings = tk.Frame(self.__main_win)
        self.__frame_settings.grid(row=4)
        # build button "add point" at row 0, column 0 in __frame_settings
        self.__button_add_point = tk.Button(self.__frame_settings,text="add point",command=lambda: self._thread_function(self._add_point))
        self.__button_add_point.grid(row=0,column=0)
        self.__button_group_list.append(self.__button_add_point)
        # build button "update point" at row 0, column 1 in __frame_settings
        self.__button_update_point = tk.Button(self.__frame_settings, text="update point", command=lambda: self._thread_function(self._update_point))
        self.__button_update_point.grid(row=0, column=1)
        self.__button_group_list.append(self.__button_update_point)
        # build button "update point" at row 0, column 2 in __frame_settings
        self.__button_E_correct = tk.Button(self.__frame_settings, text="E correct", command=lambda: self._thread_function(self._E_correct))
        self.__button_E_correct.grid(row=0, column=2)
        self.__button_group_list.append(self.__button_E_correct)
        # build button "delete point" at row 0, column 3 in __frame_settings
        self.__button_delete_point = tk.Button(self.__frame_settings, text="delete point", command=self._delete_point)
        self.__button_delete_point.grid(row=0, column=3)
        self.__button_group_list.append(self.__button_delete_point)
        # build button "goto point" at row 0, column 4 in __frame_settings
        self.__button_goto_point = tk.Button(self.__frame_settings, text="goto point", command=lambda: self._thread_function(self._goto_point))
        self.__button_goto_point.grid(row=0, column=4)
        self.__button_group_list.append(self.__button_goto_point)
        # build button "update pattern" at row 0, column 5 in __frame_settings
        self.__button_update_point_pattern = tk.Button(self.__frame_settings, text="update pattern",
                                             command=self._update_point_pattern)
        self.__button_update_point_pattern.grid(row=0, column=5)
        self.__button_group_list.append(self.__button_update_point_pattern)
        # build label "settings for taking image with electron beam" at row 0, column 1-3 in __frame_settings
        tk.Label(self.__frame_settings, text="settings for taking image").grid(row=1, column=0,columnspan=5)
        # build label "Magnification" at row 2, column 1 in __frame_settings
        tk.Label(self.__frame_settings, text="Magnification").grid(row=2, column=1)
        # build label "high tension" at row 2, column 2 in __frame_settings
        tk.Label(self.__frame_settings, text="high tension").grid(row=2, column=2)
        # build label "beam current" at row 2, column 3 in __frame_settings
        tk.Label(self.__frame_settings, text="beam current").grid(row=2, column=3)
        # build label "dwell time" at row 2, column 4 in __frame_settings
        tk.Label(self.__frame_settings, text="dwell time").grid(row=2, column=4)
        # build label "resolution" at row 2, column 5 in __frame_settings
        tk.Label(self.__frame_settings, text="resolution").grid(row=2, column=5)
        # build label "electron" at row 3, column 0 in __frame_settings
        tk.Label(self.__frame_settings, text="electron").grid(row=3, column=0)
        # build option "E_Magnification" at row 3, column 1 in __frame_settings
        self.__option_E_mag_txt = tk.StringVar()
        self.__option_E_mag_values = ["42x","100x","350x","500x","800x","1000x"]
        self.__option_E_mag_dict = {"42x":0.003,"100x":0.00127, "350x":3.63e-04, "500x":2.54e-04, "800x":1.59e-04, "1000x":0.000127}
        self.__option_E_mag_txt.set(self.__option_E_mag_values[2])
        self.__option_E_mag = tk.OptionMenu(self.__frame_settings,self.__option_E_mag_txt,*self.__option_E_mag_values)
        self.__option_E_mag.grid(row=3, column=1)
        # build option "E_HT" at row 3, column 2 in __frame_settings
        self.__option_E_HT_txt = tk.StringVar()
        self.__option_E_HT_values = ["3.0 kV"]
        self.__option_E_HT_txt.set(self.__option_E_HT_values[0])
        self.__option_E_HT = tk.OptionMenu(self.__frame_settings, self.__option_E_HT_txt, *self.__option_E_HT_values)
        self.__option_E_HT.grid(row=3, column=2)
        # build option "E_BC" at row 3, column 3 in __frame_settings
        self.__option_E_BC_txt = tk.StringVar()
        self.__option_E_BC_values = ["25 pA", "50 pA","0.10 nA","0.2 nA","0.4 nA"]
        self.__option_E_BC_txt.set(self.__option_E_BC_values[2])
        self.__option_E_BC = tk.OptionMenu(self.__frame_settings, self.__option_E_BC_txt,*self.__option_E_BC_values)
        self.__option_E_BC.grid(row=3, column=3)
        # build option "E_Dtime" at row 3, column 4 in __frame_settings
        self.__option_E_Dtime_txt = tk.StringVar()
        self.__option_E_Dtime_values = ["25 ns", "50 ns", "100 ns", "200 ns","300 ns","500 ns","1 us"]
        self.__option_E_Dtime_txt.set(self.__option_E_Dtime_values[2])
        self.__option_E_Dtime = tk.OptionMenu(self.__frame_settings, self.__option_E_Dtime_txt, *self.__option_E_Dtime_values)
        self.__option_E_Dtime.grid(row=3, column=4)
        # build option "E_resolution" at row 3, column 5 in __frame_settings
        self.__option_E_resolution_txt = tk.StringVar()
        self.__option_E_resolution_values = ["768x512", "1536x1024"]
        self.__option_E_resolution_txt.set(self.__option_E_resolution_values[1])
        self.__option_E_resolution = tk.OptionMenu(self.__frame_settings, self.__option_E_resolution_txt,*self.__option_E_resolution_values)
        self.__option_E_resolution.grid(row=3, column=5)
        # build label "ion" at row 4, column 0 in __frame_settings
        tk.Label(self.__frame_settings, text="ion").grid(row=4, column=0)
        # build option "I_Magnification" at row 4, column 1 in __frame_settings
        self.__option_I_mag_txt = tk.StringVar()
        self.__option_I_mag_values = ["1000x","1500x", "2000x", "2500x"]
        self.__option_I_mag_dict = {"1000x":0.000127, "1500x":8.47e-05, "2000x":6.35e-05, "2500x":5.08e-05}
        self.__option_I_mag_txt.set(self.__option_I_mag_values[2])
        self.__option_I_mag = tk.OptionMenu(self.__frame_settings, self.__option_I_mag_txt, *self.__option_I_mag_values)
        self.__option_I_mag.grid(row=4, column=1)
        # build option "I_HT" at row 4, column 2 in __frame_settings
        self.__option_I_HT_txt = tk.StringVar()
        self.__option_I_HT_values = ["30.0 kV"]
        self.__option_I_HT_txt.set(self.__option_I_HT_values[0])
        self.__option_I_HT = tk.OptionMenu(self.__frame_settings, self.__option_I_HT_txt, *self.__option_I_HT_values)
        self.__option_I_HT.grid(row=4, column=2)
        # build option "I_BC" at row 4, column 3 in __frame_settings
        self.__option_I_BC_txt = tk.StringVar()
        self.__option_I_BC_values = ["10 pA", "30 pA", "50 pA","0.10 nA", "0.3 nA","0.5 nA","1.0 nA"]
        self.__option_I_BC_txt.set(self.__option_I_BC_values[3])
        self.__option_I_BC = tk.OptionMenu(self.__frame_settings, self.__option_I_BC_txt, *self.__option_I_BC_values)
        self.__option_I_BC.grid(row=4, column=3)
        # build option "I_Dtime" at row 4, column 4 in __frame_settings
        self.__option_I_Dtime_txt = tk.StringVar()
        self.__option_I_Dtime_values = ["25 ns","50 ns", "100 ns", "200 ns", "300 ns", "500 ns", "1 us"]
        self.__option_I_Dtime_txt.set(self.__option_I_Dtime_values[2])
        self.__option_I_Dtime = tk.OptionMenu(self.__frame_settings, self.__option_I_Dtime_txt,*self.__option_I_Dtime_values)
        self.__option_I_Dtime.grid(row=4, column=4)
        # build option "I_resolution" at row 4, column 5 in __frame_settings
        self.__option_I_resolution_txt = tk.StringVar()
        self.__option_I_resolution_values = ["768x512", "1536x1024"]
        self.__option_I_resolution_txt.set(self.__option_I_resolution_values[1])
        self.__option_I_resolution = tk.OptionMenu(self.__frame_settings, self.__option_I_resolution_txt,*self.__option_I_resolution_values)
        self.__option_I_resolution.grid(row=4, column=5)
        # build label "blank line" at row 5, column 0-5 in __frame_settings
        tk.Label(self.__frame_settings, text="======================").grid(row=5, column=0, columnspan=5)

        # build button "milling" at row 6, column 0-1 in __frame_settings
        self.__button_mill_here = tk.Button(self.__frame_settings, text="auto milling current position",
                                            command=lambda: self._thread_function(self._mill_here))
        self.__button_mill_here.grid(row=6, column=0, columnspan=2)
        self.__button_group_list.append(self.__button_mill_here)
        # build button "milling all points" at row 6, column 3-4 in __frame_settings
        self.__button_mill_all = tk.Button(self.__frame_settings, text="auto milling all points",
                                           command=lambda: self._thread_function(self._mill_all))
        self.__button_mill_all.grid(row=6, column=3, columnspan=2)
        self.__button_group_list.append(self.__button_mill_all)
        # build button "stop milling" at row 6, column 5 in __frame_settings
        self.__button_stop_mill = tk.Button(self.__frame_settings, text="stop", command=self._stop_milling,
                                            state=tk.DISABLED)
        self.__button_stop_mill.grid(row=6, column=5)
        # build label "settings for milling with ion beam" at row 7, column 1-3 in __frame_settings
        tk.Label(self.__frame_settings, text="===========settings for milling with ion beam========").grid(row=7, column=0, columnspan=5)

        # build label "pattern notes" at row 8, column 0-5 in __frame_settings
        tk.Label(self.__frame_settings, text="name, position, type, high tension, beam current, milling angle, x, y, z ").grid(row=8, column=0, columnspan=5)
        # build frame "pattern" at row 5 in __main_win
        self.__frame_pattern = tk.Frame(self.__main_win)
        self.__frame_pattern.grid(row=5)
        # build listbox "pattern" at row in __frame_pattern
        self.__scrollbar_pattern = tk.Scrollbar(self.__frame_pattern)
        self.__scrollbar_pattern.pack(side=tk.RIGHT, fill=tk.Y)
        self.__listbox_pattern = tk.Listbox(self.__frame_pattern, width=80, height=5, selectmode=tk.SINGLE,yscrollcommand=self.__scrollbar_pattern.set)
        self.__listbox_pattern.pack(side=tk.LEFT, fill=tk.BOTH)
        self.__scrollbar_pattern.config(command=self.__listbox_pattern.yview)
        # build frame "pattern_set" at row 6 in __main_win
        self.__frame_pattern_set = tk.Frame(self.__main_win)
        self.__frame_pattern_set.grid(row=6)
        # build button "add pattern" at row 0, column 0 in __frame_pattern_set
        self.__button_add_pattern = tk.Button(self.__frame_pattern_set, text="add pattern", command=self._add_pattern)
        self.__button_add_pattern.grid(row=0, column=0)
        self.__button_group_list.append(self.__button_add_pattern)
        # build button "update pattern" at row 0, column 1 in __frame_pattern_set
        self.__button_update_pattern = tk.Button(self.__frame_pattern_set, text="change pattern", command=self._change_pattern)
        self.__button_update_pattern.grid(row=0, column=1)
        self.__button_group_list.append(self.__button_update_pattern)
        # build button "delete pattern" at row 0, column 2 in __frame_pattern_set
        self.__button_delete_pattern = tk.Button(self.__frame_pattern_set, text="delete pattern", command=self._delete_pattern)
        self.__button_delete_pattern.grid(row=0, column=2)
        self.__button_group_list.append(self.__button_delete_pattern)
        # build button "add side pattern" at row 0, column 3 in __frame_pattern_set
        self._button_side_choice_B = tk.BooleanVar()
        self._button_side_choice_B.set(True)
        self._button_side_choice_B_bool = True
        tk.Checkbutton(self.__frame_pattern_set, text="include side", variable=self._button_side_choice_B).grid(row=0, column=3)
        # build button "show pattern" at row 0, column 4 in __frame_pattern_set
        self._button_pattern_txt = tk.StringVar()
        self._button_pattern_status = False
        self._button_pattern_txt.set("show pattern")
        self.__button_show_pattern = tk.Button(self.__frame_pattern_set, textvariable=self._button_pattern_txt, command=self._show_pattern)
        self.__button_show_pattern.grid(row=0, column=4)
        self.__button_group_list.append(self.__button_show_pattern)
        # build button "load pattern" at row 0, column 5 in __frame_pattern_set
        self.__button_load_pattern = tk.Button(self.__frame_pattern_set, text="load pattern", command=self._load_pattern)
        self.__button_load_pattern.grid(row=0, column=5)
        self.__button_group_list.append(self.__button_load_pattern)
        # build label "blank line" at row 1, column 0-5 in __frame_pattern_set
        tk.Label(self.__frame_pattern_set, text="========manual thin toolset==============").grid(row=1, column=0, columnspan=5)

        # build frame "thin_milling_frame" at row 7 in __main_win
        self.__frame_thin_milling = tk.Frame(self.__main_win)
        self.__frame_thin_milling.grid(row=7)
        # build button "tilt to angle 1" at row 0, column 0-1 in __frame_thin_milling
        self.__button_thin_tilt_angle_1 = tk.Button(self.__frame_thin_milling, text="tilt to milling angle 1",
                                           command=self._thin_tilt_angle_1)
        self.__button_thin_tilt_angle_1.grid(row=0, column=0, columnspan=2)
        self.__button_group_list.append(self.__button_thin_tilt_angle_1)
        # build entry "angle 1" at row 0, column 2-3 in __frame_thin_milling
        self.__entry_thin_angle_1_flt = tk.StringVar()
        self.__entry_thin_angle_1 = tk.Entry(self.__frame_thin_milling, width=4, textvariable=self.__entry_thin_angle_1_flt,
                                           validate="focusout", validatecommand=(test_mill_angle_TMD, '%P'),
                                           invalidcommand=self._entry_invalid_thin_angle_1)
        self.__entry_thin_angle_1.grid(row=0, column=2, columnspan=2)
        self.__entry_thin_angle_1.insert(0, "10.3")
        # build button "show select pattern" at row 0, column 4-5 in __frame_thin_milling
        self.__button_thin_show_pattern = tk.Button(self.__frame_thin_milling, text="show select pattern",
                                                    command=self._thin_show_select_pattern)
        self.__button_thin_show_pattern.grid(row=0, column=4, columnspan=2)
        self.__button_group_list.append(self.__button_thin_show_pattern)
        # build button "CCS side pattern" at row 1, column 6 in __frame_thin_milling
        self.__button_thin_ccs_side_pattern = tk.Button(self.__frame_thin_milling, text="ccs side pattern",
                                                        command=self._thin_show_ccs_side_pattern)
        self.__button_thin_ccs_side_pattern.grid(row=0, column=6)
        self.__button_group_list.append(self.__button_thin_ccs_side_pattern)
        # build button "tilt to angle 2" at row 1, column 0-1 in __frame_thin_milling
        self.__button_thin_tilt_angle_2 = tk.Button(self.__frame_thin_milling, text="tilt to milling angle 2",
                                                    command=self._thin_tilt_angle_2)
        self.__button_thin_tilt_angle_2.grid(row=1, column=0, columnspan=2)
        self.__button_group_list.append(self.__button_thin_tilt_angle_2)
        # build entry "angle 2" at row 1, column 2-3 in __frame_thin_milling
        self.__entry_thin_angle_2_flt = tk.StringVar()
        self.__entry_thin_angle_2 = tk.Entry(self.__frame_thin_milling, width=4,
                                             textvariable=self.__entry_thin_angle_2_flt,
                                             validate="focusout", validatecommand=(test_mill_angle_TMD, '%P'),
                                             invalidcommand=self._entry_invalid_thin_angle_2)
        self.__entry_thin_angle_2.grid(row=1, column=2, columnspan=2)
        self.__entry_thin_angle_2.insert(0, "9.7")
        # build button "clear select pattern" at row 1, column 4-5 in __frame_thin_milling
        self.__button_thin_clear_pattern = tk.Button(self.__frame_thin_milling, text="clear pattern",
                                                    command=self._thin_clear_pattern)
        self.__button_thin_clear_pattern.grid(row=1, column=4, columnspan=2)
        self.__button_group_list.append(self.__button_thin_clear_pattern)
        # build button "cross pattern" at row 1, column 6 in __frame_thin_milling
        self.__button_thin_cross_pattern = tk.Button(self.__frame_thin_milling, text="+ pattern",
                                                     command=self._set_cross_pattern)
        self.__button_thin_cross_pattern.grid(row=1, column=6)
        self.__button_group_list.append(self.__button_thin_cross_pattern)
        # build button "take E image" at row 2-3, column 0-1 in __frame_thin_milling
        self.__button_thin_E_image = tk.Button(self.__frame_thin_milling, text="take E image",
                                               command=self._thin_take_E_image)
        self.__button_thin_E_image.grid(row=2, column=0, columnspan=2, rowspan=2)
        self.__button_group_list.append(self.__button_thin_E_image)
        # build button "save E image" at row 2, column 2 in __frame_thin_milling
        self.__button_thin_save_E_image = tk.Button(self.__frame_thin_milling, text="save E image",
                                                    command=self._thin_save_E_image)
        self.__button_thin_save_E_image.grid(row=2, column=2)
        self.__button_group_list.append(self.__button_thin_save_E_image)
        # build button "save I image" at row 2, column 4 in __frame_thin_milling
        self.__button_thin_save_I_image = tk.Button(self.__frame_thin_milling, text="save I image",
                                                    command=self._thin_save_I_image)
        self.__button_thin_save_I_image.grid(row=2, column=4)
        self.__button_group_list.append(self.__button_thin_save_I_image)
        # build button "take I image" at row 2-3, column 5-6 in __frame_thin_milling
        self.__button_thin_I_image = tk.Button(self.__frame_thin_milling, text="take I image",
                                                     command=self._thin_take_I_image)
        self.__button_thin_I_image.grid(row=2, column=5,columnspan=2,rowspan=2)
        self.__button_group_list.append(self.__button_thin_I_image)
        # build button "pause milling" at row 3, column 2 in __frame_thin_milling
        self.__button_thin_pause_milling_txt = tk.StringVar()
        self.__button_thin_pause_milling_txt.set("pause")
        self.__button_thin_pause_milling = tk.Button(self.__frame_thin_milling, textvariable=self.__button_thin_pause_milling_txt,
                                                     command=self._thin_pause_milling, state=tk.DISABLED)
        self.__button_thin_pause_milling.grid(row=3, column=2)
        # build button "stop milling" at row 3, column 4 in __frame_thin_milling
        self.__button_thin_stop_milling = tk.Button(self.__frame_thin_milling, text="stop",
                                                     command=self._thin_stop_milling, state=tk.DISABLED)
        self.__button_thin_stop_milling.grid(row=3, column=4)
        # build button "start milling" at row 4, column 3 in __frame_thin_milling
        self.__button_thin_start_milling = tk.Button(self.__frame_thin_milling, text="start milling",
                                                    command=lambda :self._thread_function(self._thin_start_milling))
        self.__button_thin_start_milling.grid(row=4, column=3)
        self.__button_group_list.append(self.__button_thin_start_milling)
        # build button "scan rotation 1" at row 5, column 0-1 in __frame_thin_milling
        self.__button_thin_scan_rotation_1 = tk.Button(self.__frame_thin_milling, text="scan rotation 1",
                                                    command=self._i_scan_rotation_1)
        self.__button_thin_scan_rotation_1.grid(row=5, column=0, columnspan=2)
        self.__button_group_list.append(self.__button_thin_scan_rotation_1)
        # build entry "scan angle 1" at row 5, column 2-3 in __frame_thin_milling
        self.__entry_thin_scan_angle_1_flt = tk.StringVar()
        self.__entry_thin_scan_angle_1 = tk.Entry(self.__frame_thin_milling, width=6,
                                             textvariable=self.__entry_thin_scan_angle_1_flt,
                                             validate="focusout", validatecommand=(test_float_TMD, '%P'),
                                             invalidcommand=self._entry_invalid_thin_scan_angle_1)
        self.__entry_thin_scan_angle_1.grid(row=5, column=2,columnspan=2)
        self.__entry_thin_scan_angle_1.insert(0, "180.2")
        # build button "scan rotation 2" at row 6, column 0-1 in __frame_thin_milling
        self.__button_thin_scan_rotation_2 = tk.Button(self.__frame_thin_milling, text="scan rotation 2",
                                                       command=self._i_scan_rotation_2)
        self.__button_thin_scan_rotation_2.grid(row=6, column=0, columnspan=2)
        self.__button_group_list.append(self.__button_thin_scan_rotation_2)
        # build entry "scan angle 2" at row 6, column 2-3 in __frame_thin_milling
        self.__entry_thin_scan_angle_2_flt = tk.StringVar()
        self.__entry_thin_scan_angle_2 = tk.Entry(self.__frame_thin_milling, width=6,
                                                  textvariable=self.__entry_thin_scan_angle_2_flt,
                                                  validate="focusout", validatecommand=(test_float_TMD, '%P'),
                                                  invalidcommand=self._entry_invalid_thin_scan_angle_2)
        self.__entry_thin_scan_angle_2.grid(row=6, column=2,columnspan=2)
        self.__entry_thin_scan_angle_2.insert(0, "179.8")
        # build button "scan rotation 180" at row 6, column 4-5 in __frame_thin_milling
        self.__button_thin_scan_rotation_180 = tk.Button(self.__frame_thin_milling, text="scan rotation 180",
                                                       command=self._i_scan_rotation_180)
        self.__button_thin_scan_rotation_180.grid(row=6, column=4, columnspan=2)
        self.__button_group_list.append(self.__button_thin_scan_rotation_180)



        self._pattern_handle_dict = {"add":0,"update":1}
        self.__option_top_win_I_HT_values_dict = {"8.0 kV": 0, "16.0 kV": 1, "30.0 kV": 0}
        self.__option_top_win_I_BC_values_dict = {"10 pA": 0, "30 pA": 1, "50 pA": 2, "0.10 nA": 3, "0.3 nA": 4,
                                                  "0.5 nA": 5, "1.0 nA": 6}

    def _entry_invalid_thin_angle_1(self):
        self.__entry_thin_angle_1.delete(0, tk.END)
        self.__entry_thin_angle_1.insert(0, "10.3")

    def _entry_invalid_thin_angle_2(self):
        self.__entry_thin_angle_2.delete(0, tk.END)
        self.__entry_thin_angle_2.insert(0, "9.7")

    def _entry_invalid_thin_scan_angle_1(self):
        self.__entry_thin_scan_angle_1.delete(0, tk.END)
        self.__entry_thin_scan_angle_1.insert(0, "180.2")

    def _entry_invalid_thin_scan_angle_2(self):
        self.__entry_thin_scan_angle_2.delete(0, tk.END)
        self.__entry_thin_scan_angle_2.insert(0, "179.8")

    def _open_folder_dialg(self):
        self.__default_path = tkf.askdirectory()
        self.__label_open_folder_txt.set(self.__default_path)
        if not self._load_e_map():
            self._load_points()
        #self._load_pattern()

    def _load_points(self):
        try:
            os.path.exists(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        previous_points = self._read_point_json()
        self._load_all_point_to_listbox(previous_points)

    def _win_warning(self):
        self.__top_warning = tk.Toplevel()
        self.__top_warning.title("confirm")
        tk.Label(self.__top_warning,text="check eucentric position and focus").grid(row=0,column=0,columnspan=2)
        tk.Label(self.__top_warning, text="if changed, please reset reference").grid(row=1,column=0,columnspan=2)
        tk.Button(self.__top_warning, text="OK", command=self._destroy_win).grid(row=2, column=1)

    def _take_e_map(self):
        try:
            self.__top_map.destroy()
        except:
            print("no win open")
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.electron_beam.turn_on()
        ht, bc, mag, resolution_str, Dtime = self._image_prep("electron")
        mag_dict = self.__option_E_mag_dict
        mag = mag_dict["42x"]
        resolution_str = "768x512"
        img_condition = [ht, bc, mag, resolution_str, Dtime]
        map_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map"))
        save_status = [True,map_path]
        self._E_imageing(save_status,img_condition)

        stage_x = self.microscope.specimen.stage.current_position.x
        stage_y = self.microscope.specimen.stage.current_position.y
        stage_z = self.microscope.specimen.stage.current_position.z
        stage_t = self.microscope.specimen.stage.current_position.t
        current_status = {}
        current_status.update(center_stage_x=stage_x)
        current_status.update(center_stage_y=stage_y)
        current_status.update(center_stage_z=stage_z)
        current_status.update(center_stage_t=stage_t)
        current_status.update(center_field_width=mag)
        current_status.update(center_resolution_str=resolution_str)
        json_path = os.path.abspath(os.path.join(self.__default_path, "E_map_json"))
        with open(json_path, "w+") as default_json:
            json.dump(current_status, default_json)
        self.microscope.disconnect()

        board_size = resolution_str.split('x')
        map_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.tiff"))
        self._tiff2gif(map_path)
        map_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.gif"))
        self._show_win_map(map_path, board_size)

    def _load_e_map(self):
        try:
            self.__top_map.destroy()
        except:
            print("no win open")
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return False
        resolution_str = "768x512"
        board_size = resolution_str.split('x')

        gif_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.gif"))
        if os.path.exists(gif_path):
            self._show_win_map(gif_path, board_size)
        else:
            map_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.tiff"))
            if os.path.exists(map_path):
                self._tiff2gif(map_path)
                gif_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.gif"))
                self._show_win_map(gif_path, board_size)
                return True
            else:
                print("no map taken")
                return False

    def _tiff2gif(self,tiff_path):
        img_tiff = Image.open(tiff_path)
        gif_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.gif"))
        img_tiff.save(gif_path, "gif")

    def _show_win_map(self,gif_path,board_size):
        if os.path.exists(gif_path):
            self.__top_map = tk.Toplevel()
            self.__top_map.title("electron beam map")
            self.__top_map.geometry(newGeometry='{}x{}+{}+{}'.format(board_size[0],board_size[1],600,100))
            self.__canvas_map = tk.Canvas(self.__top_map, width=int(board_size[0]), height=int(board_size[1]))
            print(int(board_size[0]), int(board_size[1]))
            #global map_gif to show map in canvas
            global map_gif
            map_gif = tk.PhotoImage(file=gif_path)
            self.__canv_e_map = self.__canvas_map.create_image(int(board_size[0])/2, int(board_size[1])/2,image=map_gif)
            self._show_all_points_on_map()
            self.__canvas_map.pack()
        else:
            print("{} not exists.going to take one".format(gif_path))

    def _show_all_points_on_map(self):
        #self._delete_all_points_from_map()
        self._load_points()
        center_status, center_parameter = self._add_center_point_to_map()
        if center_status:
            self._add_grid_limit_ring_to_map(center_parameter)
            previous_points = self._read_point_json()
            if len(previous_points) > 0:
                for each_point in previous_points.keys():
                    self._add_one_point_to_map(center_parameter, previous_points, each_point)

    def _show_one_point_to_map(self,previous_points,each_point):
        try:
            self.__canvas_map.delete(self._test_create)
        except:
            return
        self._test_create = self.__canvas_map.create_line(0, 0, 1, 1)
        center_status, center_parameter = self._add_center_point_to_map()
        if center_status:
            self._add_one_point_to_map(center_parameter, previous_points, each_point)

    def _add_center_point_to_map(self):
        try:
            self.__canvas_map.delete(self.__canv_center)
        except:
            pass
        center_parameter = []
        ref_status, map_center = self._read_E_map_json()
        if ref_status:
            center_x = map_center["center_stage_x"]
            center_y = map_center["center_stage_y"]
            center_z = map_center["center_stage_z"]
            center_t = map_center["center_stage_t"]
            field_width = map_center["center_field_width"]
            resolution_str = map_center["center_resolution_str"]
            resolution_split = resolution_str.split("x")
            canv_center_x = round(int(resolution_split[0]) / 2)
            canv_center_y = round(int(resolution_split[1]) / 2)
            self.__canv_center = self.__canvas_map.create_text(canv_center_x, canv_center_y, text="[   ]", fill='#00dcff',font=('Arial',20,'bold'))
            canv_pixel_size = field_width / int(resolution_split[0])
            center_parameter = [center_x,center_y,canv_center_x,canv_center_y,canv_pixel_size,center_t]
            return True,center_parameter
        else:
            return False,center_parameter

    def _coordiate_titan3_to_aquilos(self, titan_x, titan_y, grid_position):
        titan_ori_x = -95 / 1000
        titan_ori_y = -44.2 / 1000
        rotation_angle_ori = -5
        scale_factor = 1 / 1.4
        if grid_position == "2":
            grid_ori_x = 3.53
            grid_ori_y = 3.27
        elif grid_position == "1":
            grid_ori_x = 3.53 - 6.03
            grid_ori_y = 3.27 + 0.2

        rotation_angle_flt = math.pi * float(rotation_angle_ori) / 180

        aquilos_x = (titan_x / 1000 - titan_ori_x) * math.cos(rotation_angle_flt) - (
                                                                                    titan_y / 1000 - titan_ori_y) * math.sin(
            rotation_angle_flt)
        aquilos_y = (titan_x / 1000 - titan_ori_x) * math.sin(rotation_angle_flt) + (
                                                                                    titan_y / 1000 - titan_ori_y) * math.cos(
            rotation_angle_flt)
        aquilos_x = grid_ori_x - aquilos_x
        aquilos_y = grid_ori_y - aquilos_y * scale_factor
        return aquilos_x * 1e-3, aquilos_y * 1e-3

    def _coordinate_aquilos_to_map(self, center_parameter, aquilos_x, aquilos_y):
        center_x, center_y, canv_center_x, canv_center_y, canv_pixel_size, center_t = center_parameter

        rotation_angle_str = 0
        rotation_angle_flt = -1 * math.pi * float(rotation_angle_str) / 180

        diff_x = (center_x - aquilos_x) / canv_pixel_size
        diff_y = (aquilos_y - center_y) / canv_pixel_size

        diff_y = round(diff_y * (1 + math.sin(center_t)))

        diff_x_pixel = round(diff_x * math.cos(rotation_angle_flt) - diff_y * math.sin(rotation_angle_flt))
        diff_y_pixel = round(diff_x * math.sin(rotation_angle_flt) + diff_y * math.cos(rotation_angle_flt))
        diff_x_pixel = diff_x_pixel + canv_center_x
        diff_y_pixel = diff_y_pixel + canv_center_y

        return diff_x_pixel, diff_y_pixel

    def _update_all_points_to_map(self):
        try:
            self.__top_map.destroy()
        except:
            print("no win open")
        ref_status, map_center = self._read_E_map_json()
        if ref_status:
            resolution_str = map_center["center_resolution_str"]
            board_size = resolution_str.split('x')
            map_path = os.path.abspath(os.path.join(self.__default_path, "E_whole_map.gif"))
            self._show_win_map(map_path, board_size)

    def _add_one_point_to_map(self,center_parameter,previous_points,each_point):
        center_x, center_y, canv_center_x, canv_center_y, canv_pixel_size, center_t = center_parameter
        stage_x = previous_points[each_point]["current_stage_x"]
        stage_y = previous_points[each_point]["current_stage_y"]
        stage_z = previous_points[each_point]["current_stage_z"]
        stage_t = previous_points[each_point]["current_stage_t"]

        diff_x = round((center_x - stage_x) / canv_pixel_size)
        diff_y = round((stage_y - center_y) / canv_pixel_size)
        if abs(diff_x) > canv_center_x or abs(diff_y) > canv_center_y:
            print("{} out of map area: {} {}".format(each_point, diff_x, diff_y))
        else:
            dot_x, dot_y = self._coordinate_aquilos_to_map(center_parameter, stage_x, stage_y)
            num_slipt = str(each_point).split("_")
            num_for_show = int(num_slipt[1])
            print(num_for_show,dot_x, dot_y)
            self.__canvas_map.create_text(dot_x, dot_y, text="{}".format(num_for_show), fill='#ff0000',font=('Arial',20,'bold'))

    def _add_grid_limit_ring_to_map(self, center_parameter):
        center_x, center_y, canv_center_x, canv_center_y, canv_pixel_size, center_t = center_parameter
        if center_x < 0:
            grid_position = "1"
        else:
            grid_position = "2"
        distance = 900
        angle_step = 10
        for i in range(36):
            current_angle = math.pi * angle_step * i / 180
            titan_x = distance * math.cos(current_angle)
            titan_y = distance * math.sin(current_angle)
            aquilos_x, aquilos_y = self._coordiate_titan3_to_aquilos(titan_x, titan_y, grid_position)
            dot_x, dot_y = self._coordinate_aquilos_to_map(center_parameter, aquilos_x, aquilos_y)
            self.__canvas_map.create_text(dot_x, dot_y, text="+", fill='#d24302', font=('Arial', 15, 'bold'))
        return titan_x, titan_y, aquilos_x, aquilos_y, dot_x, dot_y

    def _read_E_map_json(self):
        default_status = {}
        json_path = os.path.abspath(os.path.join(self.__default_path, "E_map_json"))
        if os.path.exists(json_path):
            with open(json_path, "r") as default_json:
                default_status = json.load(default_json)
            return True, default_status
        else:
            print("please take map image.")
            return False, default_status

    def _destroy_win(self):
        self.__top_warning.destroy()

    def _set_ref_point(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.ion_beam.beam_shift.value = Point(x=0.0, y=0.0)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=0.0, y=0.0)
        stage_link = self.microscope.specimen.stage.is_linked
        if not stage_link:
            print("please link Z to work distance!")
            self.microscope.disconnect()
            return

        default_E_ht = self.microscope.beams.electron_beam.high_voltage.value
        default_I_ht = self.microscope.beams.ion_beam.high_voltage.value
        default_i_wd_value,i_beam_shift_x,i_beam_shift_y = self._read_beam_values("I")
        default_e_wd_value, e_beam_shift_x, e_beam_shift_y = self._read_beam_values("E")
        stage_x = self.microscope.specimen.stage.current_position.x
        stage_y = self.microscope.specimen.stage.current_position.y
        stage_z = self.microscope.specimen.stage.current_position.z
        stage_t = self.microscope.specimen.stage.current_position.t

        current_status = {}
        current_status.update(default_E_ht=default_E_ht)
        current_status.update(default_I_ht=default_I_ht)
        current_status.update(default_I_wd_value=default_i_wd_value)
        current_status.update(default_E_wd_value=default_e_wd_value)
        current_status.update(default_I_beam_shift_x=i_beam_shift_x)
        current_status.update(default_I_beam_shift_y=i_beam_shift_y)
        current_status.update(default_E_beam_shift_x=e_beam_shift_x)
        current_status.update(default_E_beam_shift_y=e_beam_shift_y)
        current_status.update(default_stage_x=stage_x)
        current_status.update(default_stage_y=stage_y)
        current_status.update(default_stage_z=stage_z)
        current_status.update(default_stage_t=stage_t)

        json_path = os.path.abspath(os.path.join(self.__default_path, "default_json"))
        with open(json_path, "w+") as default_json:
            json.dump(current_status, default_json)

        default_E_ht = default_E_ht / 1000
        default_I_ht = default_I_ht / 1000
        self.__option_E_HT_txt.set('{:.1f} kV'.format(default_E_ht))
        self.__option_I_HT_txt.set('{:.1f} kV'.format(default_I_ht))
        self.microscope.disconnect()
        self._win_warning()

    def _get_next_save_img_num(self,each_point,img_type):
        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_{}_{:02d}.tiff'.format(each_point,img_type, i)))
            num = i
            if os.path.exists(template_path):
                break
        return num

    def _get_template_img_num(self,each_point,img_type):
        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_{}_{:02d}.tiff'.format(each_point,img_type, i)))
            num = i - 1
            if os.path.exists(template_path):
                break
        return num

    def _read_ref_json(self):
        default_status = {}
        json_path = os.path.abspath(os.path.join(self.__default_path, "default_json"))
        if os.path.exists(json_path):
            with open(json_path, "r") as default_json:
                default_status = json.load(default_json)
            return True, default_status
        else:
            print("please set reference point.")
            return False, default_status

    def _read_beam_values(self,beam_type):
        if beam_type == "E":
            wd_value = self.microscope.beams.electron_beam.working_distance.value
            beam_shift_x = self.microscope.beams.electron_beam.beam_shift.value.x
            beam_shift_y = self.microscope.beams.electron_beam.beam_shift.value.y
        elif beam_type == "I":
            wd_value = self.microscope.beams.ion_beam.working_distance.value
            beam_shift_x = self.microscope.beams.ion_beam.beam_shift.value.x
            beam_shift_y = self.microscope.beams.ion_beam.beam_shift.value.y
        return wd_value,beam_shift_x,beam_shift_y

    def _clear_all_points(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        previous_points = self._read_point_json()
        self._delete_all_points_from_listbox(previous_points)
        previous_points = {}
        self._write_point_json(previous_points)

    def _delete_all_points_from_listbox(self,current_points):
        self.__listbox_points.delete(0, tk.END)
        if len(current_points) > 0:
            for each_point in current_points.keys():
                template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_I_01.tiff")))
                os.remove(template_path)
                template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_E_01.tiff")))
                os.remove(template_path)
        else:
            print("no point in list")
            return

    def _read_point_json(self):
        previous_points = {}
        json_path = os.path.abspath(os.path.join(self.__default_path, "auto_slice_point_json"))
        if not os.path.exists(json_path):
            with open(json_path, "w+") as default_json:
                json.dump(previous_points, default_json)
        with open(json_path, "r") as default_json:
            previous_points = json.load(default_json)
        return previous_points

    def _write_point_json(self,previous_points):
        json_path = os.path.abspath(os.path.join(self.__default_path, "auto_slice_point_json"))
        with open(json_path, "w+") as default_json:
            json.dump(previous_points, default_json)

    def _add_point(self):
        self._load_points()
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return

        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.beam_shift.value = Point(x=0.0, y=0.0)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=0.0, y=0.0)
        stage_link = self.microscope.specimen.stage.is_linked
        if not stage_link:
            print("please link Z to work distance!")
            self._link_Z_warning()
            self.microscope.disconnect()
            for each_button in self.__button_group_list:
                each_button.config(state=tk.ACTIVE)
            return
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        previous_points = self._read_point_json()
        for i in range(1,100,1):
            point_number = len(previous_points) + i
            current_num = format('%03d' % point_number)
            each_point = str("point_" + current_num)
            try:
                previous_points[each_point]
            except:
                break
        template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_I_01")))
        save_status = [True, template_path]
        imaging_condition = []
        self._I_imageing(save_status,imaging_condition)

        if self._I_adjust():
            template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_I_01.tiff")))
            if self._template_match(template_path,imaging_condition):
                e_image_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_E_01")))
                save_status = [True, e_image_path]
                self._E_imageing(save_status,imaging_condition)
                current_points = self._record_current_point(previous_points,each_point)

                self._add_one_point_to_listbox(current_points,each_point)
                self._update_all_points_to_map()
                self._current_point = each_point
        self.microscope.disconnect()
        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)

    def _E_adjust(self,previous_points,each_point):
        previous_stage_y = previous_points[each_point]["current_stage_y"]

        ref_status, default_status = self._read_ref_json()
        if ref_status:
            default_milling_angle = (default_status["default_stage_t"] / math.pi) * 180 - 7
            current_stage_t = self.microscope.specimen.stage.current_position.t
            current_mil_angle = (current_stage_t / math.pi) * 180 - 7
            if current_mil_angle > default_milling_angle + 0.3 or current_mil_angle < default_milling_angle - 0.3:
                print("please set reference at current milling angle")
                return False
            current_E_ht = self.microscope.beams.electron_beam.high_voltage.value
            #if not current_E_ht == default_status["default_E_ht"]:
            #    print("please set reference at current electron beam high tension")
            #    return False
            #current_I_ht = self.microscope.beams.ion_beam.high_voltage.value
            #if not current_I_ht == default_status["default_I_ht"]:
            #    print("please set reference at current ion beam high tension")
            #    return False

            I_beam_shift_x = default_status["default_I_beam_shift_x"]
            I_beam_shift_y = default_status["default_I_beam_shift_y"]
            E_beam_shift_x = default_status["default_E_beam_shift_x"]
            E_beam_shift_y = default_status["default_E_beam_shift_y"]

            self.microscope.beams.ion_beam.beam_shift.value = Point(x=I_beam_shift_x, y=I_beam_shift_y)
            self.microscope.beams.electron_beam.beam_shift.value = Point(x=E_beam_shift_x, y=E_beam_shift_y)

            current_stage_y = self.microscope.specimen.stage.current_position.y
            current_stage_z = self.microscope.specimen.stage.current_position.z
            current_mil_angle = current_stage_t + (24 / 180) * math.pi
            current_mil_angle_y = current_stage_t + (51 / 180) * math.pi

            diff_y = current_stage_y - previous_stage_y
            diff_I_wd_value = diff_y / math.cos(current_mil_angle)
            new_stage_z = current_stage_z + diff_I_wd_value * math.sin(current_mil_angle)
            new_stage_y = current_stage_y - diff_I_wd_value * math.cos(current_mil_angle_y)

            new_p = StagePosition(y=new_stage_y,z=new_stage_z, coordinate_system="Specimen")
            self.microscope.specimen.stage.absolute_move(new_p)

            self.microscope.beams.electron_beam.working_distance.value = default_status["default_E_wd_value"]
            self.microscope.beams.ion_beam.working_distance.value = default_status["default_I_wd_value"]
            return True
        else:
            return False

    def _I_adjust(self):
        ref_status, default_status = self._read_ref_json()
        if ref_status:
            new_p = StagePosition(t=default_status["default_stage_t"])
            self.microscope.specimen.stage.absolute_move(new_p)
            self.microscope.beams.electron_beam.high_voltage.value = default_status["default_E_ht"]
            self.microscope.beams.ion_beam.high_voltage.value = default_status["default_I_ht"]

            #default_milling_angle = ( default_status["default_stage_t"] / math.pi ) * 180 - 7
            #current_stage_t = self.microscope.specimen.stage.current_position.t
            #current_mil_angle = ( current_stage_t / math.pi ) * 180 - 7
            #if current_mil_angle > default_milling_angle + 0.3 or current_mil_angle < default_milling_angle - 0.3:
            #    print("please set reference at current milling angle")
            #    return False
            #current_E_ht = self.microscope.beams.electron_beam.high_voltage.value
            #if not current_E_ht == default_status["default_E_ht"]:
            #    print("please set reference at current electron beam high tension")
            #    return False
            #current_I_ht = self.microscope.beams.ion_beam.high_voltage.value
            #if not current_I_ht == default_status["default_I_ht"]:
            #    print("please set reference at current ion beam high tension")
            #    return False

            I_beam_shift_x = default_status["default_I_beam_shift_x"]
            I_beam_shift_y = default_status["default_I_beam_shift_y"]
            E_beam_shift_x = default_status["default_E_beam_shift_x"]
            E_beam_shift_y = default_status["default_E_beam_shift_y"]
            current_stage_t = default_status["default_stage_t"]

            self.microscope.beams.ion_beam.beam_shift.value = Point(x=I_beam_shift_x, y=I_beam_shift_y)
            self.microscope.beams.electron_beam.beam_shift.value = Point(x=E_beam_shift_x, y=E_beam_shift_y)

            current_I_wd_value = self.microscope.beams.ion_beam.working_distance.value
            diff_I_wd_value = 1 * (default_status["default_I_wd_value"] - current_I_wd_value)

            current_stage_y = self.microscope.specimen.stage.current_position.y
            current_stage_z = self.microscope.specimen.stage.current_position.z
            current_mil_angle = current_stage_t + (39 / 180) * math.pi

            new_stage_z = current_stage_z + diff_I_wd_value * math.sin(current_mil_angle)
            new_stage_y = current_stage_y + diff_I_wd_value * math.cos(current_mil_angle)
            new_p = StagePosition(y=new_stage_y, z=new_stage_z,coordinate_system="Specimen")
            self.microscope.specimen.stage.absolute_move(new_p)

            self.microscope.beams.ion_beam.working_distance.value = default_status["default_I_wd_value"]
            self.microscope.beams.electron_beam.working_distance.value = default_status["default_E_wd_value"]
            return True
        else:
            return False

    def _template_match(self,template_path,imaging_condition):
        template = AdornedImage.load(template_path)
        for match_index in range(1):
            save_status = [False, self.__default_path]
            image_taken = self._I_imageing(save_status,imaging_condition)

            match_result = self.microscope.imaging.match_template(image_taken, template)
            field_width = self.microscope.beams.ion_beam.horizontal_field_width.value
            current_stage_x = self.microscope.specimen.stage.current_position.x
            current_stage_y = self.microscope.specimen.stage.current_position.y
            resolution_str = self.__option_I_resolution_txt.get()
            resolution_split = resolution_str.split("x")
            current_stage_x = current_stage_x - (match_result.center.x - (float(resolution_split[0]) / 2)) * field_width / float(resolution_split[0])
            current_stage_y = current_stage_y + (match_result.center.y - (float(resolution_split[1]) / 2)) * field_width / float(resolution_split[0])
            new_p = StagePosition(x=current_stage_x, y=current_stage_y,coordinate_system="Specimen")
            self.microscope.specimen.stage.absolute_move(new_p)
        save_status = [False, self.__default_path]
        self._I_imageing(save_status,imaging_condition)

        if match_result.score > 0.5:
            return True
        else:
            print("template match score {} too low. please manually adjust the position again".format(match_result.score))
            return False

    def _template_match_beam_shift(self,template_path,imaging_condition):
        template = AdornedImage.load(template_path)
        for match_index in range(1):
            save_status = [False, self.__default_path]
            image_taken = self._I_imageing_side(save_status, imaging_condition)

            match_result = self.microscope.imaging.match_template(image_taken, template)
            field_width = self.microscope.beams.ion_beam.horizontal_field_width.value
            I_beam_shift_x = self.microscope.beams.ion_beam.beam_shift.value.x
            I_beam_shift_y = self.microscope.beams.ion_beam.beam_shift.value.y
            resolution_str = self.__option_I_resolution_txt.get()
            resolution_split = resolution_str.split("x")
            I_beam_shift_x = I_beam_shift_x - (match_result.center.x - (
            0.4 * float(resolution_split[0]) / 2)) * field_width / float(resolution_split[0])
            I_beam_shift_y = I_beam_shift_y + (match_result.center.y - (
            0.6 * float(resolution_split[1]) / 2)) * field_width / float(resolution_split[0])
            self.microscope.beams.ion_beam.beam_shift.value = Point(x=I_beam_shift_x, y=I_beam_shift_y)
        save_status = [False, self.__default_path]
        self._I_imageing(save_status, imaging_condition)

        if match_result.score > 0.2:
            return True
        else:
            print("template match (beam shift) score {} too low. Not process milling".format(match_result.score))
            return False

    def _record_current_point(self,previous_points,each_point):
        current_I_wd_value, I_beam_shift_x, I_beam_shift_y = self._read_beam_values("I")
        current_E_wd_value, E_beam_shift_x, E_beam_shift_y = self._read_beam_values("E")
        current_stage_x = self.microscope.specimen.stage.current_position.x
        current_stage_y = self.microscope.specimen.stage.current_position.y
        current_stage_z = self.microscope.specimen.stage.current_position.z
        current_stage_t = self.microscope.specimen.stage.current_position.t
        previous_patterns = self._read_pattern_json()

        one_point_status = {}
        one_point_status.update(current_I_wd_value=current_I_wd_value)
        one_point_status.update(current_E_wd_value=current_E_wd_value)
        one_point_status.update(current_stage_x=current_stage_x)
        one_point_status.update(current_stage_y=current_stage_y)
        one_point_status.update(current_stage_z=current_stage_z)
        one_point_status.update(current_stage_t=current_stage_t)
        one_point_status.update(I_beam_shift_x=I_beam_shift_x)
        one_point_status.update(I_beam_shift_y=I_beam_shift_y)
        one_point_status.update(E_beam_shift_x=E_beam_shift_x)
        one_point_status.update(E_beam_shift_y=E_beam_shift_y)
        one_point_status.update(thin_status=False)
        one_point_status.update(side_status=False)
        one_point_status.update(pattern_setting=previous_patterns)
        one_point_status.update(side_status_set=self._button_side_choice_B.get())

        #imaging conditions
        imaging_condition = []
        imaging_condition = self._image_prep("ion")
        one_point_status.update(I_imaging_condition=imaging_condition)
        imaging_condition = self._image_prep("electron")
        one_point_status.update(E_imaging_condition=imaging_condition)

        point_status = {str(each_point): one_point_status}
        previous_points.update(point_status)
        print("update to {}".format(each_point))
        self._write_point_json(previous_points)
        return previous_points

    def _add_one_point_to_listbox(self,current_points,each_point):
        each_point_str = self._points_show_in_listbox(current_points,each_point)
        self.__listbox_points.insert(tk.END, each_point_str)
        self.__listbox_points.activate(tk.END)

    def _points_show_in_listbox(self,current_points,each_point):
        name = each_point
        stage_x = current_points[name]["current_stage_x"] * 1e3
        stage_y = current_points[name]["current_stage_y"] * 1e3
        stage_z = current_points[name]["current_stage_z"] * 1e3
        milling_angle = (current_points[name]["current_stage_t"] / math.pi) * 180 - 7
        if current_points[name]["thin_status"]:
            thin_status_str = 'Y'
        else:
            thin_status_str = 'N'
        each_point_str = '{}    \t{:.2f}    \t{:.2f}    \t{:.2f}    \t{:.1f}    \t{}'.format(name, stage_x, stage_y, stage_z, milling_angle,thin_status_str)
        return each_point_str

    def _load_all_point_to_listbox(self,current_points):
        self.__listbox_points.delete(0, tk.END)
        if len(current_points) > 0:
            for each_point in current_points.keys():
                each_point_str = self._points_show_in_listbox(current_points, each_point)
                self.__listbox_points.insert(tk.END,each_point_str)
            self._current_point = each_point
            self.__listbox_points.activate(tk.END)
        else:
            return

    def _update_one_point_to_listbox(self, current_points, each_point):
        each_point_str = self._points_show_in_listbox(current_points, each_point)
        listbox_active_index = self.__listbox_points.index(tk.ACTIVE)
        self.__listbox_points.insert(listbox_active_index, each_point_str)
        self.__listbox_points.delete(tk.ACTIVE)
        #self.__listbox_points.activate(listbox_active_index)
        return listbox_active_index

    def _E_correct(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        try:
            print(self._current_point)
        except AttributeError:
            print("please add point first!")
            return

        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.beam_shift.value = Point(x=0.0, y=0.0)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=0.0, y=0.0)
        stage_link = self.microscope.specimen.stage.is_linked
        if not stage_link:
            print("please link Z to work distance!")
            self._link_Z_warning()
            self.microscope.disconnect()
            for each_button in self.__button_group_list:
                each_button.config(state=tk.ACTIVE)
            return
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        previous_points = self._read_point_json()

        #listbox_active_tuple = self.__listbox_points.get(tk.ACTIVE)
        #listbox_active_options = listbox_active_tuple.split('    \t')
        #each_point = listbox_active_options[0]
        each_point = self._current_point
        num = self._get_template_img_num(each_point,"I")
        if self._E_adjust(previous_points,each_point):
            ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["I_imaging_condition"]
            ht = self.microscope.beams.ion_beam.high_voltage.value
            bc = self.microscope.beams.ion_beam.beam_current.value
            I_imaging_condition = [ht, bc, mag, resolution_str, Dtime]
            template_path = os.path.abspath(os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, num)))
            if not os.path.exists(template_path):
                self.microscope.disconnect()
                print("please add point or goto point.")
                return
            if self._template_match(template_path, I_imaging_condition):
                num = self._get_next_save_img_num(each_point,"E")
                e_image_path = os.path.abspath(os.path.join(self.__default_path, '{}_E_{:02d}.tiff'.format(each_point, num)))
                save_status = [True, e_image_path]
                ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["E_imaging_condition"]
                ht = self.microscope.beams.electron_beam.high_voltage.value
                bc = self.microscope.beams.electron_beam.beam_current.value
                E_imaging_condition = [ht, bc, mag, resolution_str, Dtime]
                self._E_imageing(save_status, E_imaging_condition)
                current_points = self._record_current_point(previous_points, each_point)
                listbox_active_index = self._update_one_point_to_listbox(current_points, each_point)
                self._update_all_points_to_map()
                self.__listbox_points.activate(listbox_active_index)
                self._current_point = each_point

        self.microscope.disconnect()
        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)

    def _update_point(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_points.get(tk.ACTIVE) == "":
            print("no selection activated")
            return

        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.beam_shift.value = Point(x=0.0, y=0.0)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=0.0, y=0.0)
        stage_link = self.microscope.specimen.stage.is_linked
        if not stage_link:
            print("please link Z to work distance!")
            self._link_Z_warning()
            self.microscope.disconnect()
            for each_button in self.__button_group_list:
                each_button.config(state=tk.ACTIVE)
            return
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        previous_points = self._read_point_json()

        listbox_active_tuple = self.__listbox_points.get(tk.ACTIVE)
        listbox_active_options = listbox_active_tuple.split('    \t')
        each_point = listbox_active_options[0]

        for i in range(1,30,1):
            template_path = os.path.abspath(os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, i)))
            if os.path.exists(template_path):
                os.remove(template_path)
            template_path = os.path.abspath(os.path.join(self.__default_path, '{}_E_{:02d}.tiff'.format(each_point, i)))
            if os.path.exists(template_path):
                os.remove(template_path)

        template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_I_01")))
        save_status = [True, template_path]
        ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["I_imaging_condition"]
        ht = self.microscope.beams.ion_beam.high_voltage.value
        bc = self.microscope.beams.ion_beam.beam_current.value
        I_imaging_condition = [ht, bc, mag, resolution_str, Dtime]

        self._I_imageing(save_status,I_imaging_condition)

        if self._I_adjust():
            template_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_I_01.tiff")))
            if self._template_match(template_path,I_imaging_condition):
                e_image_path = os.path.abspath(os.path.join(self.__default_path, str(each_point + "_E_01")))
                save_status = [True, e_image_path]
                ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["E_imaging_condition"]
                ht = self.microscope.beams.electron_beam.high_voltage.value
                bc = self.microscope.beams.electron_beam.beam_current.value
                E_imaging_condition = [ht, bc, mag, resolution_str, Dtime]
                self._E_imageing(save_status,E_imaging_condition)
                current_points = self._record_current_point(previous_points, each_point)
                listbox_active_index = self._update_one_point_to_listbox(current_points, each_point)
                self._update_all_points_to_map()
                self.__listbox_points.activate(listbox_active_index)
                self._current_point = each_point
        self.microscope.disconnect()
        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)

    def _delete_point(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_points.get(tk.ACTIVE) == "":
            print("no selection activated")
            return

        point_status = {}
        previous_points = self._read_point_json()

        listbox_active_tuple = self.__listbox_points.get(tk.ACTIVE)
        listbox_active_options = listbox_active_tuple.split('    \t')
        each_point = listbox_active_options[0]
        for i in range(1,30,1):
            template_path = os.path.abspath(os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, i)))
            if os.path.exists(template_path):
                os.remove(template_path)
            template_path = os.path.abspath(os.path.join(self.__default_path, '{}_E_{:02d}.tiff'.format(each_point, i)))
            if os.path.exists(template_path):
                os.remove(template_path)
        previous_points.pop(each_point)
        self._write_point_json(previous_points)
        listbox_activate_index = self.__listbox_points.index(tk.ACTIVE)
        self.__listbox_points.delete(tk.ACTIVE)
        self.__listbox_points.activate(listbox_activate_index - 1)
        self._update_all_points_to_map()

    def _goto_point(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_points.get(tk.ACTIVE) == "":
            print("no selection activated")
            return

        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)

        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.beam_shift.value = Point(x=0.0, y=0.0)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=0.0, y=0.0)
        stage_link = self.microscope.specimen.stage.is_linked
        if not stage_link:
            print("please link Z to work distance!")
            self._link_Z_warning()
            self.microscope.disconnect()
            for each_button in self.__button_group_list:
                each_button.config(state=tk.ACTIVE)
            return
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        previous_points = self._read_point_json()

        listbox_active_tuple = self.__listbox_points.get(tk.ACTIVE)
        listbox_active_options = listbox_active_tuple.split('    \t')
        each_point = listbox_active_options[0]
        for i in range(30,1,-1):
            template_path = os.path.abspath(os.path.join(self.__default_path,'{}_I_{:02d}.tiff'.format(each_point,i)))
            num = i - 1
            if os.path.exists(template_path):
                break

        self._move_stage_to_point(previous_points,each_point)
        template_path = os.path.abspath(os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, num)))
        ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["I_imaging_condition"]
        ht = self.microscope.beams.ion_beam.high_voltage.value
        bc = self.microscope.beams.ion_beam.beam_current.value
        I_imaging_condition = [ht, bc, mag, resolution_str, Dtime]

        if self._template_match(template_path, I_imaging_condition):
            ht, bc, mag, resolution_str, Dtime = previous_points[each_point]["E_imaging_condition"]
            ht = self.microscope.beams.electron_beam.high_voltage.value
            bc = self.microscope.beams.electron_beam.beam_current.value
            E_imaging_condition = [ht, bc, mag, resolution_str, Dtime]
            save_status = [False, self.__default_path]
            #self._E_imageing(save_status, E_imaging_condition)

        # load point specific patterns
        pattern_setting = previous_points[each_point]["pattern_setting"]
        self._write_pattern_json(pattern_setting)
        self.__listbox_pattern.delete(0, tk.END)
        for each_pattern in pattern_setting.keys():
            self._add_one_pattern_to_listbox(pattern_setting, each_pattern)
        self._button_side_choice_B.set(previous_points[each_point]["side_status_set"])
        self._button_side_choice_B_bool = previous_points[each_point]["side_status_set"]

        self.microscope.disconnect()
        self._current_point = each_point
        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)

    def _link_Z_warning(self):
        self.__top_warning = tk.Toplevel()
        self.__top_warning.title("link Z first")
        tk.Label(self.__top_warning, text="please link Z to work distance!").grid(row=0, column=0, columnspan=2)
        tk.Button(self.__top_warning, text="OK", command=self._destroy_win).grid(row=1, column=1)

    def _update_point_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        activate_str = self.__listbox_points.get(tk.ACTIVE)
        if activate_str == "":
            print("no selection activated")
            return

        previous_points = self._read_point_json()

        listbox_active_tuple = self.__listbox_points.get(tk.ACTIVE)
        listbox_active_options = listbox_active_tuple.split('    \t')
        each_point = listbox_active_options[0]

        previous_patterns = self._read_pattern_json()
        previous_points[each_point]["pattern_setting"] = previous_patterns
        previous_points[each_point]["side_status_set"] = self._button_side_choice_B.get()
        self._write_point_json(previous_points)

    def _move_stage_to_point(self,previous_points,each_point):
        E_wd_value = previous_points[each_point]["current_E_wd_value"]
        I_wd_value = previous_points[each_point]["current_I_wd_value"]
        stage_x = previous_points[each_point]["current_stage_x"]
        stage_y = previous_points[each_point]["current_stage_y"]
        stage_z = previous_points[each_point]["current_stage_z"]
        stage_t = previous_points[each_point]["current_stage_t"]

        new_p = StagePosition(x=stage_x,y=stage_y, z=stage_z,t=stage_t, coordinate_system="Specimen")
        self.microscope.specimen.stage.absolute_move(new_p)

        I_beam_shift_x = previous_points[each_point]["I_beam_shift_x"]
        I_beam_shift_y = previous_points[each_point]["I_beam_shift_y"]
        E_beam_shift_x = previous_points[each_point]["E_beam_shift_x"]
        E_beam_shift_y = previous_points[each_point]["E_beam_shift_y"]

        self.microscope.beams.ion_beam.beam_shift.value = Point(x=I_beam_shift_x, y=I_beam_shift_y)
        self.microscope.beams.electron_beam.beam_shift.value = Point(x=E_beam_shift_x, y=E_beam_shift_y)

        self.microscope.beams.electron_beam.working_distance.value = E_wd_value
        self.microscope.beams.ion_beam.working_distance.value = I_wd_value

    def _add_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return

        # read reference tilt angle
        ref_status, default_status = self._read_ref_json()
        if ref_status:
            self.pattern_handle_choice = self._pattern_handle_dict["add"]
            default_milling_angle = (default_status["default_stage_t"] / math.pi) * 180 - 7
            #position, milling_angle, type, width, height, Z_thick,,target_thickness,center_x,ht,bc
            default_settings = [0, "{:.1f}".format(default_milling_angle), 0,"10.0","5.0","0.35","1","0",0,4]

            self._pattern_win(default_settings)
        else:
            return

    def _pattern_win(self,default_settings):
        self._top_win = tk.Toplevel()
        # register function
        test_mill_angle_TMD = self._top_win.register(test_mill_angle)
        test_float_TMD = self._top_win.register(test_float)
        test_thickness_TMD = self._top_win.register(test_thickness)
        test_center_x_TMD = self._top_win.register(test_center_x)

        self._top_win.title("pattern parameter input")
        # build label "position" at row 0, column 0 in top_win
        tk.Label(self._top_win, text="position").grid(row=0, column=0)
        # build option "position" at row 0, column 1 in top_win
        self.__option_position_txt = tk.StringVar()
        self.__option_position_values = ["Top", "bottom"]
        self.__option_position_txt.set(self.__option_position_values[default_settings[0]])
        self.__option_position = tk.OptionMenu(self._top_win, self.__option_position_txt, *self.__option_position_values)
        self.__option_position.grid(row=0, column=1)
        # build label "mill_angle" at row 0, column 2 in top_win
        tk.Label(self._top_win, text="milling angle").grid(row=0, column=2)
        # build entry "mill_angle" at row 0, column 3 in top_win
        self.__entry_mill_angle_flt = tk.StringVar()
        self.__entry_mill_angle = tk.Entry(self._top_win, width=4, textvariable=self.__entry_mill_angle_flt,
                                           validate="focusout", validatecommand=(test_mill_angle_TMD, '%P'),
                                           invalidcommand=self._entry_invalid_mill_angle)
        self.__entry_mill_angle.grid(row=0, column=3)
        self.__entry_mill_angle.insert(0, default_settings[1])
        # build label "pattern type" at row 0, column 4 in top_win
        tk.Label(self._top_win, text="pattern type").grid(row=0, column=4)
        # build option "pattern_type" at row 0, column 5 in top_win
        self.__option_pattern_type_txt = tk.StringVar()
        self.__option_pattern_type_values = ["CCR", "rectangle"]
        self.__option_pattern_type_txt.set(self.__option_pattern_type_values[default_settings[2]])
        self.__option_pattern_type = tk.OptionMenu(self._top_win, self.__option_pattern_type_txt,
                                                   *self.__option_pattern_type_values)
        self.__option_pattern_type.grid(row=0, column=5)
        # build label "width" at row 1, column 0 in top_win
        tk.Label(self._top_win, text="width").grid(row=1, column=0)
        # build entry "width" at row 1, column 1 in top_win
        self.__entry_width_flt = tk.StringVar()
        self.__entry_width = tk.Entry(self._top_win, width=4, textvariable=self.__entry_width_flt,
                                      validate="focusout", validatecommand=(test_float_TMD, '%P'),
                                      invalidcommand=self._entry_invalid_width)
        self.__entry_width.grid(row=1, column=1)
        self.__entry_width.insert(0, default_settings[3])
        # build label "height" at row 1, column 2 in top_win
        tk.Label(self._top_win, text="height").grid(row=1, column=2)
        # build entry "height" at row 1, column 3 in top_win
        self.__entry_height_flt = tk.StringVar()
        self.__entry_height = tk.Entry(self._top_win, width=4, textvariable=self.__entry_height_flt,
                                       validate="focusout", validatecommand=(test_float_TMD, '%P'),
                                       invalidcommand=self._entry_invalid_height)
        self.__entry_height.grid(row=1, column=3)
        self.__entry_height.insert(0, default_settings[4])
        # build label "Z_thick" at row 1, column 4 in top_win
        tk.Label(self._top_win, text="Z_thick").grid(row=1, column=4)
        # build entry "Z_thick" at row 1, column 5 in top_win
        self.__entry_Z_thick_flt = tk.StringVar()
        self.__entry_Z_thick = tk.Entry(self._top_win, width=4, textvariable=self.__entry_Z_thick_flt,
                                        validate="focusout", validatecommand=(test_float_TMD, '%P'),
                                        invalidcommand=self._entry_invalid_Z_thick)
        self.__entry_Z_thick.grid(row=1, column=5)
        self.__entry_Z_thick.insert(0, default_settings[5])
        # build label "target_lamella_thickness" at row 2, column 0-1 in top_win
        tk.Label(self._top_win, text="target_lamella_thickness").grid(row=2, column=0, columnspan=2)
        # build entry "thickness" at row 2, column 2-3 in top_win
        self.__entry_thickness_flt = tk.StringVar()
        self.__entry_thickness = tk.Entry(self._top_win, width=4, textvariable=self.__entry_thickness_flt,
                                          validate="focusout", validatecommand=(test_thickness_TMD, '%P'),
                                          invalidcommand=self._entry_invalid_thickness)
        self.__entry_thickness.grid(row=2, column=2, columnspan=2)
        self.__entry_thickness.insert(0, default_settings[6])
        # build label "center_x" at row 3, column 0 in top_win
        tk.Label(self._top_win, text="center_x").grid(row=3, column=0)
        # build entry "center_x" at row 3, column 1 in top_win
        self.__entry_center_x_flt = tk.StringVar()
        self.__entry_center_x = tk.Entry(self._top_win, width=4, textvariable=self.__entry_center_x_flt,
                                         validate="focusout", validatecommand=(test_center_x_TMD, '%P'),
                                         invalidcommand=self._entry_invalid_center_x)
        self.__entry_center_x.grid(row=3, column=1)
        self.__entry_center_x.insert(0, default_settings[7])
        # build label "attention" at row 3, column 2-5 in top_win
        tk.Label(self._top_win, text="all length in micrometer, and angle in degree").grid(row=3, column=2, columnspan=3)
        # build label "high tension" at row 4, column 0 in top_win
        tk.Label(self._top_win, text="high tension").grid(row=4, column=0)
        # build option "top_win_I_HT" at row 4, column 1 in top_win
        self.__option_top_win_I_HT_txt = tk.StringVar()
        self.__option_top_win_I_HT_values = ["30.0 kV"]
        self.__option_top_win_I_HT_txt.set(self.__option_top_win_I_HT_values[default_settings[8]])
        self.__option_top_win_I_HT = tk.OptionMenu(self._top_win, self.__option_top_win_I_HT_txt,
                                                   *self.__option_top_win_I_HT_values)
        self.__option_top_win_I_HT.grid(row=4, column=1)
        # build label "beam current" at row 4, column 2 in top_win
        tk.Label(self._top_win, text="beam current").grid(row=4, column=2)
        # build option "top_win_I_BC" at row 4, column 3 in top_win
        self.__option_top_win_I_BC_txt = tk.StringVar()
        self.__option_top_win_I_BC_values = ["10 pA", "30 pA", "50 pA", "0.10 nA", "0.3 nA", "0.5 nA", "1.0 nA"]
        self.__option_top_win_I_BC_txt.set(self.__option_top_win_I_BC_values[default_settings[9]])
        self.__option_top_win_I_BC = tk.OptionMenu(self._top_win, self.__option_top_win_I_BC_txt,
                                                   *self.__option_top_win_I_BC_values)
        self.__option_top_win_I_BC.grid(row=4, column=3)
        # build button "done" at row 5, column 2 in __frame_main
        tk.Button(self._top_win, text="done", command=self._change_pattern_win_status).grid(row=5, column=2)

    def _entry_invalid_mill_angle(self):
        self.__entry_mill_angle.delete(0, tk.END)
        self.__entry_mill_angle.insert(0, "10.0")

    def _entry_invalid_width(self):
        self.__entry_width.delete(0, tk.END)
        self.__entry_width.insert(0, "10.0")

    def _entry_invalid_height(self):
        self.__entry_height.delete(0, tk.END)
        self.__entry_height.insert(0, "5.0")

    def _entry_invalid_Z_thick(self):
        self.__entry_height.delete(0, tk.END)
        self.__entry_height.insert(0, "0.35")

    def _entry_invalid_thickness(self):
        self.__entry_thickness.delete(0, tk.END)
        self.__entry_thickness.insert(0, "1")

    def _entry_invalid_center_x(self):
        self.__entry_center_x.delete(0, tk.END)
        self.__entry_center_x.insert(0, "0")

    def _change_pattern_win_status(self):
        pattern_record = self._create_pattern_record()
        previous_patterns = self._read_pattern_json()
        if self.pattern_handle_choice == 0:
            for i in range(1, 100, 1):
                pattern_number = len(previous_patterns) + i
                current_num = format('%03d' % pattern_number)
                each_point = str("pattern_" + current_num)
                try:
                    previous_patterns[each_point]
                except:
                    break

            pattern_status = {str(each_point): pattern_record}
            previous_patterns.update(pattern_status)
            print("add new pattern to {}".format(each_point))
            self._write_pattern_json(previous_patterns)
            self._add_one_pattern_to_listbox(previous_patterns, each_point)
        elif self.pattern_handle_choice == 1:
            listbox_active_tuple = self.__listbox_pattern.get(tk.ACTIVE)
            listbox_active_options = listbox_active_tuple.split('    \t')
            each_point = listbox_active_options[0]
            pattern_status = {str(each_point): pattern_record}
            previous_patterns.update(pattern_status)
            print("update {}".format(each_point))
            self._write_pattern_json(previous_patterns)
            self._update_one_pattern_to_listbox(previous_patterns, each_point)
        self._top_win.destroy()

    def _create_pattern_record(self):
        width_str = self.__entry_width_flt.get()
        width_flt = float(width_str) * 1e-6
        height_str = self.__entry_height_flt.get()
        height_flt = float(height_str)
        Z_thickness_str = self.__entry_Z_thick_flt.get()
        Z_thickness_flt = float(Z_thickness_str) * 1e-6
        target_thickness_str = self.__entry_thickness_flt.get()
        target_thickness_flt = float(target_thickness_str)
        center_x_str = self.__entry_center_x_flt.get()
        center_x_flt = float(center_x_str)

        milling_angle_str = self.__entry_mill_angle_flt.get()
        milling_angle_flt = float(milling_angle_str)
        stage_t = math.pi * (milling_angle_flt + 7) / 180

        position_str = self.__option_position_txt.get()
        if position_str == "Top":
            factor_x = 0
            factor_y = 1
            scan_direction = "1"
            position_int = 0
        elif position_str == "bottom":
            factor_x = 0
            factor_y = -1
            scan_direction = "0"
            position_int = 1
        center_x = factor_x + center_x_flt
        center_y = factor_y * ( (height_flt + target_thickness_flt) / 2)

        pattern_type_str = self.__option_pattern_type_txt.get()
        if pattern_type_str == "CCR":
            pattern_type_int = 0
        elif pattern_type_str == "rectangle":
            pattern_type_int = 1
        ht_str = self.__option_top_win_I_HT_txt.get()
        bc_str = self.__option_top_win_I_BC_txt.get()

        ht_split = ht_str.split(' ')
        ht = float(ht_split[0]) * 1000
        bc_split = bc_str.split(' ')
        if bc_split[1] == "pA":
            factor = 1e-12
        elif bc_split[1] == "nA":
            factor = 1e-9
        bc = float(bc_split[0]) * factor

        info_for_show = [center_x_str, center_y, width_str, height_str, Z_thickness_str]
        center_x = center_x * 1e-6
        center_y = center_y * 1e-6
        height_flt = height_flt * 1e-6
        info_for_set = [center_x, center_y, width_flt, height_flt, Z_thickness_flt]
        target_thickness_flt = target_thickness_flt * 1e-6

        pattern_record = {}
        pattern_record.update(pattern_position_for_show=position_str)
        pattern_record.update(pattern_position_for_set=position_int)
        pattern_record.update(pattern_type_for_show=pattern_type_str)
        pattern_record.update(pattern_type_for_set=pattern_type_int)
        pattern_record.update(pattern_I_HT_for_set=ht)
        pattern_record.update(pattern_I_HT_for_show=ht_str)
        pattern_record.update(pattern_I_bc_for_set=bc)
        pattern_record.update(pattern_I_bc_for_show=bc_str)
        pattern_record.update(stage_t=stage_t)
        pattern_record.update(milling_angle_for_show=milling_angle_str)
        pattern_record.update(info_for_show=info_for_show)
        pattern_record.update(info_for_set=info_for_set)
        pattern_record.update(thickness_for_show=target_thickness_str)
        pattern_record.update(thickness_for_set=target_thickness_flt)
        pattern_record.update(scan_direction=scan_direction)
        return pattern_record

    def _read_pattern_json(self):
        previous_patterns = {}
        json_path = os.path.abspath(os.path.join(self.__default_path, "auto_slice_pattern_json"))
        if not os.path.exists(json_path):
            with open(json_path, "w+") as default_json:
                json.dump(previous_patterns, default_json)
        with open(json_path, "r") as default_json:
            previous_patterns = json.load(default_json)
        return previous_patterns

    def _write_pattern_json(self,previous_patterns):
        json_path = os.path.abspath(os.path.join(self.__default_path, "auto_slice_pattern_json"))
        with open(json_path, "w+") as default_json:
            json.dump(previous_patterns, default_json)

    def _add_one_pattern_to_listbox(self,current_patterns, each_point):
        each_point_str = self._pattern_show_in_listbox(current_patterns, each_point)
        self.__listbox_pattern.insert(tk.END, each_point_str)

    def _pattern_show_in_listbox(self,current_patterns, each_point):
        name = each_point
        pattern_position = current_patterns[name]["pattern_position_for_show"]
        pattern_type = current_patterns[name]["pattern_type_for_show"]
        pattern_I_HT = current_patterns[name]["pattern_I_HT_for_show"]
        pattern_I_bc = current_patterns[name]["pattern_I_bc_for_show"]
        milling_angle = current_patterns[name]["milling_angle_for_show"]
        info_for_show = current_patterns[name]["info_for_show"]
        pattern_width = info_for_show[2]
        pattern_heigth = info_for_show[3]
        pattern_Z_thickness = info_for_show[4]
        each_point_str = '{}    \t{}    \t{}    \t{}    \t{}    \t{}degree    \t{}um    \t{}um    \t{}um'.format(
            name, pattern_position, pattern_type, pattern_I_HT, pattern_I_bc, milling_angle, pattern_width,
            pattern_heigth, pattern_Z_thickness)
        return each_point_str

    def _update_one_pattern_to_listbox(self,current_patterns, each_point):
        each_point_str = self._pattern_show_in_listbox(current_patterns, each_point)
        listbox_active_index = self.__listbox_pattern.index(tk.ACTIVE)
        self.__listbox_pattern.insert(listbox_active_index, each_point_str)
        self.__listbox_pattern.delete(tk.ACTIVE)

    def _change_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_pattern.get(tk.ACTIVE) == "":
            print("no selection activated")
            return
        previous_patterns = self._read_pattern_json()
        if len(previous_patterns) > 0:
            listbox_active_tuple = self.__listbox_pattern.get(tk.ACTIVE)
            listbox_active_options = listbox_active_tuple.split('    \t')
            each_point = listbox_active_options[0]
            pattern_position = previous_patterns[each_point]["pattern_position_for_set"]
            milling_angle = previous_patterns[each_point]["milling_angle_for_show"]
            pattern_type = previous_patterns[each_point]["pattern_type_for_set"]
            info_for_show = previous_patterns[each_point]["info_for_show"]
            pattern_width = info_for_show[2]
            pattern_heigth = info_for_show[3]
            pattern_Z_thickness = info_for_show[4]
            thickness = previous_patterns[each_point]["thickness_for_show"]
            center_x = info_for_show[0]
            # self.__option_top_win_I_HT_values_dict = {"8.0 kV": 0, "16.0 kV": 1, "30.0 kV": 2}
            pattern_I_HT = self.__option_top_win_I_HT_values_dict[
                previous_patterns[each_point]["pattern_I_HT_for_show"]]
            # self.__option_top_win_I_BC_values_dict = {"10 pA":0, "30 pA":1, "50 pA":2, "0.10 nA":3, "0.3 nA":4, "0.5 nA":5, "1.0 nA":6}
            pattern_I_bc = self.__option_top_win_I_BC_values_dict[
                previous_patterns[each_point]["pattern_I_bc_for_show"]]
            default_settings = [pattern_position, milling_angle, pattern_type, pattern_width, pattern_heigth,
                                pattern_Z_thickness, thickness, center_x, pattern_I_HT, pattern_I_bc]
            self.pattern_handle_choice = self._pattern_handle_dict["update"]

            self._pattern_win(default_settings)

    def _delete_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_pattern.get(tk.ACTIVE) == "":
            print("no selection activated")
            return
        previous_patterns = self._read_pattern_json()
        if len(previous_patterns) > 0:
            listbox_active_tuple = self.__listbox_pattern.get(tk.ACTIVE)
            listbox_active_options = listbox_active_tuple.split('    \t')
            each_point = listbox_active_options[0]
            previous_patterns.pop(each_point)
            self._write_pattern_json(previous_patterns)
            self.__listbox_pattern.delete(tk.ACTIVE)

    def _load_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        json_path = tkf.askopenfilename()
        #json_path = os.path.abspath(os.path.join(self.__default_path, "auto_slice_pattern_json"))
        #if not os.path.exists(json_path):
            #pattern_path = tkf.askdirectory()
            #previous_patterns = {}
            #json_path = os.path.abspath(os.path.join(pattern_path, "auto_slice_pattern_json"))
        if not os.path.exists(os.path.abspath(json_path)):
            print("no pattern file in folder")
            return
        else:
            try:
                with open(json_path, "r") as default_json:
                    previous_patterns = json.load(default_json)
                self._write_pattern_json(previous_patterns)
                self.__listbox_pattern.delete(0, tk.END)
                for each_point in previous_patterns.keys():
                    self._add_one_pattern_to_listbox(previous_patterns, each_point)
            except:
                return
        
    def _generate_side_info(self,previous_patterns):
        check_left_center_x = 0
        check_right_center_x = 0
        check_width = 1e-6
        top_height = 1e-6
        bottom_height = 1e-6
        check_thickness = 0.5 * 1e-6
        Z_thickness = 0
        check_ht = 30000
        check_bc = 0.3e-9
        pattern_num_check = 0
        for each_pattern in previous_patterns.keys():
            info_for_set = previous_patterns[each_pattern]["info_for_set"]
            if previous_patterns[each_pattern]["pattern_position_for_show"] == "Top":
                if top_height < info_for_set[3]:
                    top_height = info_for_set[3]
            elif previous_patterns[each_pattern]["pattern_position_for_show"] == "bottom":
                if bottom_height < info_for_set[3]:
                    bottom_height = info_for_set[3]
            if check_thickness < previous_patterns[each_pattern]["thickness_for_set"]:
                check_thickness = previous_patterns[each_pattern]["thickness_for_set"]
            if check_width < info_for_set[2]:
                check_width = info_for_set[2]
            if check_left_center_x > info_for_set[0]:
                check_left_center_x = info_for_set[0]
            elif check_right_center_x < info_for_set[0]:
                check_right_center_x = info_for_set[0]
            if Z_thickness < info_for_set[4]:
                Z_thickness = info_for_set[4]
            if check_ht > previous_patterns[each_pattern]["pattern_I_HT_for_set"]:
                check_ht = previous_patterns[each_pattern]["pattern_I_HT_for_set"]
            if check_bc > previous_patterns[each_pattern]["pattern_I_bc_for_set"]:
                check_bc = previous_patterns[each_pattern]["pattern_I_bc_for_set"]
            pattern_num_check += 1
            if pattern_num_check >= 2:
                break
        side_left_center_x = check_left_center_x - (check_width / 2) - 3e-6
        side_right_center_x = check_right_center_x + (check_width / 2) + 3e-6
        height = top_height + check_thickness + bottom_height

        side_info = [side_left_center_x, side_right_center_x, 0, 0.25e-6, height, Z_thickness]

        return side_info,check_ht,check_bc

    def _show_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self._button_pattern_status == False:
            previous_patterns = self._read_pattern_json()
            if len(previous_patterns) > 0:
                self.microscope = SdbMicroscopeClient()
                self.microscope.connect()
                self.microscope.patterning.set_default_beam_type(BeamType.ION)
                self.microscope.patterning.set_default_application_file("Si")
                self.microscope.imaging.set_active_view(2)
                self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
                self.microscope.patterning.clear_patterns()
                for each_pattern in previous_patterns.keys():
                    self._set_one_pattern(previous_patterns, each_pattern)
                    self._set_ref_pattern_tiff(previous_patterns, each_pattern)

                if self._button_side_choice_B.get():
                    self._set_side_pattern(previous_patterns)
                    self._set_ref_pattern_side_tiff(previous_patterns)
                self.microscope.disconnect()
            self._button_pattern_txt.set("clear pattern")
            self._button_pattern_status = True
            self.__button_thin_start_milling.config(state=tk.ACTIVE)
        else:
            self.microscope = SdbMicroscopeClient()
            self.microscope.connect()
            self.microscope.imaging.set_active_view(2)
            #self.__current_pattern = ""
            self.microscope.patterning.clear_patterns()
            self._remove_pattern_tiff()
            self.microscope.disconnect()
            self._button_pattern_txt.set("show pattern")
            self._button_pattern_status = False

    def _mill_here(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        try:
            print(self._current_point)
        except AttributeError:
            print("please add point first!")
            return
        print(len(self.__button_group_list))
        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)
        self.__button_stop_mill.config(state=tk.ACTIVE)

        stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
        if os.path.exists(stop_file):
            os.remove(stop_file)

        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)

        previous_points = self._read_point_json()
        each_point = self._current_point
        print("{}:milling start".format(each_point))

        thin_status = previous_points[each_point]["thin_status"]
        side_status = previous_points[each_point]["side_status"]

        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, i)))
            new_num = i - 1
            if os.path.exists(template_path):
                break
        template_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        imaging_condition = previous_points[each_point]["I_imaging_condition"]

        self._auto_mill_action(thin_status,side_status,template_path, imaging_condition)

        previous_points[each_point]["thin_status"] = True
        if self._button_side_choice_B.get():
            previous_points[each_point]["side_status"] = True
        self._write_point_json(previous_points)
        self.__listbox_points.delete(0, tk.END)
        self._load_all_point_to_listbox(previous_points)

        new_num = new_num + 1
        template_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_I_{:02d}'.format(each_point, new_num)))
        save_status = [True, template_path]
        self._I_imageing(save_status, imaging_condition)

        template_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_E_{:02d}'.format(each_point, new_num)))
        save_status = [True, template_path]
        imaging_condition = previous_points[each_point]["E_imaging_condition"]
        self._E_imageing(save_status, imaging_condition)

        self.microscope.disconnect()
        print("{}: milling end".format(each_point))

        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)
        self.__button_stop_mill.config(state=tk.DISABLED)

    def _auto_mill_action(self,thin_status,side_status,template_path, imaging_condition):
        mill_begin = False
        pattern_num_check = 0
        previous_patterns = self._read_pattern_json()
        if len(previous_patterns) > 0:
            self.microscope.patterning.clear_patterns()
            if thin_status == False:
                mill_begin = True
                for each_pattern in previous_patterns.keys():
                    self._set_one_pattern(previous_patterns,each_pattern)
                    self._set_ref_pattern_tiff(previous_patterns, each_pattern)
                    pattern_num_check += 1
                    if pattern_num_check >= 2:
                        break

            if self._button_side_choice_B_bool and side_status == False:
                mill_begin = True
                self._set_side_pattern(previous_patterns)
                self._set_ref_pattern_side_tiff(previous_patterns)
            if mill_begin:
                ht = previous_patterns[each_pattern]["pattern_I_HT_for_set"]
                bc = previous_patterns[each_pattern]["pattern_I_bc_for_set"]
                self.microscope.beams.ion_beam.high_voltage.value = ht
                self.microscope.beams.ion_beam.beam_current.value = bc
                self.microscope.patterning.mode = "Parallel"
                self.microscope.patterning.run()
                self.microscope.patterning.clear_patterns()
            stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
            if os.path.exists(stop_file):
                return
            pattern_num_check = 0
            for each_pattern in previous_patterns.keys():
                stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
                if os.path.exists(stop_file):
                    return
                pattern_num_check += 1
                self._set_ref_pattern_tiff(previous_patterns, each_pattern)
                if self._button_side_choice_B_bool:
                    self._set_ref_pattern_side_tiff(previous_patterns)
                if not pattern_num_check <= 2:
                    stage_t = previous_patterns[each_pattern]["stage_t"]
                    new_p = StagePosition(t=stage_t)
                    self.microscope.specimen.stage.absolute_move(new_p)

                    if self._template_match_beam_shift(template_path, imaging_condition):
                        self._set_one_pattern(previous_patterns, each_pattern)
                        ht = previous_patterns[each_pattern]["pattern_I_HT_for_set"]
                        bc = previous_patterns[each_pattern]["pattern_I_bc_for_set"]
                        self.microscope.beams.ion_beam.high_voltage.value = ht
                        self.microscope.beams.ion_beam.beam_current.value = bc
                        self.microscope.patterning.mode = "Parallel"
                        self.microscope.patterning.run()
                        self.microscope.patterning.clear_patterns()
                    else:
                        print("{} milling failed".format(each_pattern))

    def _remove_pattern_tiff(self):
        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        if os.path.exists(ref_pattern_tiff_path):
            os.remove(ref_pattern_tiff_path)

    def _set_ref_pattern_tiff(self,previous_patterns,each_pattern):
        info_for_set = previous_patterns[each_pattern]["info_for_set"]
        pattern_center_x = info_for_set[0]
        pattern_center_y = info_for_set[1]
        pattern_width = info_for_set[2]
        pattern_height = info_for_set[3]
        self._pattern_to_tiff(pattern_center_x,pattern_center_y,pattern_width,pattern_height)
        ref_pattern_tiff_1_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern1.tiff"))
        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        if os.path.exists(ref_pattern_tiff_1_path):
            os.system("copy {} {}".format(ref_pattern_tiff_1_path, ref_pattern_tiff_path))

    def _set_ref_pattern_side_tiff(self,previous_patterns):
        side_info, check_ht, check_bc = self._generate_side_info(previous_patterns)
        self._pattern_to_tiff(side_info[0], side_info[2], side_info[3], side_info[4])
        ref_pattern_tiff_1_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern1.tiff"))
        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        if os.path.exists(ref_pattern_tiff_1_path):
            os.system("copy {} {}".format(ref_pattern_tiff_1_path, ref_pattern_tiff_path))

        self._pattern_to_tiff(side_info[1], side_info[2], side_info[3], side_info[4])
        ref_pattern_tiff_1_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern1.tiff"))
        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        if os.path.exists(ref_pattern_tiff_1_path):
            os.system("copy {} {}".format(ref_pattern_tiff_1_path, ref_pattern_tiff_path))

    def _pattern_to_tiff(self,pattern_center_x,pattern_center_y,pattern_width,pattern_height):
        ht, bc, mag, resolution_str, Dtime = self._image_prep("ion")
        resolution_list = resolution_str.split('x')
        tiff_img_x = int(resolution_list[0])
        tiff_img_x_reduce = round(tiff_img_x * 0.4)
        #tiff_img_x_reduce = round(tiff_img_x * 1)
        tiff_img_y = int(resolution_list[1])
        tiff_img_y_reduce = round(tiff_img_y * 0.6)
        #tiff_img_y_reduce = round(tiff_img_y * 1)

        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
        if os.path.exists(ref_pattern_tiff_path):
            ref_pattern_tiff = Image.open(ref_pattern_tiff_path)
        else:
            print(tiff_img_x_reduce,tiff_img_y_reduce)
            ref_pattern_tiff = Image.new('L', (tiff_img_x_reduce, tiff_img_y_reduce), 128)
        pattern_pixel_size = mag / tiff_img_x
        pattern_center_x = pattern_center_x / pattern_pixel_size
        pattern_center_y = pattern_center_y / pattern_pixel_size
        pattern_width = pattern_width / pattern_pixel_size
        pattern_height = pattern_height / pattern_pixel_size

        tiff_draw_left_top_x = round(
            tiff_img_x_reduce / 2 - pattern_width / 2 + pattern_center_x)
        tiff_draw_left_top_y = round(
            tiff_img_y_reduce / 2 - pattern_height / 2 - pattern_center_y)
        tiff_draw_right_buttom_x = round(
            tiff_img_x_reduce / 2 + pattern_width / 2 + pattern_center_x)
        tiff_draw_right_buttom_y = round(
            tiff_img_y_reduce / 2 + pattern_height / 2 - pattern_center_y)

        pattern_draw = ImageDraw.Draw(ref_pattern_tiff)
        pattern_draw.rectangle(
            (tiff_draw_left_top_x, tiff_draw_left_top_y, tiff_draw_right_buttom_x, tiff_draw_right_buttom_y), fill=0)

        ref_pattern_tiff_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern1.tiff"))
        ref_pattern_tiff.save(ref_pattern_tiff_path, "tiff")

    def _set_one_pattern(self,previous_patterns,each_pattern):
        pattern_type = previous_patterns[each_pattern]["pattern_type_for_show"]
        info_for_set = previous_patterns[each_pattern]["info_for_set"]
        scan_direction = previous_patterns[each_pattern]["scan_direction"]
        print(each_pattern,pattern_type)
        if pattern_type == "CCR":
            pattern_ccr = self.microscope.patterning.create_cleaning_cross_section(info_for_set[0],
                                                                                   info_for_set[1],
                                                                                   info_for_set[2],
                                                                                   info_for_set[3],
                                                                                   info_for_set[4])
            pattern_ccr.scan_direction = scan_direction

        elif pattern_type == "rectangle":
            pattern_rect = self.microscope.patterning.create_rectangle(info_for_set[0],
                                                                       info_for_set[1],
                                                                       info_for_set[2],
                                                                       info_for_set[3],
                                                                       info_for_set[4])
            pattern_rect.scan_direction = scan_direction

    def _set_side_pattern(self,previous_patterns):
        side_info, check_ht, check_bc = self._generate_side_info(previous_patterns)
        # pattern CCS left
        pattern_LCCS = self.microscope.patterning.create_rectangle(side_info[0], side_info[2],
                                                                   side_info[3],
                                                                   side_info[4], side_info[5])
        pattern_LCCS.scan_direction = "3"
        # pattern CCS right
        pattern_RCCS = self.microscope.patterning.create_rectangle(side_info[1], side_info[2],
                                                                   side_info[3],
                                                                   side_info[4], side_info[5])
        pattern_RCCS.scan_direction = "2"
        #self.microscope.beams.ion_beam.high_voltage.value = check_ht
        #self.microscope.beams.ion_beam.beam_current.value = check_bc

    def _set_side_pattern_ccs(self,previous_patterns):
        side_info, check_ht, check_bc = self._generate_side_info(previous_patterns)
        # pattern CCS left
        pattern_LCCS = self.microscope.patterning.create_cleaning_cross_section(side_info[0], side_info[2],
                                                                   side_info[3],
                                                                   side_info[4], side_info[5])
        pattern_LCCS.scan_direction = "3"
        # pattern CCS right
        pattern_RCCS = self.microscope.patterning.create_cleaning_cross_section(side_info[1], side_info[2],
                                                                   side_info[3],
                                                                   side_info[4], side_info[5])
        pattern_RCCS.scan_direction = "2"

    def _set_cross_pattern(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        self.microscope.patterning.create_rectangle(-29.8e-6,0,2e-6,1e-6,0.1e-6)
        self.microscope.patterning.create_rectangle(-26e-6,0,1e-6,2e-6, 0.3e-6)
        #self.microscope.patterning.create_rectangle(-29.8e-6, 0, 1.5e-6, 0.5e-6, 0.1e-6)
        self.microscope.disconnect()

    def _auto_mill_sequent(self,previous_patterns,each_pattern,template_path,imaging_condition):
        previous_patterns = self._read_pattern_json()
        pattern_num_check = 0
        if len(previous_patterns) > 0:
            self.microscope.patterning.clear_patterns()
            for each_pattern in previous_patterns.keys():
                stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
                if os.path.exists(stop_file):
                    return
                stage_t = previous_patterns[each_pattern]["stage_t"]
                new_p = StagePosition(t=stage_t)
                self.microscope.specimen.stage.absolute_move(new_p)
                if self._template_match_beam_shift(template_path, imaging_condition):
                    self._set_one_pattern(previous_patterns, each_pattern)
                    self._set_ref_pattern_side_tiff(previous_patterns)
                    ht = previous_patterns[each_pattern]["pattern_I_HT_for_set"]
                    bc = previous_patterns[each_pattern]["pattern_I_bc_for_set"]
                    self.microscope.beams.ion_beam.high_voltage.value = ht
                    self.microscope.beams.ion_beam.beam_current.value = bc
                    self.microscope.patterning.run()
                    self.microscope.patterning.clear_patterns()
                else:
                    print("{} milling failed".format(each_pattern))
                if pattern_num_check >= 2:
                    break
            if self._button_side_choice_B_bool and side_status == False:
                mill_begin = True
                self._set_side_pattern(previous_patterns)
                self._set_ref_pattern_side_tiff(previous_patterns)
                self.microscope.patterning.run()
                self.microscope.patterning.clear_patterns()
            stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
            if os.path.exists(stop_file):
                return
            pattern_num_check = 0
            for each_pattern in previous_patterns.keys():
                stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
                if os.path.exists(stop_file):
                    return
                pattern_num_check += 1
                self._set_ref_pattern_tiff(previous_patterns, each_pattern)
                if self._button_side_choice_B_bool:
                    self._set_ref_pattern_side_tiff(previous_patterns)
                if not pattern_num_check <= 2:
                    stage_t = previous_patterns[each_pattern]["stage_t"]
                    new_p = StagePosition(t=stage_t)
                    self.microscope.specimen.stage.absolute_move(new_p)

                    if self._template_match_beam_shift(template_path, imaging_condition):
                        self._set_one_pattern(previous_patterns, each_pattern)
                        ht = previous_patterns[each_pattern]["pattern_I_HT_for_set"]
                        bc = previous_patterns[each_pattern]["pattern_I_bc_for_set"]
                        self.microscope.beams.ion_beam.high_voltage.value = ht
                        self.microscope.beams.ion_beam.beam_current.value = bc
                        self.microscope.patterning.mode = "Parallel"
                        self.microscope.patterning.run()
                        self.microscope.patterning.clear_patterns()
                    else:
                        print("{} milling failed".format(each_pattern))

    def _check_mill_status(self,previous_points,each_point):
        thin_status = previous_points[each_point]["thin_status"]
        side_status = previous_points[each_point]["side_status"]
        if thin_status:
            if self._button_side_choice_B.get() and side_status == False:
                return True
            return False
        else:
            return True

    def _check_pattern_mill_angle(self):
        #milling angles of all patterns are the same, return True, else return False
        stage_t = 0
        pattern_num_check = 0
        previous_patterns = self._read_pattern_json()
        if len(previous_patterns) > 0:
            angle_dict = {}
            for each_pattern in previous_patterns.keys():
                stage_t = previous_patterns[each_pattern]["stage_t"]
                one_angle_dict = {str(stage_t):1}
                angle_dict.update(one_angle_dict)

                pattern_num_check += 1
                if pattern_num_check >= 2:
                    break
            if len(angle_dict) > 1:
                return False, stage_t
            else:
                return True, stage_t
        return True, stage_t

    def _mill_all(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        for each_button in self.__button_group_list:
            each_button.config(state=tk.DISABLED)
        self.__button_stop_mill.config(state=tk.ACTIVE)

        stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
        if os.path.exists(stop_file):
            os.remove(stop_file)

        previous_points = self._read_point_json()
        if len(previous_points) > 0:
            for each_point in previous_points.keys():
                if os.path.exists(stop_file):
                    os.remove(stop_file)
                    print("stopped")
                    break
                if self._check_mill_status(previous_points,each_point):
                    print("{}: milling start".format(each_point))
                    self.microscope = SdbMicroscopeClient()
                    self.microscope.connect()
                    self.microscope.beams.electron_beam.scanning.rotation.value = math.pi
                    self.microscope.beams.ion_beam.scanning.rotation.value = math.pi
                    self.microscope.beams.ion_beam.turn_on()
                    self.microscope.beams.electron_beam.turn_on()
                    self.microscope.patterning.set_default_beam_type(BeamType.ION)
                    self.microscope.patterning.set_default_application_file("Si")
                    self.microscope.imaging.set_active_view(2)
                    self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
                    self.microscope.patterning.clear_patterns()
                    self._remove_pattern_tiff()
                    for i in range(30, 1, -1):
                        template_path = os.path.abspath(
                            os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, i)))
                        new_num = i - 1
                        if os.path.exists(template_path):
                            break
                    self._move_stage_to_point(previous_points, each_point)
                    template_path = os.path.abspath(
                        os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, new_num)))
                    I_imaging_condition = previous_points[each_point]["I_imaging_condition"]
                    if self._template_match(template_path, I_imaging_condition):

                        # load point specific patterns
                        pattern_setting = previous_points[each_point]["pattern_setting"]
                        self._write_pattern_json(pattern_setting)
                        self.__listbox_pattern.delete(0, tk.END)
                        for each_pattern in pattern_setting.keys():
                            self._add_one_pattern_to_listbox(pattern_setting, each_pattern)
                        self._button_side_choice_B.set(previous_points[each_point]["side_status_set"])
                        self._button_side_choice_B_bool = previous_points[each_point]["side_status_set"]

                        mill_angle_status, stage_t = self._check_pattern_mill_angle()
                        if mill_angle_status:
                            thin_status = previous_points[each_point]["thin_status"]
                            side_status = previous_points[each_point]["side_status"]
                            template_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
                            self._auto_mill_action(thin_status, side_status, template_path, I_imaging_condition)
                        else:
                            template_path = os.path.abspath(os.path.join(self.__default_path, "ref_pattern.tiff"))
                            self._button_side_choice_B.set(False)
                            self._auto_mill_sequent(template_path, I_imaging_condition)

                        previous_points[each_point]["thin_status"] = True
                        if self._button_side_choice_B.get():
                            previous_points[each_point]["side_status"] = True
                        self._write_point_json(previous_points)
                        self.__listbox_points.delete(0, tk.END)
                        self._load_all_point_to_listbox(previous_points)

                        new_num = new_num + 1
                        template_path = os.path.abspath(
                            os.path.join(self.__default_path, '{}_I_{:02d}'.format(each_point, new_num)))
                        save_status = [True, template_path]
                        self._I_imageing(save_status, I_imaging_condition)

                        template_path = os.path.abspath(
                            os.path.join(self.__default_path, '{}_E_{:02d}'.format(each_point, new_num)))
                        save_status = [True, template_path]
                        imaging_condition = previous_points[each_point]["E_imaging_condition"]
                        self._E_imageing(save_status, imaging_condition)
                    self.microscope.disconnect()
                    print("{}: milling end".format(each_point))
        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)
        self.__button_stop_mill.config(state=tk.DISABLED)

    def _thread_function(self,funrction):
        self._win_thread = threading.Thread(target=funrction)
        self._win_thread.setDaemon(True)
        self._win_thread.start()

    def _stop_milling(self):
        stop_file = os.path.abspath(os.path.join(self.__default_path, "stop.txt"))
        with open(stop_file, "w+") as stop_file_c:
            stop_file_c.write("")
        print("stopping")

    def _image_prep(self,beam_type):
        if beam_type == "ion":
            ht_str = self.__option_I_HT_txt.get()
            bc_str = self.__option_I_BC_txt.get()
            mag_str = self.__option_I_mag_txt.get()
            resolution_str = self.__option_I_resolution_txt.get()
            Dtime_str = self.__option_I_Dtime_txt.get()
            mag_dict = self.__option_I_mag_dict
        elif beam_type == "electron":
            ht_str = self.__option_E_HT_txt.get()
            bc_str = self.__option_E_BC_txt.get()
            mag_str = self.__option_E_mag_txt.get()
            resolution_str = self.__option_E_resolution_txt.get()
            Dtime_str = self.__option_E_Dtime_txt.get()
            mag_dict = self.__option_E_mag_dict

        ht_split = ht_str.split(' ')
        ht = float(ht_split[0]) * 1000
        bc_split = bc_str.split(' ')
        if bc_split[1] == "pA":
            factor = 1e-12
        elif bc_split[1] == "nA":
            factor = 1e-9
        bc = float(bc_split[0]) * factor
        mag = mag_dict[mag_str]
        Dtime_split = Dtime_str.split(' ')
        if Dtime_split[1] == "ns":
            factor = 1e-9
        elif Dtime_split[1] == "us":
            factor = 1e-6
        Dtime = int(Dtime_split[0]) * factor
        return ht, bc, mag, resolution_str, Dtime

    def _I_imageing_side(self,save_status,img_condition):
        if not len(img_condition) > 0:
            ht, bc, mag, resolution_str, Dtime = self._image_prep("ion")
        else:
            ht, bc, mag, resolution_str, Dtime = img_condition

        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)

        self.microscope.beams.ion_beam.high_voltage.value = ht
        self.microscope.beams.ion_beam.beam_current.value = bc
        self.microscope.beams.ion_beam.horizontal_field_width.value = mag
        settings = GrabFrameSettings(resolution=resolution_str, dwell_time=Dtime,reduced_area=Rectangle(0.3, 0.2, 0.4, 0.6))
        if save_status[0]:
            self.microscope.imaging.grab_frame_to_disk(save_status[1], 'tiff', settings)
        else:
            image_taken = self.microscope.imaging.grab_frame(settings)
            return image_taken

    def _I_imageing(self,save_status,img_condition):
        if not len(img_condition) > 0:
            ht, bc, mag, resolution_str, Dtime = self._image_prep("ion")
        else:
            ht, bc, mag, resolution_str, Dtime = img_condition

        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)

        self.microscope.beams.ion_beam.high_voltage.value = ht
        self.microscope.beams.ion_beam.beam_current.value = bc
        self.microscope.beams.ion_beam.horizontal_field_width.value = mag
        settings = GrabFrameSettings(resolution=resolution_str, dwell_time=Dtime)
        if save_status[0]:
            self.microscope.imaging.grab_frame_to_disk(save_status[1], 'tiff', settings)
        else:
            image_taken = self.microscope.imaging.grab_frame(settings)
            return image_taken

    def _E_imageing(self,save_status,img_condition):
        if not len(img_condition) > 0:
            ht, bc, mag, resolution_str, Dtime = self._image_prep("electron")
        else:
            ht, bc, mag, resolution_str, Dtime = img_condition

        self.microscope.imaging.set_active_view(1)
        self.microscope.imaging.set_active_device(ImagingDevice.ELECTRON_BEAM)

        self.microscope.beams.electron_beam.high_voltage.value = ht
        self.microscope.beams.electron_beam.beam_current.value = bc
        self.microscope.beams.electron_beam.horizontal_field_width.value = mag
        settings = GrabFrameSettings(resolution=resolution_str, dwell_time=Dtime)
        if save_status[0]:
            self.microscope.imaging.grab_frame_to_disk(save_status[1], 'tiff', settings)
        else:
            image_taken = self.microscope.imaging.grab_frame(settings)
            return image_taken

    def _thin_tilt_angle_1(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        milling_angle = float(self.__entry_thin_angle_1_flt.get())
        stage_t = math.pi * ( milling_angle + 7 ) / 180
        new_p = StagePosition(t=stage_t, coordinate_system="Specimen")
        self.microscope.specimen.stage.absolute_move(new_p)
        self.microscope.disconnect()

    def _thin_tilt_angle_2(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        milling_angle = float(self.__entry_thin_angle_2_flt.get())
        stage_t = math.pi * ( milling_angle + 7 ) / 180
        new_p = StagePosition(t=stage_t, coordinate_system="Specimen")
        self.microscope.specimen.stage.absolute_move(new_p)
        self.microscope.disconnect()

    def _thin_show_select_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        if self.__listbox_pattern.get(tk.ACTIVE) == "":
            print("no selection activated")
            return
        previous_patterns = self._read_pattern_json()
        if len(previous_patterns) > 0:
            listbox_active_tuple = self.__listbox_pattern.get(tk.ACTIVE)
            listbox_active_options = listbox_active_tuple.split('    \t')
            each_pattern = listbox_active_options[0]
            self.microscope = SdbMicroscopeClient()
            self.microscope.connect()
            self.microscope.patterning.set_default_beam_type(BeamType.ION)
            self.microscope.patterning.set_default_application_file("Si")
            self.microscope.imaging.set_active_view(2)
            self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
            self._set_one_pattern(previous_patterns, each_pattern)
            self._set_ref_pattern_tiff(previous_patterns, each_pattern)

            self.microscope.disconnect()

    def _thin_switch_pattern_direction(self):
        try:
            print(self.__current_pattern.scan_direction)
        except:
            print("switch scan direction failed: no pattern")
            return
        current_direction = self.__current_pattern.scan_direction
        if current_direction == "0":
            self.__current_pattern.scan_direction = "1"
        else:
            self.__current_pattern.scan_direction = "0"

    def _thin_show_ccs_side_pattern(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        previous_patterns = self._read_pattern_json()
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        self._set_side_pattern_ccs(previous_patterns)
        self._set_ref_pattern_side_tiff(previous_patterns)
        self.microscope.disconnect()

    def _thin_clear_pattern(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.imaging.set_active_view(2)
        self.microscope.patterning.clear_patterns()
        self._remove_pattern_tiff()
        self.microscope.disconnect()

    def _thin_take_I_image(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        self._I_temp_image = self.microscope.imaging.grab_frame()

        self.microscope.disconnect()

    def _thin_save_I_image(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        try:
            print(self._current_point)
        except AttributeError:
            print("please add point first!")
            return
        try:
            print(self._I_temp_image.width)
        except:
            print("no I image have been taken")
            return
        each_point = self._current_point
        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_I_thin{:02d}.tiff'.format(each_point, i)))
            new_num = i
            if os.path.exists(template_path):
                break

        image_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_I_thin{:02d}.tiff'.format(each_point, new_num)))
        self._I_temp_image.save(image_path)

    def _thin_take_E_image(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.electron_beam.turn_on()
        self.microscope.imaging.set_active_view(1)
        self.microscope.imaging.set_active_device(ImagingDevice.ELECTRON_BEAM)
        self._E_temp_image = self.microscope.imaging.grab_frame()

        self.microscope.disconnect()

    def _thin_save_E_image(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        try:
            print(self._current_point)
        except AttributeError:
            print("please add point first!")
            return
        try:
            print(self._E_temp_image.width)
        except:
            print("no I image have been taken")
            return
        each_point = self._current_point
        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_E_thin{:02d}.tiff'.format(each_point, i)))
            new_num = i
            if os.path.exists(template_path):
                break

        image_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_E_thin{:02d}.tiff'.format(each_point, new_num)))
        self._E_temp_image.save(image_path)

    def _thin_start_milling(self):
        try:
            print(self.__default_path)
        except AttributeError:
            print("please set user folder")
            return
        try:
            print(self._current_point)
        except AttributeError:
            print("please add point first!")
            return
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        self.__button_thin_start_milling.config(state=tk.DISABLED)
        self.__button_thin_pause_milling.config(state=tk.ACTIVE)
        self.__button_thin_stop_milling.config(state=tk.ACTIVE)
        try:
            self.microscope.patterning.start()
            for each_button in self.__button_group_list:
                each_button.config(state=tk.DISABLED)
        except:
            print("start failed: no pattern created")
            for each_button in self.__button_group_list:
                each_button.config(state=tk.ACTIVE)
            self.__button_thin_start_milling.config(state=tk.ACTIVE)
            self.__button_thin_pause_milling.config(state=tk.DISABLED)
            self.__button_thin_stop_milling.config(state=tk.DISABLED)

        self.microscope.disconnect()

    def _thin_pause_milling(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        self.__button_thin_start_milling.config(state=tk.DISABLED)
        self.__button_thin_stop_milling.config(state=tk.ACTIVE)
        button_txt = self.__button_thin_pause_milling_txt.get()
        if button_txt == "pause":
            try:
                self.microscope.patterning.pause()
                self._I_temp_image = self.microscope.imaging.grab_frame()
                self.__button_thin_I_image.config(state=tk.ACTIVE)
                self.__button_thin_save_I_image.config(state=tk.ACTIVE)
                self.__button_thin_E_image.config(state=tk.ACTIVE)
                self.__button_thin_save_E_image.config(state=tk.ACTIVE)
            except:
                print("pause failed: no patterning running")
            self.__button_thin_pause_milling_txt.set("resume")
        elif button_txt == "resume":
            try:
                self.microscope.patterning.resume()
            except:
                print("resume failed: no patterning running")
            self.__button_thin_pause_milling_txt.set("pause")
            for each_button in self.__button_group_list:
                each_button.config(state=tk.DISABLED)

        self.microscope.disconnect()

    def _thin_stop_milling(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        self.microscope.beams.ion_beam.turn_on()
        self.microscope.beams.electron_beam.turn_on()
        self.microscope.patterning.set_default_beam_type(BeamType.ION)
        self.microscope.patterning.set_default_application_file("Si")
        self.microscope.imaging.set_active_view(2)
        self.microscope.imaging.set_active_device(ImagingDevice.ION_BEAM)
        try:
            self.microscope.patterning.stop()
        except:
            print("stop failed: no patterning running")
        each_point = self._current_point
        for i in range(30, 1, -1):
            template_path = os.path.abspath(
                os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, i)))
            new_num = i + 1
            if os.path.exists(template_path):
                break

        self._I_temp_image = self.microscope.imaging.grab_frame()
        image_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_I_{:02d}.tiff'.format(each_point, new_num)))
        self._I_temp_image.save(image_path)

        self.microscope.imaging.set_active_view(1)
        self.microscope.imaging.set_active_device(ImagingDevice.ELECTRON_BEAM)
        self._E_temp_image = self.microscope.imaging.grab_frame()
        image_path = os.path.abspath(
            os.path.join(self.__default_path, '{}_E_{:02d}.tiff'.format(each_point, new_num)))
        self._E_temp_image.save(image_path)

        for each_button in self.__button_group_list:
            each_button.config(state=tk.ACTIVE)
        self.__button_thin_pause_milling.config(state=tk.DISABLED)
        self.__button_thin_stop_milling.config(state=tk.DISABLED)

        self.microscope.disconnect()

    def _i_scan_rotation_1(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        scan_angle_str = self.__entry_thin_scan_angle_1_flt.get()
        scan_angle = math.pi * float(scan_angle_str) / 180
        self.microscope.beams.ion_beam.scanning.rotation.value = scan_angle
        self.microscope.disconnect()

    def _i_scan_rotation_2(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        scan_angle_str = self.__entry_thin_scan_angle_2_flt.get()
        scan_angle = math.pi * float(scan_angle_str) / 180
        self.microscope.beams.ion_beam.scanning.rotation.value = scan_angle
        self.microscope.disconnect()

    def _i_scan_rotation_180(self):
        self.microscope = SdbMicroscopeClient()
        self.microscope.connect()
        scan_angle = math.pi
        self.microscope.beams.ion_beam.scanning.rotation.value = scan_angle
        self.microscope.disconnect()

    def mainloop(self):
        self.__main_win.mainloop()


if __name__ == '__main__':
    point_input_ui()
