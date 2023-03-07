import gi, sys, os, json
from deepface import DeepFace
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

max_size = 640
whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))

dialog = Gtk.FileChooserDialog(
    title='Odpri sliko', parent=None, action=Gtk.FileChooserAction.OPEN,
    buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

def PrintConsole(text):
    global abuilder
    console_view = abuilder.get_object("lblConsole")
    console_view.get_buffer().set_text("[INFO] " + str(text))

class HandleSignals:
    global dialog, abuilder, max_size

    def onQuit(self, *a, **kv):
        print("[STATUS] Close app")
        PrintConsole("[STATUS] Zapiranje aplikacije")
        sys.exit(0)

    def on_bntBrowse_clicked(self, *a, **kv):
        print("[EVENT] Clicked browse button")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("[INFO] Selected file to open: {}".format(dialog.get_filename()))
            # Display path text
            path_label = abuilder.get_object("lblSelectedFile")
            path_label.set_text(dialog.get_filename()) 
            # Display image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())
            original_width = pixbuf.get_width()
            original_height = pixbuf.get_height()
            scale_factor = max_size / float(original_width if original_width > original_height else original_height)
            scaled_pixbuf = pixbuf.scale_simple(int(original_width * scale_factor), int(original_height * scale_factor), GdkPixbuf.InterpType.BILINEAR)
            image = abuilder.get_object("imgFace")
            image.set_from_pixbuf(scaled_pixbuf)
            # Remove previous analytic data
            text_view = abuilder.get_object("lblFaceInfo")
            text_view.get_buffer().set_text("")
        else:
            PrintConsole("Preklicali ste izbiro slike")
            print("[INFO] Canceled open image")
        dialog.hide()

    def on_btnAnalyze_clicked(self, *a, **kv):
        path_label = abuilder.get_object("lblSelectedFile")
        if os.path.exists(path_label.get_text()):
            # Analyze image
            PrintConsole("Začenjamo analizo slike")
            demography = DeepFace.analyze(dialog.get_filename())
            print("[INFO] Image detection: {}".format(demography))
            # Print details
            text_view = abuilder.get_object("lblFaceInfo")
            text_view.get_buffer().set_text(json.dumps(demography[0], indent=4))
            PrintConsole("Analiza slike končana")
        else:
            PrintConsole("Izbrana slika ne obstaja")
            print("[ERROR] File path doesn't exists")

abuilder = Gtk.Builder()
# whatis(abuilder)
abuilder.add_from_file("Gui.glade")
abuilder.connect_signals(HandleSignals)

myForm = abuilder.get_object("Form1")
myForm.show()

Gtk.main()