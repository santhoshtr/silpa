#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import main



	


class HelloWorld:
    def toggle_editable(self, checkbutton, entry):
	if checkbutton.get_active():
		self.buttonb.show()
		print "check button activates"
	else:
		self.buttonb.hide()		
#	entry.set_editable(checkbutton.get_active())



    def file_ok_sel(self, w, entry):
        print "%s" % self.filew.get_filename()
	entry.set_text(self.filew.get_filename())
	self.filew.destroy()

    def enter_callback(self, widget, entry):
	entry_text = entry.get_text()
	print "Entry contents: %s\n" % entry_text

#    def make_box(self, homogeneous, spacing, expand, fill, padding):
#	box = gtk.HBox(homogeneous, spacing)
#	label = gtk.Label("Input File")
#	box.pack_start(label, expand, fill, padding)
#	label.show()
#	entry = self.entry_box()
#	box.pack_start(entry, True, True, 0)
#	return box

    def entry_box(self):
	self.entry = gtk.Entry()
	self.entry.set_max_length(50)
	self.entry.connect("activate", self.enter_callback, self.entry)
	self.entry.set_text("input file")
#	self.entry.insert_text(" world", len(self.entry.get_text()))
	self.entry.select_region(0, len(self.entry.get_text()))
#	vbox.pack_start(entry, True, True, 0)
	self.entry.show()
	return self.entry 

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit() 

    def destroy_filesel(self, widget, data=None):
	print "destroy file selection widget"
#	lambda w: self.filew.destroy()

    def trans(self, w):
	print "Tranliterating"
	ipfile = self.entry.get_text()
	output = self.entry1.get_text()
#	global fout
#	fout = open(self.entry1.get_text(), "wb")
	print self.entry1.get_text()
	flag = 1
	if self.check.get_active():
		flag = 0
	else:
		flag = 1
# send flag for check button ;)
	main.TranslateFile(ipfile, output, self.textbuffer, flag)
	out = open(output, 'rb')
	buffer = out.read()
	self.textbuffer.set_text(buffer)
#	if (self.i==0):
#		self.i=1
#		self.trans(w)

	self.sw.show()	
	self.textview.show()
	



    def file_sel(self, w):
	self.filew = gtk.FileSelection("File selection")
	self.filew.connect("destroy", self.destroy_filesel)
	self.filew.ok_button.connect("clicked", self.file_ok_sel,self.entry)
	self.filew.cancel_button.connect("clicked", lambda w: self.filew.destroy())
	self.filew.set_filename("input")
	self.filew.show()

    def file_sel_i(self, w):
	self.filew = gtk.FileSelection("File selection")
	self.filew.connect("destroy", self.destroy_filesel)
	self.filew.ok_button.connect("clicked", self.file_ok_sel, self.entry1)
	self.filew.cancel_button.connect("clicked", lambda w: self.filew.destroy())
	self.filew.set_filename("input")
	self.filew.show()

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)

	window.set_resizable(True)
    
        window.connect("delete_event", self.delete_event)
    
        window.connect("destroy", self.destroy)
    
        window.set_border_width(10)
	window.set_title("Tool by Pravin Satpute")


	box1 = gtk.VBox(False, 0)

	label = gtk.Label("Transliteration Tool")
	box1.pack_start(label, False, False, 0)
	label.show()
	separator = gtk.HSeparator()
	



	box1.pack_start(separator, False, True, 5)
	separator.show()
	label1 = gtk.Label("Input File/Word")
	label1.set_alignment(0, 0)
	box1.pack_start(label1, False, True, 5)
	label1.show()


	hbox = gtk.HBox(False, 0)

	entry = gtk.Entry()
	entry = self.entry_box()
	hbox.pack_start(entry, True, True, 0)

        self.check = gtk.CheckButton("File")
        box1.pack_start(self.check, False, False, 0)
        self.check.connect("toggled", self.toggle_editable, entry)
        self.check.set_active(False)
        self.check.show()

#	hbox = self.make_box(False, 0, False, False, 10)

	self.buttonb = gtk.Button("Browse")
	hbox.pack_start(self.buttonb, False, False, 10)
	self.buttonb.set_alignment(0, 0)
	self.buttonb.connect("clicked", self.file_sel)
#	self.buttonb.show()

	box1.pack_start(hbox, False, False, 0)
	hbox.show()

	label2 = gtk.Label("Select Output File")
	label2.set_alignment(0, 0)
	box1.pack_start(label2, False, True, 5)
	label2.show()


	hbox2 = gtk.HBox(False, 0)
	self.entry1 = gtk.Entry()
	self.entry1.set_max_length(50)
	self.entry1.connect("activate", self.enter_callback, self.entry)
	self.entry1.set_text("output")
	self.entry1.select_region(0, len(self.entry.get_text()))
#	self.entry1.set_editable()
#	vbox.pack_start(entry, True, True, 0)
	self.entry1.show()
	hbox2.pack_start(self.entry1, True, True, 0)
	button2 = gtk.Button("Browse")
	hbox2.pack_start(button2, False, False, 10)
	button2.set_alignment(0, 0)
	button2.connect("clicked", self.file_sel_i)
	button2.show()

	box1.pack_start(hbox2, False, False, 0)
	hbox2.show()




	hbox1 = gtk.HBox(False, 0)


	button = gtk.Button("Transliterate")
	hbox1.pack_start(button, False, True, 0)
	button.connect("clicked", self.trans)
#	button.set_alignment(0, 0)
	button.show()
	box1.pack_start(hbox1, False, False, 0)
	hbox1.show()

        box3 = gtk.VBox(False, 10)
        box3.set_border_width(10)
        box1.pack_start(box3, True, True, 0)
        box3.show()


	self.sw = gtk.ScrolledWindow()
	self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.textview = gtk.TextView()
	self.textbuffer = self.textview.get_buffer()
	infile = open("gui_output", "r")
	if infile:
		string = infile.read()
		infile.close()
		self.textbuffer.set_text(string)
	self.sw.add(self.textview)
#	self.sw.show()	
#	self.textview.show()	

	box3.pack_start(self.sw, True, True, 5)




	quitbox = gtk.HBox(True, 0)
	button = gtk.Button("Quit")
#	button.align("left")
	button.connect("clicked", lambda w: gtk.main_quit())
	quitbox.pack_start(button, True, True, 0)
	box1.pack_start(quitbox, False, False, 0)
	window.add(box1)
	button.show()
	quitbox.show()

	box1.show()
        window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
