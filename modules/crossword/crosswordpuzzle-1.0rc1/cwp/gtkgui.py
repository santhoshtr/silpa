"""
Crossword Puzzle - GTK GUI
Copyright 2008-2009  Peter Gebauer
Licensed under GNU GPLv3, see LICENSE or
visit http://www.gnu.org/copyleft/gpl.htmlfor more info.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import gtk
import gobject
import pango
import cairo
from cwp import *
from cwp.render import CairoRender

  

def format_time(t):
    """
    Returns a neatly formatted time with d:h:m:s as needed.
    """
    s = t % 60
    m = int(t / 60) % 60
    h = int(t / 3600) % 24
    d = int(t / 86400)
    if d > 0:
        return "%02dd %02dh %02d:%02d"%(d, h, m, s)
    if h > 0:
        return "%02dh %02d:%02d"%(h, m, s)
    if m > 0:
        return "%02d:%02d"%(m, s)
    if s > 0:
        return "%d"%s
    return ""
                   

def cairoColor(gdkColor, alpha = 1.0):
    """
    Transofmrs a gdk color to a cairo usable color.
    """
    return (gdkColor.red / float(0xffff), gdkColor.green / float(0xffff), gdkColor.blue / float(0xffff), alpha)

class CrosswordWindow(gtk.Window):
    """
    The main crossword window.
    """

    def __init__(self, config, editMode = True):
        gtk.Window.__init__(self)
        self._clipboard = gtk.Clipboard()
        self.config = config
        width, height = safeInt(config.get("window.width", 640)), safeInt(config.get("window.height", 480))
        if width < 320:
            width = 320
        if height < 240:
            height = 240
        self.resize(width, height)
        self._editMode = editMode
        self._changed = False
        self.game = Game()
        self._scoringClass = self.game.scoring.__class__
        self.board = CrosswordWidget(self.game.crossword)
        self.board.draw_missing_clues = safeBool(config.get("gui.draw_missing_clues", True))
        self.board.mirror_mode = safeBool(config.get("gui.mirror_mode")) and editMode
        self.filename = None
        self.vbox = gtk.VBox()
        self.add(self.vbox)
        # controls
        menubar = gtk.MenuBar()
        self.vbox.pack_start(menubar, False)
        frame = gtk.Frame("Completed")
        self.vbox.pack_start(frame, False)
        self.progressCompleted = gtk.ProgressBar()
        self.progressCompleted.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0, 0xffff))
        frame.add(self.progressCompleted)
        self.update_progress_completed()
        self.timeFrame = gtk.Frame("Time")
        self.vbox.pack_start(self.timeFrame, False)
        self.progressTime = gtk.ProgressBar()
        self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xffff, 0xffff, 0))
        self.progressTime.modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0, 0))
        self.timeFrame.add(self.progressTime)
        if self._editMode:
            self.labelLayer = gtk.Label()
            self.vbox.pack_start(self.labelLayer, False)
            self.labelLayer.set_property("xalign", 0.0)
        self.paned = gtk.HPaned()
        self.vbox.pack_start(self.paned)
        self.paned.set_position(safeInt(config.get("window.paned", -1)))
        # active clues
        self.labelActiveClues = gtk.Label()
        self.labelActiveClues.set_property("use-markup", True)
        self.labelActiveClues.set_property("xalign", 0.01)
        eventbox = gtk.EventBox()
        eventbox.add(self.labelActiveClues)
        eventbox.modify_bg(gtk.STATE_NORMAL, self.get_style().base[gtk.STATE_NORMAL])
        self.vbox.pack_start(eventbox, False, True, 8)
        self.board.connect("right-click", self.on_board_rightclick)
        self.board.connect("edited", self.on_board_edited)
        self.board.connect("cursor-moved", self.on_board_cursor_moved)
        self.paned.pack1(self.board, True, True)
        vbox = gtk.VBox()
        self.paned.pack2(vbox, False, True)
        self.hclues = gtk.TreeView(gtk.ListStore(str, int, int, int))
        self.hclues.set_enable_search(False)
        scrolledWindow = gtk.ScrolledWindow()
        scrolledWindow.add(self.hclues)
        self.hclues.connect("button-press-event", self.on_list_button_press)
        vbox.pack_start(scrolledWindow)
        self.hclues.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)
        col = gtk.TreeViewColumn("Across")
        self.hclues.append_column(col)
        cell = gtk.CellRendererText()
        cell.set_property("scale-set", True)
        cell.set_property("scale", 0.8)
        col.pack_start(cell)
        col.add_attribute(cell, "text", 0)
        self.update_hclues_list()
        self.vclues = gtk.TreeView(gtk.ListStore(str, int, int, int))
        self.vclues.set_enable_search(False)
        scrolledWindow = gtk.ScrolledWindow()
        scrolledWindow.add(self.vclues)
        self.vclues.connect("button-press-event", self.on_list_button_press)
        vbox.pack_start(scrolledWindow)
        self.vclues.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)
        col = gtk.TreeViewColumn("Down")
        self.vclues.append_column(col)
        cell = gtk.CellRendererText()
        cell.set_property("scale-set", True)
        cell.set_property("scale", 0.8)
        col.pack_start(cell)
        col.add_attribute(cell, "text", 0)
        self.update_vclues_list()
        # file menu
        accelgroup = gtk.AccelGroup()
        item = gtk.MenuItem("_File")
        menubar.append(item)
        menu = gtk.Menu()
        item.set_submenu(menu)
        menu.set_accel_group(accelgroup)
        self.add_accel_group(accelgroup)
        item = gtk.ImageMenuItem(gtk.STOCK_NEW)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("n"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_new_crossword)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("o"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_open)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("s"), gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_save_as)
        menu.append(item)
        item = gtk.ImageMenuItem(gtk.STOCK_SAVE)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("s"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_save)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.ImageMenuItem(gtk.STOCK_PRINT)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("p"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_print)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        item.connect("activate", self.on_open_preferences)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("q"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_quit)
        menu.append(item)
        # Edit menu
        item = gtk.MenuItem("_Edit")
        menubar.append(item)
        menu = gtk.Menu()
        item.set_submenu(menu)
        item = gtk.ImageMenuItem(gtk.STOCK_COPY)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("c"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_copy_selection)
        menu.append(item)
        item = gtk.ImageMenuItem(gtk.STOCK_CUT)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("x"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_cut_selection)
        menu.append(item)
        item = gtk.ImageMenuItem(gtk.STOCK_PASTE)
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("v"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_paste_selection)
        menu.append(item)
        if self._editMode:
            menu.append(gtk.MenuItem())
            item = gtk.ImageMenuItem(gtk.STOCK_PROPERTIES)
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("p"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_open_properties)
            menu.append(item)
            item = gtk.CheckMenuItem("Mirror mode")
            item.set_active(self.board.mirror_mode)
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("m"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_mirror_mode_toggle)
            menu.append(item)
        # View menu
        item = gtk.MenuItem("_View")
        menubar.append(item)
        menu = gtk.Menu()
        item.set_submenu(menu)
        item = gtk.CheckMenuItem("_Keep aspect ratio")
        self.board.maintainaspect = safeBool(self.config.get("gui.keep_aspect"), True)
        item.set_active(self.board.maintainaspect)
        item.connect("toggled", self.on_aspect_toggled)
        menu.append(item)
        item = gtk.CheckMenuItem("_Draw missing clues")
        item.set_active(self.board.draw_missing_clues)
        item.connect("toggled", self.on_draw_missing_clues_toggled)
        menu.append(item)
        # Game menu
        item = gtk.MenuItem("_Game")
        menubar.append(item)
        menu = gtk.Menu()
        item.set_submenu(menu)
        item = gtk.MenuItem("_New game")
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("g"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_new_game)
        menu.append(item)
        item = gtk.MenuItem("S_core")
        item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("r"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        item.connect("activate", self.on_score_game)
        menu.append(item)
        menu.append(gtk.MenuItem())
        item = gtk.MenuItem("Scoring")
        menu.append(item)
        menu = gtk.Menu()
        item.set_submenu(menu)
        group = None
        selected = u"%s"%self.config.get("scoring", u"")
        for index, scls in enumerate((ScoringSimple, ScoringTimeAttack, ScoringTournament)):
            item = gtk.RadioMenuItem(group, scls.name)
            if not group:
                group = item
                if not selected:
                    self._scoringClass = scls
                    item.set_active(True)
            if selected and scls.name == selected:
                self._scoringClass = scls
                item.set_active(True)
            item.connect("activate", self.on_change_scoring, scls)
            menu.append(item)
        self.game.scoring = self._scoringClass()
        if self._editMode:
            # Layer menu
            item = gtk.MenuItem("_Layer")
            menubar.append(item)
            self.layerMenu = gtk.Menu()
            item.set_submenu(self.layerMenu)
            self.update_layer_menu()
            # clues
            item = gtk.MenuItem("_Clues")
            menubar.append(item)
            menu = gtk.Menu()
            item.set_submenu(menu)            
            item = gtk.MenuItem("Add/Edit _horizontal clue")
            self.itemAddHClue = item
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("h"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_add_hclue)
            menu.append(item)
            item = gtk.MenuItem("Add/Edit _vertical clue")
            self.itemAddVClue = item
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("b"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_add_vclue)
            menu.append(item)
            menu.append(gtk.MenuItem())
            item = gtk.MenuItem("Remove horizontal clue")
            self.itemRemoveHClue = item
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("h"), gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_remove_hclue)
            menu.append(item)
            item = gtk.MenuItem("Remove vertical clue")
            self.itemRemoveVClue = item
            item.add_accelerator("activate", accelgroup, gtk.gdk.keyval_from_name("v"), gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
            item.connect("activate", self.on_remove_vclue)
            menu.append(item)
            menu.append(gtk.MenuItem())
            item = gtk.MenuItem("Remove all clues")
            item.connect("activate", self.on_remove_all_clues)
            menu.append(item)
            # popups
            self.popupMenu = gtk.Menu()
            menu = self.popupMenu
            item = gtk.MenuItem("Add/Edit _horizontal clue")
            item.connect("activate", self.on_add_hclue)
            menu.append(item)
            item = gtk.MenuItem("Add/Edit _vertical clue")
            item.connect("activate", self.on_add_vclue)
            menu.append(item)
            menu.append(gtk.MenuItem())
            item = gtk.MenuItem("Remove horizontal clue")
            item.connect("activate", self.on_remove_hclue)
            menu.append(item)
            item = gtk.MenuItem("Remove vertical clue")
            item.connect("activate", self.on_remove_vclue)
            menu.append(item)
            menu = gtk.Menu()
            self.listPopup = menu
            item = gtk.MenuItem("Edit clue")
            item.connect("activate", self.on_list_edit_clue)
            menu.append(item)
            menu.append(gtk.MenuItem())
            item = gtk.MenuItem("Remove clue")
            item.connect("activate", self.on_list_remove_clue)
            menu.append(item)
        # Final fixes
        self.update_title()
        self.update_active_clues(self.board.cursorx, self.board.cursory)
        self.update_time()
        self.set_changed(False)
        # signals
        self.connect("delete-event", self.on_delete)
        self.vbox.show_all()

    def run_properties_dialog(self, blank = False):
        dialog = PropertiesDialog(self, blank)
        if dialog.run() == gtk.RESPONSE_ACCEPT:
            self.game.crossword.width = dialog.swidth.get_value_as_int()
            self.game.crossword.height = dialog.sheight.get_value_as_int()
            self.game.crossword.title = dialog.etitle.get_text()
            self.game.crossword.author = dialog.eauthor.get_text()
            self.game.crossword.category = dialog.ecategory.get_text()
            self.game.crossword.alphabet = dialog.ealphabet.get_text()
            self.game.crossword.language = dialog.elanguage.get_text()
            self.game.crossword.minWordLength = dialog.sminwlength.get_value_as_int()
            self.game.crossword.normalize()
            self.set_changed(True)
            self.board.update_matrix_size_ratio()
            self.board.queue_draw()
            dialog.destroy()
            return True
        dialog.destroy()
        return False

    def run_score_dialog(self):
        self.game.stopGame()
        self.update_time_progress()
        dialog = gtk.Dialog("Score", self)
        vbox = dialog.get_child()
        comps = self.game.getScoreComponents()
        label = gtk.Label("Score using %s rules"%self.game.scoring.name)
        label.set_property("xalign", 0.0)
        vbox.pack_start(label)
        model = gtk.ListStore(self.game.scoring.type_, str, str)
        for comp in comps:
            model.append([comp[0] * comp[1], "%sx%s"%(comp[0], comp[1]), "%s"%comp[2]])
        tv = gtk.TreeView(model)
        column = gtk.TreeViewColumn("Score", gtk.CellRendererText())
        column.add_attribute(column.get_cell_renderers()[0], "text", 0)
        tv.append_column(column)
        column = gtk.TreeViewColumn("Calc.", gtk.CellRendererText())
        column.add_attribute(column.get_cell_renderers()[0], "text", 1)
        tv.append_column(column)
        column = gtk.TreeViewColumn("Description", gtk.CellRendererText())
        column.add_attribute(column.get_cell_renderers()[0], "text", 2)
        tv.append_column(column)
        tv.get_selection().set_mode(gtk.SELECTION_NONE)
        tv.set_enable_search(False)
        vbox.pack_start(tv)
        label = gtk.Label("<big><b>Final score:</b> %s</big>"%sum((c[0] * c[1] for c in comps)))
        label.set_property("xalign", 0.0)
        label.set_use_markup(True)
        vbox.pack_start(label)
        dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        dialog.set_default_response(gtk.RESPONSE_CLOSE)
        vbox.show_all()    
        dialog.run()
        dialog.destroy()

    def update_title(self):
        if self.filename:
            self.set_title("CrosswordPuzzle - %s"%self.filename)
        else:
            self.set_title("CrosswordPuzzle")

    def update_time_progress(self):
        t = self.game.getTime()
        if self.game.scoring.timelimit > 0:
            if t >= self.game.scoring.timelimit:
                self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xffff, 0x0000, 0x0000))
            elif t >= self.game.scoring.timelimit * 0.9:
                self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xffff, 0x8888, 0x0000))
            elif t >= self.game.scoring.timelimit * 0.5:
                self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xffff, 0xffff, 0x0000))
            else:
                self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0x0, 0xffff, 0x0000))
            fraction = t / self.game.scoring.timelimit
            self.progressTime.set_fraction(fraction <= 1.0 and fraction or fraction > 0.0 and 1.0 or 0.0)
        else:
            self.progressTime.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0x0, 0xffff, 0x0000))
            self.progressTime.set_fraction(0.0)

    def update_time(self):
        t = self.game.getTime()
        if self.game.scoring.timelimit > 0 and t >= self.game.scoring.timelimit:
            self.progressTime.set_text("%s / %s"%(format_time(t), format_time(self.game.scoring.timelimit)))
            self.run_score_dialog()
            return
        if self.game.scoring.timelimit > 0:
            self.progressTime.set_text("%s / %s"%(format_time(t), format_time(self.game.scoring.timelimit)))
        else:
            self.progressTime.set_text(format_time(t))
        if self.game.start > 0.0 and self.game.stop == 0.0:
            gobject.timeout_add(1000, self.update_time)                
        self.update_time_progress()

    def update_progress_completed(self):
        compl = self.board.get_completed()
        self.progressCompleted.set_fraction(compl)
        self.progressCompleted.set_text("%d%%"%int(compl * 100))

    def update_layer_menu(self):        
        if self._editMode:
            for child in self.layerMenu.get_children():
                self.layerMenu.remove(child)
                del child
            item = gtk.MenuItem("Clear layer")
            item.connect("activate", self.on_clear_layer)
            self.layerMenu.append(item)
            self.layerMenu.append(gtk.MenuItem())
            item = gtk.MenuItem("Add solution")
            item.connect("activate", self.on_add_solution_clicked)
            self.layerMenu.append(item)
            item = gtk.MenuItem("Remove solution")
            item.connect("activate", self.on_remove_solution_clicked)
            self.layerMenu.append(item)
            self.layerMenu.append(gtk.MenuItem())
            item = gtk.RadioMenuItem(None, "Player")
            item.set_active(self.board.editmatrix == -1)
            item.connect("toggled", self.on_select_layer, -1)
            item.set_draw_as_radio(True)
            group = item
            self.layerMenu.append(item)
            item = gtk.RadioMenuItem(group, "Black cells")
            item.set_active(self.board.editmatrix == -2)
            item.connect("toggled", self.on_select_layer, -2)
            self.layerMenu.append(item)
            for i in xrange(1, self.board.numsolutions + 1):
                item = gtk.RadioMenuItem(group, "Solution %d"%i)
                item.set_active(self.board.editmatrix == i - 1)
                item.connect("toggled", self.on_select_layer, i - 1)
                self.layerMenu.append(item)
            self.layerMenu.show_all()
            self.update_layer_label()

    def update_layer_label(self):
        if self._editMode:
            if self.board.editmatrix == -1:
                self.labelLayer.set_text("<b>Layer:</b> Player")
            elif self.board.editmatrix == -2:
                self.labelLayer.set_text("<b>Layer:</b> Black cells")
            elif self.board.editmatrix >= 0 and self.board.editmatrix < self.board.numsolutions:
                self.labelLayer.set_text("<b>Layer:</b> Solution %d"%(self.board.editmatrix + 1))
            self.labelLayer.set_use_markup(True)
        
    def update_hclues_list(self):
        h, v = self.board.get_clues().getIds()
        self._update_clues_list(self.hclues.get_model(), self.board.get_clues().iterHItems(), h)

    def update_vclues_list(self):
        h, v = self.board.get_clues().getIds()
        self._update_clues_list(self.vclues.get_model(), self.board.get_clues().iterVItems(), v)

    def update_clues_lists(self):
        self.update_hclues_list()
        self.update_vclues_list()

    def _update_clues_list(self, model, itemsiter, ids):
        model.clear()
        l = [(x, y, clue, ids[x, y]) for (x, y), clue in itemsiter]
        l.sort(lambda a, b: cmp(a[3], b[3]))
        for x, y, clue, id_ in l:
            model.append(["%d: %s"%(id_, clue), x, y, id_])

    def update_active_clues(self, x, y):
        hids, vids = self.board.get_clues().getIds()
        texts = []
        clues = self.board.get_clues()
        hclue = clues.getHClue(x, y)
        if hclue:
            ml = self.board.getLongestHorizontal(x, y)
            texts.append(u"<tt><b>[%d] %d across:</b></tt> %s"%(hids[x, y], ml, hclue))
        else:
            texts.append(u"")
        vclue = clues.getVClue(x, y)
        if vclue:
            ml = self.board.getLongestVertical(x, y)
            texts.append(u"<tt><b>[%d] %d down:  </b></tt> %s"%(vids[x, y], ml, vclue))
        else:
            texts.append(u"")
        self.labelActiveClues.set_text(u"\n".join(texts))
        self.labelActiveClues.set_property("use-markup", True)
        self.hclues.get_selection().unselect_all()
        for i, row in enumerate(self.hclues.get_model()):
            if row[1] == x and row[2] == y:
                self.hclues.get_selection().select_path("%s"%i)
                self.hclues.scroll_to_cell("%s"%i)
        self.vclues.get_selection().unselect_all()
        for i, row in enumerate(self.vclues.get_model()):
            if row[1] == x and row[2] == y:
                self.vclues.get_selection().select_path("%s"%i)
                self.vclues.scroll_to_cell("%s"%i)

    def save_crossword(self, filename):
        s = str(self.game)
        try:
            f = file(filename, "w")
            f.write(s)
            f.close()
            self.filename = filename
        except IOError, ioe:
            self.run_error_dialog("Error reading file", str(ioe))
            return False
        self.set_changed(False)
        self.update_title()
        return True

    def load_crossword(self, filename):
        try:
            f = file(filename)
            s = f.read()
            f.close()
        except IOError, ioe:
            self.run_error_dialog("Error reading file", str(ioe))
            return False
        self.filename = filename
        game = Game.loadFromString(s)
        self.game = game
        self.game.scoring = self._scoringClass()
        self.board.set_crossword(self.game.crossword)
        self.update_layer_menu()
        self.update_clues_lists()
        self.update_progress_completed()
        self.board.cursorpos = (0, 0)
        self.update_active_clues(self.board.cursorx, self.board.cursory)
        self.set_changed(False)
        self.update_title()
        return True

    def quit(self):
        if not self.has_changed() or self.run_yesno_dialog("Quit", "Quit even though your current changes will be lost?"):
            r = self.get_allocation()
            self.config["window.width"] = r.width
            self.config["window.height"] = r.height
            self.config["window.paned"] = self.paned.get_position()
            self.config["gui.draw_missing_clues"] = self.board.draw_missing_clues
            self.config["gui.keep_aspect"] = self.board.maintainaspect
            self.config["gui.mirror_mode"] = self.board.mirror_mode
            gtk.main_quit()
            return False
        return True

    def has_changed(self):
        return self._changed

    def set_changed(self, value):
        t = self.get_title()
        if value and not t.endswith(" *"):
            self.set_title("%s *"%t)
        elif not value and t.endswith(" *"):
            self.set_title(t[:-2])
        self._changed = value

    def run_error_dialog(self, title, text):
        dialog = gtk.Dialog(title, self)
        hbox = gtk.HBox()
        dialog.get_child().pack_start(hbox)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(image)
        hbox.pack_start(gtk.Label(text))
        dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        hbox.show_all()
        if dialog.run() == gtk.RESPONSE_CLOSE:
            dialog.destroy()
            return True
        dialog.destroy()
        return False

    def run_yesno_dialog(self, title, text):
        dialog = gtk.Dialog(title, self)
        hbox = gtk.HBox()
        dialog.get_child().pack_start(hbox)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(image)
        hbox.pack_start(gtk.Label(text))
        dialog.add_button(gtk.STOCK_NO, gtk.RESPONSE_REJECT)
        dialog.add_button(gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
        hbox.show_all()
        if dialog.run() == gtk.RESPONSE_ACCEPT:
            dialog.destroy()
            return True
        dialog.destroy()
        return False

    def run_input_dialog(self, title, text, oldContents = ""):
        dialog = gtk.Dialog(title, self)
        hbox = gtk.HBox()
        dialog.get_child().pack_start(hbox)
        hbox.pack_start(gtk.Label(text), False, False, 16)
        self.entry = gtk.Entry()
        self.entry.set_text(oldContents)
        self.entry.connect("activate", lambda o: dialog.response(gtk.RESPONSE_ACCEPT))
        hbox.pack_start(self.entry)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
        hbox.show_all()
        if dialog.run() == gtk.RESPONSE_ACCEPT:
            dialog.destroy()
            return self.entry.get_text()
        dialog.destroy()
        return None

    def update_remove_clues(self):
        if self._editMode:
            x, y = self.board.cursorx, self.board.cursory
            hclue = self.board.get_clues().getHClue(x, y)
            self.itemRemoveHClue.set_sensitive(bool(hclue))
            vclue = self.board.get_clues().getVClue(x, y)
            self.itemRemoveVClue.set_sensitive(bool(vclue))

    def update_clue_change(self):
        self.update_clues_lists()
        self.update_active_clues(self.board.cursorx, self.board.cursory)
        self.update_remove_clues()
        self.board.queue_draw()
        self.set_changed(True)

    def copy_to_clipboard(self, x, y, w, h):
        ret = []
        for yy in xrange(y, y + h):
            row = []
            for xx in xrange(x, x + w):
                if xx >= 0 and yy >= 0 and xx < self.board.width and yy < self.board.height:
                    row.append(self.board.read_matrix(xx, yy))
            ret.append(u"".join(row))
        self._clipboard.set_text(u"\n".join(ret))

    def paste_from_clipboard(self, x, y):
        txt = self._clipboard.wait_for_text()
        yy = y
        if txt:
            rows = txt.split(u"\n")
            for row in rows:
                xx = x
                for col in row:
                    if xx >= 0 and yy >= 0 and xx < self.board.width and yy < self.board.height:
                        self.board.write_matrix(xx, yy, col)
                    xx += 1
                yy += 1
            self.board.selection_unset()

    def clear_selection(self, x, y, w, h):
        if w > 0 or h > 0:
            for yy in xrange(y, y + h):
                for xx in xrange(x, x + w):
                    self.board.write_matrix(xx, yy, u" ")
            self.board.selection_unset()
                
    #
    # Callbacks
    #

    def on_print(self, widget):
        op = gtk.PrintOperation()
        op.set_show_progress(True)
        op.set_n_pages(1)
        op.set_use_full_page(False)
        op.connect("draw-page", self.on_draw_page)
        op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, self)

    def on_draw_page(self, widget, pctx, nr):
        black = (0.0, 0.0, 0.0, 1.0)
        white = (1.0, 1.0, 1.0, 1.0)
        render = CairoRender(pctx.get_cairo_context(), self.board.width, self.board.height, pctx.get_width(), pctx.get_height(), True)
        middle = pctx.get_width() * 0.5
        render.offsetx = middle
        title = self.board._crossword.title or ""
        render.context.set_font_size(16)
        tx, ty, tw, th, tdx, tdy = render.context.text_extents(title or "")
        y = th
        render.context.move_to(pctx.get_width() * 0.5 - tw * 0.5, y)
        render.context.show_text(title or "")
        y += th
        if self.board._crossword.author:
            author = "(%s)"%self.board._crossword.author
        else:
            author = ""
        render.context.set_font_size(10)
        tx, ty, tw, th, tdx, tdy = render.context.text_extents(author or "")
        render.context.move_to(pctx.get_width() * 0.5 - tw * 0.5, y)
        y += th
        render.context.show_text(author or "")
        render.context.stroke()
        render.context.translate(0, y)
        render.context.scale(0.5, 0.5)
        render.draw_grid()
        render.draw_matrix(self.board.get_editable_matrix(), black, -1)
        render.draw_matrix(self.board._crossword.blackMatrix, black, 1)
        hids, vids = self.board._crossword.clues.getIds()
        hids.update(vids)
        render.draw_clue_ids(hids, black, white)
        render.context.translate(0, pctx.get_height() * 0.85)
        render.width = pctx.get_width() * 2
        render.draw_clues(self.board._crossword, 0, 0, black)

    def on_quit(self, widget):        
        return self.quit()

    def on_delete(self, widget, event):
        return self.quit()

    def on_draw_missing_clues_toggled(self, widget):
        self.board.set_draw_missing_clues(widget.get_active())

    def on_aspect_toggled(self, widget):
        self.board.set_maintain_aspect(widget.get_active())

    def on_add_solution_clicked(self, widget):
        self.board.add_solution_matrix()
        self.board.editmatrix = self.board.numsolutions - 1
        self.update_layer_menu()

    def on_remove_solution_clicked(self, widget):
        if self.board.editmatrix >= 0 and self.board.editmatrix < self.board.numsolutions:
            self.board.remove_solution_matrix(self.board.editmatrix)
        self.update_layer_menu()

    def on_select_layer(self, widget, index):
        self.board.editmatrix = index
        self.board.grab_focus()
        self.board.normalize()
        self.update_layer_label()

    def on_save(self, widget):
        if self.filename:
            self.save_crossword(self.filename)
        else:
            self.on_save_as(widget)
    
    def on_save_as(self, widget):
        dialog = gtk.FileChooserDialog("Save crossword puzzle as...", self, gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE_AS, gtk.RESPONSE_ACCEPT))
        f = gtk.FileFilter()
        f.set_name("Crossword Puzzles")
        f.add_pattern("*.cwp")
        dialog.add_filter(f)
        while dialog.run() == gtk.RESPONSE_ACCEPT:
            if self.save_crossword(dialog.get_filename()):
                self.filename = dialog.get_filename()
                break
        dialog.destroy()


    def on_open(self, widget):
        dialog = gtk.FileChooserDialog("Open crossword puzzle as...", self, gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT))
        f = gtk.FileFilter()
        f.set_name("Crossword Puzzles")
        f.add_pattern("*.cwp")
        dialog.add_filter(f)
        while dialog.run() == gtk.RESPONSE_ACCEPT:
            if self.load_crossword(dialog.get_filename()):
                break
        dialog.destroy()

    def on_board_edited(self, widget, x, y, letter):
        self.update_progress_completed()
        self.set_changed(True)

    def on_board_cursor_moved(self, widget, x, y):
        self.update_active_clues(x, y)
        self.update_remove_clues()

    def on_clear_layer(self, widget, onlyLetters = False):
        layernames = ["Black cells", "Player"] + ["Solution %d"%i for i in xrange(1, self.board.numsolutions + 1)]
        name = layernames[self.board.editmatrix + 2]
        if self.run_yesno_dialog("Clear layer: %s"%name, "Are you sure you want to clear layer the layer named \"%s\"?"%name):
            if self.board.editmatrix == -1:
                self.board.clearPlayerLayer(onlyLetters)
            elif self.board.editmatrix == -2:
                self.board.clearBlackLayer()
            elif self.board.editmatrix >= 0:
                self.board.clearSolutionLayer(self.board.editmatrix, onlyLetters)

    def on_new_crossword(self, widget):
        if self.has_changed() and not self.run_yesno_dialog("New crossword", "Your current work will be lost, are you sure?"):
            return
        if self.run_properties_dialog(True):
            self.filename = None
            self.game = Game()
            self.board.set_crossword(self.game.crossword)
            self.board.cursorpos = (0, 0)
            self.set_changed(False)
            self.update_title()
            self.update_hclues_list()
            self.update_vclues_list()

    def on_new_game(self, widget):
        if self.has_changed() and self.game.stop == 0.0:
            if not self.run_yesno_dialog("New game", "Your current game will be lost, are you sure?"):
                return
        self.game.startGame()
        self.board.clearPlayerLayer()
        self.update_time()
        self.on_select_layer(widget, -1)
        self.update_layer_menu()

    def on_score_game(self, widget):
        self.run_score_dialog()
        self.update_time()

    def on_add_hclue(self, widget):
        self.edit_hclue(self.board.cursorx, self.board.cursory)
        
    def edit_hclue(self, x, y):
        l = self.board.getLongestHorizontal(x, y)
        if l == 0:
            self.run_error_dialog("Invalid clue position", "Clues cannot start inside black cells.")
            return
        clue = self.game.crossword.clues.getHClue(x, y)
        t = self.run_input_dialog("Add/Edit horizontal clue", "[%02d:%02d] %d across"%(x, y, l), clue or "")
        if t is None:
            return
        self.game.crossword.clues.setHClue(x, y, t)
        self.update_clue_change()
        self.set_changed(True)
        self.board.queue_draw()

    def on_add_vclue(self, widget):
        self.edit_vclue(self.board.cursorx, self.board.cursory)

    def edit_vclue(self, x, y):
        l = self.board.getLongestVertical(x, y)
        if l == 0:
            self.run_error_dialog("Invalid clue position", "Clues cannot start inside black cells.")
            return
        clue = self.game.crossword.clues.getVClue(x, y)
        t = self.run_input_dialog("Add/Edit vertical clue", "[%02d:%02d] %d down"%(x, y, l), clue or "")
        if t is None:
            return
        self.game.crossword.clues.setVClue(x, y, t)
        self.update_clue_change()
        self.set_changed(True)
        self.board.queue_draw()

    def on_remove_hclue(self, widget):
        self.remove_hclue(self.board.cursorx, self.board.cursory)

    def remove_hclue(self, x, y):
        clues = self.board.get_clues()
        clues.delHClue(x, y)
        self.update_clue_change()
        self.set_changed(True)
        self.board.queue_draw()

    def on_remove_vclue(self, widget):
        self.remove_vclue(self.board.cursorx, self.board.cursory)

    def remove_vclue(self, x, y):
        clues = self.board.get_clues()
        clues.delVClue(x, y)
        self.update_clue_change()
        self.set_changed(True)
        self.board.queue_draw()

    def on_remove_all_clues(self, widget):
        if len(self.board.get_clues()) > 0:
            if self.run_yesno_dialog("Remove all clues", "Are you sure you want to remove all clues?"):
                self.board.new_clues()
                self.update_clue_change()

    def on_copy_selection(self, widget):
        sel = self.board.get_selection()
        if sel.width > 0 or sel.height > 0:
            self.copy_to_clipboard(*sel)

    def on_cut_selection(self, widget):
        sel = self.board.get_selection()
        if sel.width > 0 or sel.height > 0:
            self.copy_to_clipboard(*sel)
            self.clear_selection(*sel)
        
    def on_paste_selection(self, widget):
        self.paste_from_clipboard(self.board.cursorx, self.board.cursory)

    def on_open_properties(self, widget):
        self.run_properties_dialog()

    def on_open_preferences(self, widget):
        self.run_error_dialog("Not implemented", "Ooops! CrosswordPuzzle doesn't have any preferences yet.")

    def on_change_scoring(self, widget, scoringClass):
        self.game.scoring = scoringClass()
    
    def on_mirror_mode_toggle(self, widget):
        self.board.set_mirror_mode(widget.get_active())

    def on_board_rightclick(self, widget, event):
        if self._editMode:
            self.popupMenu.show_all()
            self.popupMenu.popup(None, None, None, 3, event.time)

    def on_list_rightclick(self, widget, event):
        if self._editMode:
            if self.hclues.is_focus():
                model = self.hclues.get_model()
            elif self.vclues.is_focus():
                model = self.vclues.get_model()
            else:
                model = None
            if model and len(model) > 0:
                self.listPopup.show_all()
                self.listPopup.popup(None, None, None, 3, event.time)

    def on_list_edit_clue(self, widget):
        if self.hclues.is_focus():
            selected = self.hclues.get_selection().get_selected()
            func = self.edit_hclue
        elif self.vclues.is_focus():
            selected = self.vclues.get_selection().get_selected()
            func = self.edit_vclue
        else:
            selected = None
        if selected:
            model, it = selected
            if len(model) > 0:
                func(model[it][1], model[it][2])
            
    def on_list_remove_clue(self, widget):
        if self.hclues.is_focus():
            selected = self.hclues.get_selection().get_selected()
            func = self.remove_hclue
        elif self.vclues.is_focus():
            selected = self.vclues.get_selection().get_selected()
            func = self.remove_vclue
        else:
            selected = None
        if selected:
            model, it = selected
            if len(model) > 0:
                func(model[it][1], model[it][2])

    def on_list_button_press(self, widget, event):
        if event.button == 3:
            selected = widget.get_selection().get_selected()
            if selected:
                self.on_list_rightclick(widget, event)
            


class CrosswordPuzzle(object):

    def __init__(self, config = {}, editmode = False):
        self.config = config
        self.window = CrosswordWindow(self.config, editmode)
        self.window.show()

    def run(self):
        gtk.main()


class CrosswordWidget(gtk.DrawingArea):
    EDIT_PLAYER_MATRIX = -1
    EDIT_BLACK_MATRIX = -2
    
    def __init__(self, crossword = None, **kwargs):
        gtk.DrawingArea.__init__(self)
        self._readonly = kwargs.get("readonly", False)
        self._maintainAspect = kwargs.get("maintainAspect", True)
        self._drawClues = kwargs.get("drawClues", True)
        self._editMatrix = kwargs.get("editMatrix", -1)
        self._drawMissingClues = kwargs.get("drawMissingClues", True)
        self._mirrorMode = kwargs.get("mirrorMode", True)
        self._cursorx = 0
        self._cursory = 0
        self._selectionStart = None
        self._cursorColor = kwargs.get("cursorColors", gtk.gdk.Color(0x0, 0x0, 0xffff))
        self._crossword = crossword or Crossword()
        self.set_flags(gtk.CAN_FOCUS)
        self.update_matrix_size_ratio()
        self.set_size_request(256, 256)
        self.connect("configure-event", self.on_configure)
        self.connect("expose-event", self.on_expose)
        self.connect("key-press-event", self.on_keypress)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.connect("button-press-event", self.on_button_pressed)
        self.connect("button-release-event", self.on_button_released)
        self.connect("motion-notify-event", self.on_mouse_motion)
        self.cursorpos = 0, 0
        self._selection = gtk.gdk.Rectangle(0, 0, 0, 0)

    #
    # Internal mumbo jumbo
    #

    def update_selection_from_mouse(self, x, y):
        if self._selectionStart:
            sx, sy = int(self._selectionStart[0] / self._uw), int(self._selectionStart[1] / self._uh)
            ex, ey = int(x / self._uw), int(y / self._uh)
            if sx < ex:
                x = sx
                w = ex - sx
            else:
                x = ex
                w = sx - ex
            if sy < ey:
                y = sy
                h = ey - sy
            else:
                y = ey
                h = sy - ey
            self.set_selection(x, y, w + 1, h + 1)

    def selection_unset(self):
        self.set_selection(0, 0, 0, 0)

    def get_translated_selection(self):
        sel = self.get_selection()
        if sel:
            return int(sel.x * self._uw), int(sel.y * self._uh), int(sel.width * self._uw), int(sel.height * self._uh)
        return None
            
    def get_selection(self):
        if self._selection.width != 0 or self._selection.height == 0:
            return self._selection
        return None

    def set_selection(self, x, y, w, h):
        self.set_selection_position(x, y)
        self.set_selection_size(w, h)
        x, y, w, h = self._selection.x, self._selection.y, self._selection.width, self._selection.height
        ox, oy = self.offsets
        self.queue_draw_area(ox + int(x * self._uw - self._uw), oy + int(y * self._uh - self._uh),
                             int(w * self._uw + self._uw * 2), int(h * self._uh + self._uh * 2))

    def set_selection_size(self, w, h):
        if w < 0:
            w = 0
        elif w + self._selection.x >= self._crossword.width:
            self.w = self._crossword.width - self._selection.x
        if h < 0:
            h = 0
        elif h + self._selection.y >= self._crossword.height:
            h = self._crossword.height - self._selection.y
        self._selection.width = w
        self._selection.height = h

    def set_selection_position(self, x, y):
        if x < 0:
            x = 0
        elif x >= self._crossword.width:
            x = self._crossword.width - 1
        if y < 0:
            y = 0
        elif y >= self._crossword.height:
            y = self._crossword.height - 1
        self._selection.x = x
        self._selection.y = y

    def get_editable_matrix(self):
        """
        Returns the editable matrix. Don't change the matrix directly,
        use the write_matrix and read_matrix methods instead.
        """
        if self.editmatrix == -1:
            return self._crossword.playerMatrix
        if self.editmatrix == -2:
            return self._crossword.blackMatrix
        if self.editmatrix >= self.numsolutions:
            self.editmatrix = self.numsolutions - 1
        return self._crossword.solutionMatrices[self.editmatrix]

    def update_matrix_size_ratio(self):
        rect = self.get_allocation()
        if self.maintainaspect:
            uw = rect.width / float(self.width)
            uh = rect.height / float(self.height)
            if uw < uh:
                uh = uw                
            elif uw > uh:
                uw = uh
        else:
            uw = rect.width / float(self.width)
            uh = rect.height / float(self.height)
        self._uw = uw
        self._uh = uh

    #
    # Public methods and attributes
    #

    def get_mirror_mode(self):
        return self._mirrorMode

    def set_mirror_mode(self, value):
        self._mirrorMode = value

    mirror_mode = property(get_mirror_mode, set_mirror_mode)

    def redraw_cursor(self):
        ox, oy = self.offsets
        self.queue_draw_area(ox + int(self.cursorx * self._uw), oy + int(self.cursory * self._uh), ox + int(self._uw), oy + int(self._uh))

    def clearPlayerLayer(self, onlyLetters = False):
        if onlyLetters:
            self._crossword.playerMatrix.clearLetters()
        else:
            self._crossword.playerMatrix.clear()
        self.emit("edited", 0, 0, None)
        self.queue_draw()

    def clearBlackLayer(self):
        self._crossword.blackMatrix.clear()
        self.emit("edited", 0, 0, None)
        self.queue_draw()

    def clearSolutionLayer(self, index, onlyLetters = False):
        if index >= 0 and index < self.numsolutions:
            matrix = self._crossword.solutionMatrices[index]
            if onlyLetters:
                matrix.clearLetters()
            else:
                matrix.clear()
        self.emit("edited", 0, 0, None)
        self.queue_draw()

    def get_crossword(self):
        return self._crossword

    def set_crossword(self, crossword):
        self._crossword = crossword
        self.update_matrix_size_ratio()
        self.queue_draw()

    def getLongestHorizontal(self, x, y):
        return self._crossword.blackMatrix.getMaxHLength(x, y, 1)

    def getLongestVertical(self, x, y):
        return self._crossword.blackMatrix.getMaxVLength(x, y, 1)

    def get_clues(self):
        return self._crossword.clues

    def new_clues(self):
        self._crossword.clues = CluesSheet()
        self.emit("edited", 0, 0, None)

    def set_clues(self, cluessheet):
        self._crossword.clues = cluessheet

    def get_completed(self):
        total = self._crossword.width * self._crossword.height
        available = len(self._crossword.blackMatrix.getEmptyCells())
        player = len(self._crossword.playerMatrix.getFullCells())
        if available == 0:
            return 0.0
        return player / float(available)

    def normalize(self):
        self._crossword.normalize()

    def add_solution_matrix(self):
        self._crossword.solutionMatrices.append(Matrix(self.width, self.height))
        self._crossword.normalize()

    def remove_solution_matrix(self, i):
        if i >= 0 and i < self.numsolutions:
            del self._crossword.solutionMatrices[i]
        self._editMatrix -= 1
        self.queue_draw()

    def get_maintain_aspect(self):
        return self._maintainAspect

    def set_maintain_aspect(self, value):
        self._maintainAspect = value
        self.update_matrix_size_ratio()
        self.queue_draw()

    maintainaspect = property(get_maintain_aspect, set_maintain_aspect)

    def resize_matrix(self, w, h):
        """
        Resizes the matrix. Valid dimensions must be in the range 4 to 128.
        """
        if w < 4 or w > 128 or h < 4 or h > 128:
            raise ValueError("matrix dimensions must be in the range of 4-128")
        self._crossword.playerMatrix.width = w
        self._crossword.playerMatrix.height = h
        self._crossword.normalize()
        self.update_matrix_size_ratio()
        self.queue_draw()

    def get_num_solutions(self):
        return len(self._crossword.solutionMatrices)

    def set_num_solutions(self, i):
        oldeditmatrix = self.editmatrix
        if i < self.numsolutions:
            self._crossword.solutionMatrices = self._crossword.solutionMatrices[:i]
        elif i > self.numsolutions:
            self._crossword.solutionMatrices += [Grid(self.width, self.height) for i in xrange(i - self.numsolutions)]
            self._crossword.normalizeSolutions()
        if oldeditmatrix != self.editmatrix:
            self.queue_draw()

    numsolutions = property(get_num_solutions, set_num_solutions)

    def set_readonly(self, value):
        """
        Set True to make the crossword read-only. It can still be sensitive,
        but no input can be written.
        """
        self._readonly = value
        self.queue_draw()

    def get_readonly(self):
        return self._readonly

    readonly = property(get_readonly, set_readonly)

    def set_edit_matrix(self, value):
        """
        Select which matrix to edit.
        -1 means the player matrix, then it's the index of the alternative
        matrices found in the self.crossword.solutionMatrices list.
        """
        if value >= self.numsolutions or value < -2:
            raise ValueError("no matrix index %d"%value)
        self._editMatrix = value
        self._crossword.normalize()
        self.cursorx = self.cursorx
        self.cursory = self.cursory
        self.queue_draw()

    def get_edit_matrix(self):
        if self._editMatrix >= self.numsolutions:
            self.editmatrix = self.numsolutions - 1
            self.queue_draw()
        return self._editMatrix

    editmatrix = property(get_edit_matrix, set_edit_matrix)

    def set_cursor_x(self, x):
        """
        Update the cursor's horizontal position.
        """
        w = self.width
        oldx = self.cursorx
        direction = self.cursorx < x and 1 or -1
        if x < 0:
            x = w - 1
        elif x >= w:
            x = 0
        tries = 0
        while self.editmatrix == self.EDIT_PLAYER_MATRIX and self.read_matrix(x, self.cursory) == u"#" and tries < 2:
            x += direction
            if x < 0:
                x = w - 1
                tries += 1
            elif x >= w:
                x = 0
                tries += 1
        self._cursorx = x
        if oldx != x:
            self.emit("cursor-moved", x, self.cursory)
            ox, oy = self.offsets
            self.queue_draw_area(ox + int(oldx * self._uw), oy + int(self.cursory * self._uh),
                                 ox + int(self._uw), oy + int(self._uh))
            self.queue_draw_area(ox + int(self.cursorx * self._uw), oy + int(self.cursory * self._uh),
                                 ox + int(self._uw), oy + int(self._uh))

    def get_cursor_x(self):
        return self._cursorx

    cursorx = property(get_cursor_x, set_cursor_x)

    def set_cursor_y(self, y):
        """
        Update the cursor's vertical position.
        """
        h = self.height
        oldy = self.cursory
        direction = self.cursory < y and 1 or -1
        if y < 0:
            y = h - 1
        elif y >= h:
            y = 0
        tries = 0
        while self.editmatrix == self.EDIT_PLAYER_MATRIX and self.read_matrix(self.cursorx, y) == u"#" and tries < 2:
            y += direction
            if y < 0:
                y = h - 1
                tries += 1
            elif y >= h:
                y= 0
                tries += 1
        self._cursory = y
        if oldy != y:
            self.emit("cursor-moved", self.cursorx, y)
            ox, oy = self.offsets
            self.queue_draw_area(ox + int(self.cursorx * self._uw), oy + int(oldy * self._uh),
                                 ox + int(self._uw + 1), oy + int(self._uh + 1))
            self.queue_draw_area(ox + int(self.cursorx * self._uw), oy + int(self.cursory * self._uh),
                                 ox + int(self._uw + 1), oy + int(self._uh + 1))

    def get_cursor_y(self):
        return self._cursory

    cursory = property(get_cursor_y, set_cursor_y)

    def set_cursor_pos(self, x, y = None):
        """
        Update cursor position.
        """
        if y is None:
            x, y = x
        self.set_cursor_x(x)
        self.set_cursor_y(y)

    def get_cursor_pos(self):
        return self.cursorx, self.cursory

    cursorpos = property(get_cursor_pos, set_cursor_pos)

    def get_state(self):
        """
        For some reason there's no way to get a state from a widget.
        You have to figure it out yourself based on other flags.
        """
        if self.props.sensitive:
            return gtk.STATE_NORMAL
        return gtk.STATE_INSENSITIVE

    state = property(get_state)

    def get_width(self):
        return self._crossword.playerMatrix.width

    def set_width(self, w):
        self.resize_matrix(w, self.height)

    width = property(get_width, set_width)

    def get_height(self):
        return self._crossword.playerMatrix.height

    def set_height(self, h):
        self.resize_matrix(self.width, h)

    height = property(get_height, set_height)

    def get_draw_missing_clues(self):
        return self._drawMissingClues

    def set_draw_missing_clues(self, value):
        self._drawMissingClues = value
        self.queue_draw()

    draw_missing_clues = property(get_draw_missing_clues, set_draw_missing_clues)

    def write_matrix(self, x, y, letter):
        """
        Puts a letter into the editable matrix if possible.
        Raises ValueError if readonly and IndexError if the position
        is outside the matrix dimensions.
        """
        if self.readonly:
            raise ValueError("crossword is readonly")
        if letter == "#":
            if self.editmatrix != self.EDIT_PLAYER_MATRIX:
                matrix = self._crossword.blackMatrix
            else:
                letter = " "
                matrix = self.get_editable_matrix()
        else:
            if self.editmatrix == self.EDIT_BLACK_MATRIX and not letter in "# ":
                letter = "#"
            matrix = self.get_editable_matrix()
        if x < 0 or x >= matrix.width or y < 0 or y >= matrix.height:
            raise IndexError("matrix position out of range")
        if letter != "#" and self.editmatrix >= 0:
            self._crossword.blackMatrix[self.cursorx, self.cursory] = u" "
        letter = (u"%s"%letter)[0].upper()
        matrix[x, y] = letter
        if self.mirror_mode and self.editmatrix != -1:
            newy = self._crossword.height - y - 1
            newx = self._crossword.width - x - 1
            matrix[newx, newy] = letter
        ox, oy = self.offsets
        #self.queue_draw_area(ox + int(x * self._uw), oy + int(y * self._uh), ox + int(self._uw), oy + int(self._uh))
        self.queue_draw()
        self.emit("edited", x, y, letter)

    def read_matrix(self, x, y):
        """
        Reads a letter from the editable matrix if possible.
        Raises ValueError if readonly and IndexError if the position
        is outside the matrix dimensions.
        """
        matrix = self.get_editable_matrix()
        if x < 0 or x >= matrix.width or y < 0 or y >= matrix.height:
            raise IndexError("matrix position out of range")
        black = bool(self._crossword.blackMatrix[x, y] == u"#")
        if black:
            return u"#"
        l = matrix[x, y]
        if not l:
            l = u" "
        return (u"%s"%l)[0].upper()

    def get_offsets(self):
        if self._drawClues:
            return 0, 0
        rect = self.get_allocation()
        if rect.width < rect.height:
            return 0, int(rect.height * 0.5) - int(rect.width * 0.5)
        return int(rect.width * 0.5) - int(rect.height * 0.5), 0

    offsets = property(get_offsets)

    def set_cursor_from_world(self, x, y):
        ox, oy = self.offsets
        xx, yy = int((x - ox) / self._uw), int((y - oy) / self._uh)
        self.cursorpos = xx, yy
        

    #
    # Callbacks
    #

    def on_configure(self, widget, event):
        self.update_matrix_size_ratio()

    def on_expose(self, widget, event):
        rect = self.get_allocation()
        ox, oy = self.offsets
        render = CairoRender(widget.window.cairo_create(), self.width, self.height, rect.width, rect.height,
                             self.maintainaspect, readonly = self.readonly,
                             offsetx = ox, offsety = oy)
        render.clip()
        render.draw_background(cairoColor(self.get_style().base[self.get_state()]))
        if self._drawMissingClues:
            render.draw_missing_clues(self._crossword, (1.0, 0.75, 0.75, 1.0))
        if self._selection.width > 0 and self._selection.height > 0:
            selection = self._selection.x, self._selection.y, self._selection.width, self._selection.height
            sx, sy, sw, sh = selection
            render.draw_selection(sx, sy, sw, sh, cairoColor(self.get_style().text[self.get_state()]))
        render.draw_grid(cairoColor(self.get_style().text[self.get_state()]))
        render.draw_matrix(self.get_editable_matrix(), cairoColor(self.get_style().text[self.get_state()]), -1)
        render.draw_matrix(self._crossword.blackMatrix, cairoColor(self.get_style().text[self.get_state()]), 1)
        hids, vids = self._crossword.clues.getIds()
        hids.update(vids)
        render.draw_clue_ids(hids,
                             cairoColor(self.get_style().text[self.get_state()]),
                             cairoColor(self.get_style().base[self.get_state()]))
        if self.props.sensitive:
            if self.is_focus():
                render.draw_focus_border(cairoColor(self.get_style().fg[self.get_state()]))
                fg = (0.0, 1.0, 0.0, 0.5)
                r, g, b = (0.0, 0.5, 0.0)
            else:
                fg = cairoColor(self.get_style().dark[self.get_state()])
                r, g, b, a = cairoColor(self.get_style().dark[self.get_state()])
            render.draw_cursor(self.cursorx, self.cursory, fg, (r, g, b, 0.3))
        if self._drawClues:
            render.draw_clues(self._crossword, self.width * self._uw + 8, 0, cairoColor(self.get_style().text[self.get_state()]))

    def on_keypress(self, widget, event):
        """
        Our own key handling routines.
        """
        kvn = gtk.gdk.keyval_name(event.keyval).upper()
        if kvn == "LEFT":
            self.cursorx -= 1
            return True
        elif kvn == "RIGHT":
            self.cursorx += 1
            return True
        elif kvn == "UP":
            self.cursory -= 1
            return True
        elif kvn == "DOWN":
            self.cursory += 1
            return True
        elif kvn == "DELETE":
            self.write_matrix(self.cursorx, self.cursory, u" ")
            return True        
        elif kvn == "BACKSPACE":
            if event.state & gtk.gdk.SHIFT_MASK:
                self.cursory -= 1
            else:
                self.cursorx -= 1
            self.write_matrix(self.cursorx, self.cursory, u" ")
            return True        
        elif kvn == "SPACE":
            self.write_matrix(self.cursorx, self.cursory, u" ")
            if event.state & gtk.gdk.SHIFT_MASK:
                self.cursory += 1
            else:
                self.cursorx += 1
            return True        
        elif not self.readonly:
            k = event.string.upper().strip()
            if k and k in self._crossword.alphabet + "#":
                self.write_matrix(self.cursorx, self.cursory, u"%s"%k)
                if k != "#":
                    if event.state & gtk.gdk.SHIFT_MASK:
                        self.cursory += 1
                    else:
                        self.cursorx += 1
                return True
        return False

    def on_button_pressed(self, widget, event):
        ox, oy = self.offsets
        if event.button == 1:
            if event.x >= ox and event.y >= oy and event.x < ox + self.width * self._uw and event.y < oy + self.height * self._uh:
                if not self._selectionStart and self.get_selection():
                    self.selection_unset()
                    self.queue_draw()
                self._selectionStart = (event.x - ox, event.y - oy)
                if not self.is_focus():
                    self.grab_focus()
                else:
                    self.set_cursor_from_world(event.x, event.y)
                return True
        elif event.button == 3:
            if event.x >= ox and event.y >= oy and event.x < ox + self.width * self._uw and event.y < oy + self.height * self._uh:
                self.set_cursor_from_world(event.x, event.y)
                self.emit("right-click", event)
                return True
        return False

    def on_button_released(self, widget, event):
        if event.button == 1:
            if self._selectionStart:
                sx, sy = self._selectionStart
                ox, oy = self.offsets
                ex, ey = event.x - ox, event.y - oy
                self._selectionStart = None
                if abs(sx - ex) > 4 or abs(sy - ey) > 4:
                    self.update_selection_from_mouse(event.x - ox, event.y - oy)
                    self.queue_draw()
                else:
                    self.selection_unset()
        return False

    def on_mouse_motion(self, widget, event):
        if self._selectionStart:
            ox, oy = self.offsets
            self.update_selection_from_mouse(event.x - ox, event.y - oy)


class PropertiesDialog(gtk.Dialog):

    def __init__(self, parent, blank = False):
        gtk.Dialog.__init__(self, "Properties", parent)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
        self.set_default_response(gtk.RESPONSE_CANCEL)
        vbox = self.get_child()
        table = gtk.Table(9, 2)
        table.set_row_spacings(4)
        table.set_col_spacings(32)
        table.attach(gtk.Label("Width"), 0, 1, 0, 1, 0, 0)
        table.attach(gtk.Label("Height"), 0, 1, 1, 2, 0, 0)
        table.attach(gtk.Label("Title"), 0, 1, 2, 3, 0, 0)
        table.attach(gtk.Label("Author"), 0, 1, 3, 4, 0, 0)
        table.attach(gtk.Label("Category"), 0, 1, 4, 5, 0, 0)
        table.attach(gtk.Label("Alphabet"), 0, 1, 5, 6, 0, 0)
        table.attach(gtk.Label("Language"), 0, 1, 6, 7, 0, 0)
        table.attach(gtk.Label("Minimum word length"), 0, 1, 7, 8, 0, 0)
        self.swidth = gtk.SpinButton()
        self.swidth.set_range(3, 128)
        self.swidth.set_increments(1, 1)
        self.swidth.set_value(blank and 15 or parent.game.crossword.width)
        table.attach(self.swidth, 1, 2, 0, 1, gtk.FILL | gtk.EXPAND)        
        self.sheight = gtk.SpinButton()
        self.sheight.set_range(3, 128)
        self.sheight.set_increments(1, 1)
        self.sheight.set_value(blank and 15 or parent.game.crossword.height)
        table.attach(self.sheight, 1, 2, 1, 2, gtk.FILL | gtk.EXPAND)        
        self.etitle = gtk.Entry()
        self.etitle.set_text(not blank and parent.game.crossword.title or "")
        table.attach(self.etitle, 1, 2, 2, 3, gtk.FILL | gtk.EXPAND)        
        self.eauthor = gtk.Entry()
        self.eauthor.set_text(not blank and parent.game.crossword.author or "")
        table.attach(self.eauthor, 1, 2, 3, 4, gtk.FILL | gtk.EXPAND)        
        self.ecategory = gtk.Entry()
        self.ecategory.set_text(not blank and parent.game.crossword.category or "")
        table.attach(self.ecategory, 1, 2, 4, 5, gtk.FILL | gtk.EXPAND)        
        self.ealphabet = gtk.Entry()
        self.ealphabet.set_text(not blank and parent.game.crossword.alphabet or "")
        table.attach(self.ealphabet, 1, 2, 5, 6, gtk.FILL | gtk.EXPAND)        
        self.elanguage = gtk.Entry()
        self.elanguage.set_text(not blank and parent.game.crossword.language or "")
        table.attach(self.elanguage, 1, 2, 6, 7, gtk.FILL | gtk.EXPAND)        
        self.sminwlength = gtk.SpinButton()
        self.sminwlength.set_range(2, 128)
        self.sminwlength.set_increments(1, 1)
        self.sminwlength.set_value(blank and 3 or parent.game.crossword.minWordLength)
        table.attach(self.sminwlength, 1, 2, 7, 8, gtk.FILL | gtk.EXPAND)        
        vbox.pack_start(table, False)
        vbox.show_all()
            
gobject.signal_new("edited", CrosswordWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_BOOLEAN, (gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_STRING))
gobject.signal_new("cursor-moved", CrosswordWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_BOOLEAN, (gobject.TYPE_INT, gobject.TYPE_INT))
gobject.signal_new("right-click", CrosswordWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_BOOLEAN, (gtk.gdk.Event,))
