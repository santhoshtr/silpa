"""
Crossword Puzzle - Main package
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
import os
import sys
import time
import random
DOWN = 10
UP = 20
LEFT = 30
RIGHT = 40

def safeInt(v, default = 0):
    try:
        return int(v)
    except (ValueError, TypeError):
        return default

def safeFloat(v, default = 0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default

def safeBool(v, default = False):
    if v is None or isinstance(v, (bool, int, long, float)):
        return bool(v)
    v = v.strip()
    if v.lower() in ("true", "on", "yes") or safeInt(v):
        return True
    elif not v or v.lower() in ("false", "off", "no") or not safeInt(v):
        return False
    return default


def loadConfig(filename):
    try:
        f = file(os.path.expanduser(os.path.expandvars(filename)))
        data = f.read()
        f.close()
    except IOError, ioe:
        sys.stderr.write("warning: could not read config '%s'; %s\n"%(filename, ioe))
        return {}
    conf = {}
    data = data.replace("\r", "")
    for line in (l.strip() for l in data.split("\n") if l.strip()):
        spl = line.split("=", 1)
        if len(spl) == 2:
            key, val = spl
            if key == "window.width":
                conf[key] = safeInt(val, 640)
            elif key == "window.height":
                conf[key] = safeInt(val, 480)
            elif key == "window.paned":
                conf[key] = safeInt(val, 128)
            elif key == "gui.draw_missing_clues":
                conf[key] = safeBool(val, True)
            elif key == "gui.keep_aspect":
                conf[key] = safeBool(val, True)
            elif key == "gui.mirror_mode":
                conf[key] = safeBool(val, True)
    return conf
    

def saveConfig(filename, config):
    data = []
    for key, val in config.items():
        if key == "window.width":
            data.append("%s=%d"%(key, safeInt(val)))
        elif key == "window.height":
            data.append("%s=%d"%(key, safeInt(val)))
        elif key == "window.paned":
            data.append("%s=%d"%(key, safeInt(val)))
        elif key == "gui.draw_missing_clues":
            data.append("%s=%s"%(key, safeBool(val, True) and "true" or "false"))
        elif key == "gui.keep_aspect":
            data.append("%s=%s"%(key, safeBool(val, True) and "true" or "false"))
        elif key == "gui.mirror_mode":
            data.append("%s=%s"%(key, safeBool(val, True) and "true" or "false"))
    try:
        f = file(os.path.expanduser(os.path.expandvars(filename)), "w")
        f.write("\n".join(data))
        f.close()
    except IOError, ioe:
        sys.stderr.write("warning: could not write config '%s'; %s\n"%(filename, ioe))


class Matrix(dict):
    """
    2D matrix for holding unicode letters.
    """

    def __init__(self, w, h, contents = {}):
        """
        The contents of this matrix is a dictionary where the keys are tuples
        of x and y coordinates.
        """
        dict.__init__(self)
        self._width = w
        self._height = h

    def copy(self):
        m = Matrix(self.width, self.height)
        for y in xrange(self.height):
            for x in xrange(self.width):
                m[x, y] = self[x, y]

    def setWidth(self, w):
        self._width = w
        for x, y in self.keys():
            if x < 0 or x >= w:
                del self[x, y]

    def setHeight(self, h):
        self._height = h
        for x, y in self.keys():
            if y < 0 or y >= h:
                del self[x, y]

    width = property(lambda o: o._width, setWidth)
    height = property(lambda o: o._height, setHeight)

    def setVWord(self, x, y, word, direction = 1):
        """
        See setWord.
        Set vertical word on position x, y. By default it will
        set the word downwards, change the third and optional argument to -1
        to get a negative direction, i.e upwards.
        """
        for i, c in enumerate(word):
            if x >= 0 and y >= 0 and x < self.width and y + i * direction < self.height:
                self[x, y + i * direction] = c

    def setHWord(self, x, y, word, direction = 1):
        """
        See setWord.
        Set horizontal word on position x, y. By default it will
        set the word from left to right, change the third and optional
        argument to -1 to get a negative direction, i.e right to left.
        """
        for i, c in enumerate(word):
            if x >= 0 and y >= 0 and y < self.height and x + i * direction < self.width:
                self[x + i * direction, y] = u"%s"%c

    def getVWord(self, x, y, direction = 1):
        """
        See getWord.
        """
        ret = []
        c = self[x, y]
        while x >= 0 and x < self.width and y >= 0 and y < self.height and c != u"#":
            ret.append(c)
            y += direction
            c = self[x, y]
        return u"".join(ret)

    def getHWord(self, x, y, length = 0, direction = 1):
        """
        See getWord.
        """
        ret = []
        c = self[x, y]
        while x >= 0 and x < self.width and y >= 0 and y < self.height and c != u"#":
            ret.append(c)
            x += direction
            c = self[x, y]
        return u"".join(ret)

    def get(self, x, y, default = u"#"):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return dict.get((x, y), default)
        return u"#"

    def __getitem__(self, pos):
        x, y = pos
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return dict.get(self, pos) or u" "
        return u"#"

    def __setitem__(self, pos, value):
        x, y = pos
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            dict.__setitem__(self, pos, value)

    def serializeComponents(self):
        ret = []
        for y in xrange(self.height):
            row = []
            for x in xrange(self.width):
                c = self[x, y]
                if not c.strip():
                    c = u" "
                row.append(c)
            ret.append(u", ".join(row))
        return ret

    def __str__(self):
        ret = []
        for y in xrange(self.height):
            row = []
            for x in xrange(self.width):
                row.append(self[x, y])
            ret.append(u"|".join(row))
        return u"\n".join(ret)

    def getMaxVLength(self, x , y, direction = 1):
        """
        See getMaxLength.
        """
        i = 0
        c = self[x, y + i * direction]
        while c != u"#" and y + i < self.height:
            i += 1
            c = self[x, y + i * direction]
        return i

    def getMaxHLength(self, x , y, direction = 1):
        """
        See getMaxLength.
        """
        i = 0
        c = self[x + i * direction, y]
        while c != u"#" and x + i < self.width:
            i += 1
            c = self[x + i * direction, y]
        return i

    def getMatch(self, other):
        """
        Compares two matrixs and returns all letters that match it
        in a new matrix.
        """
        matrix = Matrix(self.width, self.height)
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                o = other[x, y]
                if c not in u" #" and c == o:
                    matrix[x, y] = c
                else:
                    matrix[x, y] = u" "
        return matrix

    def getNumLetters(self):
        """
        Return the number of letters filled out in the matrix.
        """
        num = 0
        for (x, y), letter in self.items():
            if letter and x >= 0 and x < self.width and y >= 0 and y < self.height and letter not in u" #":
                num += 1
        return num

    def clearBlack(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c == u"#":
                    self[x, y] = u" "

    def clearLetters(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c not in u"# ":
                    self[x, y] = u" "

    def conformToBlack(self, blackMatrix):
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = blackMatrix[x, y]
                if c == u"#":
                    self[x, y] = u" "

    def getEmptyCells(self):
        ret = []
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if not c or c == u" ":
                    ret.append((x, y))
        return ret

    def getFullCells(self):
        ret = []
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if not c is None and c.strip():
                    ret.append((x, y))
        return ret

    def removeInvalid(self, valid):
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c not in u"# " and not c in valid:
                    self[x, y] = u" "
                
    def getAllHWords(self):
        ret = []
        for y in xrange(self.height):
            word = []
            for x in xrange(self.width):
                c = self[x, y]
                if c == u" #":
                    ret.append(u"".join(word))
                else:
                    word.append(c)
            if word:
                ret.append(u"".join(word))
        return [r for r in ret if r.strip()]

    def getAllVWords(self):
        ret = []
        for x in xrange(self.width):
            word = []
            for y in xrange(self.height):
                c = self[x, y]
                if c == u"#":
                    ret.append(u"".join(word))
                else:
                    word.append(c)
            if word:
                ret.append(u"".join(word))
        return [r for r in ret if r.strip()]

    def getAllWords(self):
        return self.getAllHWords() + self.getAllVWords()

    def getNumWrong(self, sol):
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                o = sol[x, y]
                if c not in u" #" and not o in u" #" and c != o:
                    total += 1
        return total

    def getNumCorrect(self, sol):
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                o = sol[x, y]
                if c not in u" #" and not o in u" #" and c == o:
                    total += 1
        return total
                    
    def getNumBlack(self):
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c == u"#":
                    total += 1
        return total

    def getNumFree(self):
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c != u"#":
                    total += 1
        return total

    def getNumEmpty(self):
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                c = self[x, y]
                if c != u" ":
                    total += 1
        return total

    
class CluesSheet(object):
    """
    Holds all the clues for a crossword.
    """

    def __init__(self, hclues = {}, vclues = {}):
        """
        Starts a clue sheet at optional specified clues.
        """
        self._hclues = {}
        self._vclues = {}

    def iterHItems(self):
        return iter(self._hclues.items())

    def iterVItems(self):
        return iter(self._vclues.items())

    def setHClue(self, x, y, clue):
        """
        Set a clue for the horizontal word at position.
        """
        self._hclues[x, y] = clue

    def setVClue(self, x, y, clue):
        """
        Set a clue for the vertical word at position.
        """
        self._vclues[x, y] = clue

    def getHClue(self, x, y):
        """
        Get a clue for the horizontal word at position.
        Returns a unicode string or None if no clue was found.
        """
        if (x, y) in self._hclues:
            return self._hclues[x, y]
        return None

    def getVClue(self, x, y):
        """
        Get a clue for the vertical word at position.
        Returns a unicode string or None if no clue was found.
        """
        if (x, y) in self._vclues:
            return self._vclues[x, y]
        return None

    def delHClue(self, x, y):
        """
        Deletes a horizontal clue.
        """
        if (x, y) in self._hclues:
            del self._hclues[x, y]

    def delVClue(self, x, y):
        """
        Deletes a vertical clue.
        """
        if (x, y) in self._vclues:
            del self._vclues[x, y]

    def getBoundaries(self):
        """
        Returns the minimum horizontal and vertical position as well
        as the maximum horizontal and vertical position in a four
        element tuple.
        """
        xs = [p[0] for p in self._vclues.keys() + self._hclues.keys()]
        ys = [p[1] for p in self._vclues.keys() + self._hclues.keys()]
        if not xs:
            xs = [0]
        if not ys:
            ys = [0]
        return min(xs), min(ys), max(xs), max(ys)

    def getIds(self):
        """
        Returns two dictionaries: one with all the positions for keys
        and the IDs as values for horizontal and the other for vertical.
        """
        hpos = {}
        vpos = {}
        id_ = 1
        sx, sy, lx, ly = self.getBoundaries()
        for y in xrange(sy, ly + 1):
            for x in xrange(sx, lx + 1):
                if (x, y) in self._vclues:
                    vpos[x, y] = id_
                if (x, y) in self._hclues:
                    hpos[x, y] = id_
                if vpos.get((x, y)) or hpos.get((x, y)):
                    id_ += 1
        return hpos, vpos

    def getLongest(self):
        """
        Returns the longst clue (in characters) in the sheet.
        """
        m = 0
        c = None
        for (x, y), clue in self._vclues.items() + self._hclues.items():
            if len(clue) > m:
                m = len(clue)
                c = (x, y), clue
        return c

    def getHLongest(self):
        """
        Returns the longst clue (in characters) in the sheet for horizontal clues.
        """
        m = 0
        c = None
        for (x, y), clue in self._hclues.items():
            if len(clue) > m:
                m = len(clue)
                c = (x, y), clue
        return c

    def getVLongest(self):
        """
        Returns the longst clue (in characters) in the sheet for vertical clues.
        """
        m = 0
        c = None
        for (x, y), clue in self._vclues.items():
            if len(clue) > m:
                m = len(clue)
                c = (x, y), clue
        return c

    def lenH(self):
        return len(self._hclues)

    def lenV(self):
        return len(self._vclues)

    def __len__(self):
        return len(self._hclues) + len(self._vclues)
    
    def __str__(self):
        ret = []
        for (x, y), clue in self._hclues.items():
            ret.append(u"H %d, %d: %s"%(x, y, clue))
        for (x, y), clue in self._vclues.items():
            ret.append(u"V %d, %d: %s"%(x, y, clue))
        return u"\n".join(ret)
    
        
class Crossword(object):
    """
    A crossword holds one contents matrix, zero or more solution matrices and
    zero or more clue sheets.
    """
    def __init__(self, **kwargs):
        """
        Keyword args:
        playerMatrix    A matrix the player uses to fill in his contents.
        solutionMatrices  A list of solution variations.
        clues           A CluesSheet instance.
        """
        self.alphabet = kwargs.get("alphabet", u"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self.playerMatrix = kwargs.get("playerMatrix", Matrix(kwargs.get("width", 15), kwargs.get("height", 15)))
        self.solutionMatrices = kwargs.get("solutionMatrices", [])
        self.blackMatrix = kwargs.get("blackMatrix", Matrix(self.playerMatrix.width, self.playerMatrix.height))
        self.normalize()
        self.clues = kwargs.get("clues", CluesSheet())
        self.title = kwargs.get("title")
        self.category = kwargs.get("category")
        self.author = kwargs.get("author")
        self.language = kwargs.get("language")
        self.minWordLength = kwargs.get("minWordLength", 3)

    def normalize(self):
        for solution in self.solutionMatrices + [self.playerMatrix, self.blackMatrix]:
            if solution == self.blackMatrix:
                solution.clearLetters()
            else:
                solution.clearBlack()
                solution.conformToBlack(self.blackMatrix)
            if solution != self.playerMatrix:
                if solution.width != self.playerMatrix.width:
                    solution.width = self.playerMatrix.width
                if solution.height != self.playerMatrix.height:
                    solution.height = self.playerMatrix.height
            solution.removeInvalid(self.alphabet)

    def getWidth(self):
        return self.playerMatrix.width

    def getHeight(self):
        return self.playerMatrix.height

    def setWidth(self, w):
        self.playerMatrix.width = w
        self.normalize()
        return self.playerMatrix.height

    def setHeight(self, h):
        self.playerMatrix.height = h
        self.normalize()
        return self.playerMatrix.height

    width = property(getWidth, setWidth)
    height = property(getHeight, setHeight)

    def getMatching(self):
        """
        Return match matrices for all solution matrices in the crossword.
        """
        ret = []
        for solutionMatrix in self.solutionMatrices:
            ret.append(self.playerMatrix.getMatch(solutionMatrix))
        return ret


class Game(object):

    def __init__(self, crossword = None, **kwargs):
        self.start = 0.0
        self.stop = 0.0
        self.crossword = crossword or Crossword()
        self.scoring = kwargs.get("scoring", ScoringTimeAttack())

    def getMinWordLength(self):
        return self.crossword.minWordLength

    def setMinWordLength(self, v):
        if v < 2:
            v = 2
        elif v > 128:
            v = 128
        self.crossword.minWordLength = v

    minWordLength = property(getMinWordLength, setMinWordLength)

    def startGame(self):
        self.start = time.time()
        self.stop = 0.0

    def stopGame(self):
        self.stop = time.time()

    def getTime(self):
        if self.start > 0.0:
            if self.stop > 0.0:
                return self.stop - self.start
            return time.time() - self.start
        return 0.0

    def getScore(self):
        if self.start and self.scoring:
            return self.scoring.getFinalScore(self.getTime(), self.crossword)
        return 0.0

    def getScoreComponents(self):
        if self.scoring:
            return self.scoring.getComponents(self.getTime(), self.crossword)
        return []

    def __str__(self):
        ret = [u"# Crossword Puzzle game",
               u"encoding=utf8",
               u"width=%d"%self.crossword.width,
               u"height=%d"%self.crossword.height,
               u"title=%s"%(self.crossword.title or u"").strip(),
               u"category=%s"%(self.crossword.category or u"").strip().upper(),
               u"author=%s"%(self.crossword.author or u"").strip(),
               u"alphabet=%s"%(self.crossword.alphabet or u"").strip().upper(),
               u"language=%s"%(self.crossword.language or u"").strip().upper(),
               u"min_word_length=%d"%self.minWordLength,
               u"",
               u"; Player matrix", u"Player matrix:"]
        ret += self.crossword.playerMatrix.serializeComponents()
        ret += [u"", u"; Black matrix", u"Black matrix:"]
        ret += self.crossword.blackMatrix.serializeComponents()
        for i, sol in enumerate(self.crossword.solutionMatrices):
            ret += [u"", u"; Solution %d"%(i + 1), u"Solution matrix:"]
            ret += sol.serializeComponents()
        ret += [u"", u"; Clues", "Clues:"]
        for (x, y), clue in self.crossword.clues.iterHItems():
            ret.append("H %d %d %s"%(x, y, clue))
        for (x, y), clue in self.crossword.clues.iterVItems():
            ret.append("V %d %d %s"%(x, y, clue))
        r = u"\n".join(ret)
        return r.encode("utf8")
            
    @staticmethod
    def loadFromString(s):
        game = Game()
        s = unicode(s, "utf8")
        mode = 0
        row = 0
        for line in (l.strip() for l in s.split("\n")):
            if not line.startswith(";"):
                low = line.lower()
                splits = [l.strip() for l in line.split("=", 1)]
                if len(splits) == 2 and mode == 0:
                    key, val = splits
                    if key == "width":
                        game.crossword.width = safeInt(val, 15)
                    elif key == "height":
                        game.crossword.height = safeInt(val, 15)  
                    elif key == "title":
                        game.crossword.title = val
                    elif key == "alpha":
                        game.crossword.crossword.alphabet = val
                    elif key == "author":
                        game.crossword.author = val
                    elif key == "category":
                        game.crossword.category = val
                    elif key == "alphabet":
                        game.crossword.alphabet = val.upper()
                    elif key == "language":
                        game.crossword.language = val.upper()
                    elif key == "min_word_length":
                        game.crossword.minWordLength = safeInt(val, 3)
                elif low == "player matrix:":
                    mode = 1
                    row = 0
                elif low == "black matrix:":
                    mode = 2
                    row = 0
                elif low == "solution matrix:":
                    mode = 3
                    row = 0
                    game.crossword.solutionMatrices.append(Matrix(1, 1))
                    game.crossword.normalize()
                elif low == "clues:":
                    mode = 4
                elif mode > 0 and mode < 4 and line.find(",") >= 0:
                    cols = [l.strip() for l in line.split(",")]
                    for i, c in enumerate(cols):
                        if mode == 1:
                            matrix = game.crossword.playerMatrix                        
                        elif mode == 2:
                            matrix = game.crossword.blackMatrix
                        elif mode == 3:
                            matrix = game.crossword.solutionMatrices[-1]
                        if i < game.crossword.width and row < game.crossword.height:
                            c = u"%s"%c
                            if len(c) > 1:
                                c = c[0]
                            elif not c:
                                c = u" "
                            matrix[i, row] = c.upper()
                    row += 1
                elif mode == 4:
                    spl = [l.strip() for l in line.split(" ", 3)]
                    if len(spl) == 4:
                        orientation, x, y, clue = spl
                        try:
                            x = int(x)
                        except ValueError:
                            x = -1
                        try:
                            y = int(y)
                        except ValueError:
                            y = -1
                        if x >= 0 and y >= 0:
                            if orientation.upper() == "H":
                                game.crossword.clues.setHClue(x, y, clue)
                            elif orientation.upper() == "V":
                                game.crossword.clues.setVClue(x, y, clue)
                
        game.crossword.normalize()
        return game


class Scoring(object):
    """
    A scoring class.
    """
    name = u""
    description = u""
    type_ = int
    timelimit = 0

    def getComponents(self, t, cw):
        """
        Returns a list of tuples containing the score (float) and the component name (str).
        """
        return []

    def getFinalScore(self, t, cw):
        return self.getSumComponents(self.getComponents(t, cw))

    def getSumComponents(self, comps):
        total = self.type_(0)
        for score, mult, name in comps:
            total += (score * mult)
        return score


class ScoringSimple(Scoring):
    """
    A simple scoring system that just gives you one point for
    every correct word. Time is of no relevance.
    """
    name = u"Simple"
    description = u"A simple scoring system that just gives you one point for every correct word. Time is of no relevance."
    type_ = int
    timelimit = 0

    def getComponents(self, t, cw):
        wordscores = []
        pwords = cw.playerMatrix.getAllWords()
        for matrix in cw.solutionMatrices:
            wordscores.append(0)
            mwords = matrix.getAllWords()
            for pword in pwords:
                if pword in mwords:
                    wordscores[-1] += 1
        if wordscores:
            wordscores.sort()
            return [(1, wordscores[-1], "Correct words")]
        return [(1, 0, "Correct words")]
        

class ScoringTimeAttack(Scoring):
    """
    Gives you 100 points for every correct word, -100 for every incorrect word and divides it with the number of minutes played.
    """
    name = u"Time Attack"
    description = u"Gives you 100 points for every correct word, -100 for every incorrect word and divides it with the number of minutes played."
    type_ = int
    timelimit = 0

    def getComponents(self, t, cw):
        ret = []
        wordscores = []
        pwords = cw.playerMatrix.getAllWords()
        for matrix in cw.solutionMatrices:
            wordscores.append([0, 0])
            mwords = matrix.getAllWords()
            for pword in pwords:
                if pword in mwords:
                    wordscores[-1][0] += 1
                else:
                    wordscores[-1][1] += 1
        if wordscores:
            wordscores.sort(lambda a, b: cmp(a[0] - a[1], b[0] - b[1]))
            ret.append((100, wordscores[-1][0], "Correct words"))
            ret.append((-100, wordscores[-1][1], "Incorrect words"))
            total = wordscores[-1][0] * 100 - wordscores[-1][1] * 100
            mins = float(int(t / 60))
            if mins > 0:
                finalscore = total / mins
            else:
                finalscore = total
            ret.append((-1, int(total - finalscore), "Time deduction"))
        return ret


class ScoringTournament(Scoring):
    """
    A scoring class for tournament rules.
    """
    name = u"Tournament"
    description = u"Tournament rules."
    type_ = int
    timelimit = 600

    def getComponents(self, t, cw):
        """
        Returns a list of tuples containing the score, multiplier and the component name (str).
        Always tries to return the highest possible score.
        """
        retcomps = []
        highest = 0
        for matrix in cw.solutionMatrices:
            comps = self.getComponentsForMatrix(t, cw, matrix)
            sm = self.getSumComponents(comps)
            if sm > highest or not retcomps:
                retcomps = comps
                highest = sm
        return retcomps

    def getComponentsForMatrix(self, t, cw, matrix):
        ret = []
        wordscore = 0
        pwords = cw.playerMatrix.getAllWords()
        mwords = matrix.getAllWords()
        for pword in pwords:
            if pword in mwords:
                wordscore += 1
        ret.append((10, wordscore, "Correct words"))
        parbeat = int(self.timelimit / 60 - t / 60)
        if parbeat < 0:
            parbeat = 0
        ret.append((25, parbeat, "Full minutes before par"))
        wrong = cw.blackMatrix.getNumFree() - cw.playerMatrix.getNumCorrect(matrix)
        ret.append((-25, wrong, "Deduction for incorrect cells"))
        ret.append((150, wordscore == len(mwords) and 1 or 0, "Complete and correct bonus"))
        return ret

    def getFinalScore(self, t, cw):
        return 0
