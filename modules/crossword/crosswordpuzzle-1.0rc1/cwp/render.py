"""
Crossword Puzzle - Rendering, default Cairo
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
import cairo


class CairoRender(object):
    """
    The Cairo renderer uses Cairo to render the crossword.
    """

    def __init__(self, context, gw, gh, w, h, aspect = True, **kwargs):
        """
        Given a context, grid width, grid height, resolution width and resolution height
        the crossword can be drawn accordingly.
        Optional arguments are boolean for keeping aspect ratio, keyword arguments are
        offsetx, offsety, lineWidth and readonly.
        """
        self.context = context
        self.gridWidth = gw
        self.gridHeight = gh
        self.width = w
        self.height = h
        self.aspect = aspect
        self.lineWidth = kwargs.get("lineWidth", 2.0)
        self.readonly = kwargs.get("readonly", False)
        self.offsetx = kwargs.get("offsetx", 0)
        self.offsety = kwargs.get("offsety", 0)
        self._uw = w / float(gw)
        self._uh = h / float(gh)
        if aspect:
            if self._uw < self._uh:
                self._uh = self._uw
            else:
                self._uw = self._uh
        else:
            self._uw *= 0.5

    def clip(self):
        """
        Set the clip for the offset, width and height.
        """
        self.context.rectangle(self.offsetx, self.offsety, self.width, self.height)
        self.context.clip()
        
    def draw_background(self, color = (1.0, 1.0, 1.0, 1.0)):
        """
        Draws the background using the rgba color optionally specified.
        """
        self.context.set_source_rgba(*color)
        self.context.fill()        
        self.context.paint()

    def draw_cursor(self, x, y, fgcolor = (1.0, 0.0, 0.0), bgcolor = (1.0, 0.5, 0.0, 0.5)):
        """
        Draws the cursor at specified grid position. Optional arguments for foreground and
        background color can be supplied.
        """
        if not self.readonly:
            self.context.set_source_rgba(*bgcolor)
            self.context.rectangle(self.offsetx + x * self._uw + self.lineWidth,
                                   self.offsety + y * self._uh + self.lineWidth,
                                   self._uw - self.lineWidth * 2,
                                   self._uh - self.lineWidth * 2)
            self.context.fill()
        self.context.set_source_rgba(*fgcolor)
        self.context.rectangle(self.offsetx + x * self._uw + self.lineWidth,
                               self.offsety + y * self._uh + self.lineWidth,
                               self._uw - self.lineWidth * 2,
                               self._uh - self.lineWidth * 2)
        self.context.stroke()

    def draw_grid(self, color = (0.0, 0.0, 0.0, 1.0)):
        """
        Draws the grid using optionally color argument.
        """
        uw, uh = self._uw, self._uh
        self.context.set_source_rgba(*color)
        self.context.set_line_width(self.lineWidth)
        for y in xrange(0, self.gridHeight + 1):
            self.context.move_to(self.offsetx, self.offsety + y * uh)
            self.context.line_to(self.offsetx + self.gridWidth * uw, self.offsety + y * uh)
        for x in xrange(0, self.gridWidth + 1):
            self.context.move_to(self.offsetx + x * uw, self.offsety)
            self.context.line_to(self.offsetx + x * uw, self.offsety + self.gridHeight * uh)
        self.context.stroke()

    def draw_focus_border(self, color = (0.0, 0.0, 0.0, 1.0)):
        """
        Draws a focus border (dotted inline border) using optionally specified
        color.
        """
        self.context.set_source_rgba(*color)
        if self.aspect:
            if self.width < self.height:
                w = self.width
                h = self.width
            else:
                w = self.height
                h = self.height
        else:
            w, h = self.width, self.height
        self.context.set_line_width(self.lineWidth * 0.5)
        self.context.rectangle(self.offsetx + self.lineWidth * 2,
                               self.offsety + self.lineWidth * 2,
                               w - self.lineWidth * 4,
                               h - self.lineWidth * 4)
        self.context.set_dash((1, 1))
        self.context.stroke()
        self.context.set_line_width(self.lineWidth)
        self.context.set_dash([])
            
        
    def draw_matrix(self, matrix, color = (0.0, 0.0, 0.0,1.0), modifyBlack = 0):
        """
        Draws all the letters and black cells using the optionally specified color.
        The second optional argument is caleld modifyBlack;
        0 = both letters and black, 1 = only black, -1 = only letters and
        1 for only black cells.
        """
        self.context.set_source_rgba(*color)
        uw, uh = self._uw, self._uh
        if uh <= uw:
            self.context.set_font_size(uh * 0.75)
        else:
            self.context.set_font_size(uw * 0.75)
        for y in xrange(matrix.height):
            for x in xrange(matrix.width):
                letter = matrix[x, y]
                self.draw_cell(x, y, letter, modifyBlack)
        
    def draw_cell(self, x, y, letter, modifyBlack = 0):
        """
        Draws the cell using specified grid position and letter.
        The third, optional argument modifies what is drawn;
        0 = both letters and black, 1 = only black, -1 = only letters and
        1 for only black cells.
        """
        uw, uh = self._uw, self._uh
        if letter == u"#":
            if modifyBlack >= 0:
                self.context.rectangle(self.offsetx + x * uw, self.offsety + y * uh, uw, uh)
                self.context.fill()
        elif modifyBlack <= 1:
            tx, ty, tw, th, tdx, tdy = self.context.text_extents(letter or "")
            self.context.move_to(self.offsetx + x * uw + uw * 0.5 - (tw * 0.5 + tx),
                                 self.offsety + y * uh + uh * 0.55 - (th * 0.5 + ty))
            self.context.show_text(letter or "")
            self.context.stroke()

    def draw_clue_ids(self, ids, fgcolor = (0.0, 0.0, 0.0, 1.0), bgcolor = (1.0, 1.0, 1.0,1.0)):
        """
        Draws the small clue ID numbers in the top, left corner of the cell.
        It takes a ID dictionary as given by Matrix.getIds() and two optional
        color arguments for foreground and background.
        Background is used first to outline the text.
        """
        uw, uh = self._uw, self._uh
        if uh <= uw:
            fz = uh
        else:
            fz = uw
        for (x, y), id_ in ids.items():
            letter = "%d"%id_
            self.context.set_font_size(fz * 0.4)
            tx, ty, tw, th, tdx, tdy = self.context.text_extents(letter or "")
            dx = int(self.offsetx + x * uw + uw * 0.1)
            dy = int(self.offsety + y * uh + uh * 0.1 + th)
            self.context.set_source_rgba(*bgcolor)
            for yy in xrange(dy - 1, dy + 1):
                for xx in xrange(dx - 1, dx + 1):
                    if xx != dx or yy != dy:
                        self.context.move_to(xx, yy)
                        self.context.show_text(letter or "")
            self.context.move_to(dx, dy)
            self.context.set_source_rgba(*fgcolor)
            self.context.show_text(letter or "")
        self.context.stroke()

    def draw_selection(self, x, y, w, h, color = (0.5, 0.5, 0.5, 0.5)):
        """
        Draws a selection on the context. The selection is specified by
        grid units for top, left corner, width and height.
        Optional color argument available.
        """
        self.context.set_source_rgba(*color)
        sizes = int(self.offsetx + x * self._uw), int(self.offsety + y * self._uh), int(w * self._uw), int(h * self._uh)
        self.context.rectangle(*sizes)
        self.context.fill()

    def draw_missing_clues(self, crossword, color = (1.0, 0.0, 0.0, 0.25)):
        """
        Fills the cell area with a distinct color to notify clues are missing.
        You have to specify an entire crossword and optional color argument.
        """
        self.context.set_source_rgba(*color)
        y = 0
        while y < crossword.height:
            x = 0
            while x < crossword.width:
                ml = crossword.blackMatrix.getMaxHLength(x, y)
                if ml >= crossword.minWordLength:
                    if not crossword.clues.getHClue(x, y):
                        xx, yy, w, h = int(self.offsetx + x * self._uw), int(self.offsety + y * self._uh), int(ml * self._uw), int(self._uh)
                        self.context.rectangle(xx, yy, w, h)
                        self.context.fill()
                    x += ml
                else:
                    x += 1
            y += 1
        x = 0
        while x < crossword.width:
            y = 0
            while y < crossword.height:
                ml = crossword.blackMatrix.getMaxVLength(x, y)
                if ml >= crossword.minWordLength:
                    if not crossword.clues.getVClue(x, y):
                        xx, yy, w, h = int(self.offsetx + x * self._uw), int(self.offsety + y * self._uh), int(self._uw), int(ml * self._uh)
                        self.context.rectangle(xx, yy, w, h)
                        self.context.fill()
                    y += ml
                else:
                    y += 1
            x += 1
                    

    def draw_clues(self, crossword, ox, oy, color = (0.0, 0.0, 0.0, 1.0)):
        """
        Draw the clues from a crossword at specified grid location. Optional
        color argument available.
        """
        clues = crossword.clues
        if not clues:
            return
        self.context.set_source_rgba(*color)
        maxwidth = self.width - self.offsetx - ox
        maxheight = self.height - self.offsety - oy        
        hpos, vpos = clues.getIds()
        if clues.lenH() > 0:
            hc = clues.getHLongest()[1]
        else:
            hc = ""
        if clues.lenV() > 0:
            vc = clues.getVLongest()[1]
        else:
            vc = ""
        ll = clues.lenH() > clues.lenV() and clues.lenH() or clues.lenV()
        fz = self.height / (ll + 3.0)
        self.context.set_font_size(fz)
        tx, ty, tw1, th, tdx, tdy = self.context.text_extents("0000: %s"%vc)
        tx, ty, tw2, th, tdx, tdy = self.context.text_extents("0000: %s"%hc)
        while self.width * 0.5 + tw1 + tw2 >= self.width:
            fz -= 1.0
            self.context.set_font_size(fz)
            tx, ty, tw1, th, tdx, tdy = self.context.text_extents("0000: %s"%vc)
            tx, ty, tw2, th, tdx, tdy = self.context.text_extents("0000: %s"%hc)
        tw = tw2
        y = self.offsety + oy + th
        x = self.offsetx + ox
        self.context.move_to(x, y)
        self.context.show_text("Across:")
        cluepos = sorted([(xx, yy, id_) for (xx, yy), id_ in hpos.items()], lambda a, b: cmp(a[2], b[2]))
        y += th
        for xx, yy, id_ in cluepos:
            self.context.move_to(x, y)
            self.context.show_text("%d: %s"%(id_, clues.getHClue(xx, yy)))
            y += th
        y = self.offsety + oy + th
        x = self.offsetx + ox + tw
        self.context.move_to(x, y)
        self.context.show_text("Down:")
        cluepos = sorted([(xx, yy, id_) for (xx, yy), id_ in vpos.items()], lambda a, b: cmp(a[2], b[2]))
        y += th
        for xx, yy, id_ in cluepos:
            self.context.move_to(x, y)
            self.context.show_text("%d: %s"%(id_, clues.getVClue(xx, yy)))
            y += th
        self.context.stroke()
        
        
