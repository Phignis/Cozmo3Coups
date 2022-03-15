#!/bin/python3

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

import os
import subprocess


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Cozmo fait les 3 coups")

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.main_box)

        self.titre = Gtk.Label(label="Chi Fou Mi Cozmo")
        self.main_box.pack_start(self.titre, True, True, 0)

        self.titre.get_style_context().add_class("title")


        # Selection nb point gagnants
        self.box_selection_nb_point_gagnant = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.box_selection_nb_point_gagnant.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(self.box_selection_nb_point_gagnant, False, False, 0)

        self.label_points_gagnants = Gtk.Label(label="Nombre de points gagnants")
        self.box_selection_nb_point_gagnant.pack_start(self.label_points_gagnants, False, False, 0)

        adjustement = Gtk.Adjustment(value=1, lower=1, upper=9, step_increment=1, page_increment=10)
        self.spinbutton_points_gagnants = Gtk.SpinButton()
        self.spinbutton_points_gagnants.set_adjustment(adjustement)
        self.spinbutton_points_gagnants.set_snap_to_ticks(True)
        self.spinbutton_points_gagnants.set_numeric(True)
        self.box_selection_nb_point_gagnant.pack_start(self.spinbutton_points_gagnants, False, False, 0)


        # Start
        self.button_start = Gtk.Button(label="Start")
        self.button_start.connect("clicked", self.start_clicked)
        self.main_box.pack_start(self.button_start, True, True, 0)
        self.button_start.get_style_context().add_class("start")
        self.button_start.set_valign(Gtk.Align.CENTER)
        self.button_start.set_halign(Gtk.Align.CENTER)

        self.load_css()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        css_provider.load_from_path(os.path.join(current_directory, "../resources/css/theme.css"))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def start_clicked(self, _):
        print("Start ! ", self.get_nb_points_gagnants())
        current_directory = os.path.dirname(os.path.realpath(__file__))
        subprocess.run(args=[os.path.join(current_directory, "main.py"), str(self.get_nb_points_gagnants())])

    def get_nb_points_gagnants(self):
        return int(self.spinbutton_points_gagnants.get_value())


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
