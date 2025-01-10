# -*- coding: utf-8 -*-
#############################################################################
# zlib License
#
# (C) 2024 Cristóvão Beirão da Cruz e Silva <cbeiraod@cern.ch>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#############################################################################
"""The ETROC2 GUI module

This is a utility module which serves as a wrapper for the ETROC2 GUI module so it can be called from the command line

"""

import argparse
import logging
import tkinter as tk

from i2c_gui2.gui import set_platform
from i2c_gui2.gui.base_gui import Base_GUI


def main(args=None):
    """This is the main entry function for the command line interface"""
    parser = argparse.ArgumentParser(description='Run the ETROC2 GUI from I2C-GUI++')
    # parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
    #                 help="A name of something.")
    args = parser.parse_args(args=args)

    print("This will eventually run the ETROC2 GUI, for now, just run the base stuff for testing")

    etroc2_logger = logging.getLogger("ETROC2")

    root = tk.Tk()
    set_platform(root.tk.call('tk', 'windowingsystem'))

    #  GUI = Base_GUI("Test", root, etroc2_logger)
    Base_GUI("Test", root, etroc2_logger)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
