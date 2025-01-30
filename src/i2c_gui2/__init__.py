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

from __future__ import annotations

__version__ = '0.1.11'

from .chips.etroc2_chip import ETROC2_Chip
from .functions import addLoggingLevel
from .i2c_messages import I2CMessages
from .i2c_usb_iss_helper import USB_ISS_Helper

# Add custom log levels to logging
addLoggingLevel('TRACE', 8)
addLoggingLevel('DETAILED_TRACE', 5)
# addLoggingLevel('HIGH_TEST', 100)

__all__ = ["I2CMessages", "USB_ISS_Helper", "ETROC2_Chip"]
