import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.main_box)

        self.titre = Gtk.Label(label="Chi Fou Mi Cozmo")
        self.main_box.pack_start(self.titre, True, True, 0)

        self.round_box = Gtk.Box(spacing=6)
        self.main_box.pack_start(self.round_box, True, True, 0)

        self.button_minus = Gtk.Button(label="-")
        self.button_minus.connect("clicked", self.on_button_minus_clicked)
        self.round_box.pack_start(self.button_minus, True, True, 0)

        self.label_round = Gtk.Label(label="1")
        self.round_box.pack_start(self.label_round, True, True, 0)

        self.button_plus = Gtk.Button(label="+")
        self.button_plus.connect("clicked", self.on_button_plus_clicked)
        self.round_box.pack_start(self.button_plus, True, True, 0)


    def on_button_plus_clicked(self, widget):
        self.label_round.set_label("10")

    def on_button_minus_clicked(self, widget):
        self.label_round.set_label("1")



win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()