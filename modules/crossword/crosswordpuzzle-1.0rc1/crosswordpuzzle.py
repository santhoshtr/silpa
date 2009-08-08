#!/usr/bin/env python
"""
Crossword Puzzle
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

import sys
sys.path.append(".")
import os
from optparse import OptionParser
from cwp.gtkgui import CrosswordPuzzle
from cwp import loadConfig, saveConfig

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--advanced", dest="advanced",
                      action="store_true", default=False,
                      help="start application in advanced mode")
    (options, args) = parser.parse_args()
    config = loadConfig("~/.crosswordrc")
    cwp = CrosswordPuzzle(config, options.advanced)
    if args:
        cwp.window.load_crossword(args[0])
    cwp.run()
    saveConfig("~/.crosswordrc", config)
