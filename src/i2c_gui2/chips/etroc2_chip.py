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

import logging

from ..i2c_connection_helper import I2C_Connection_Helper
from .address_space_controller import Address_Space_Controller
from .base_chip import Base_Chip

etroc2_version = "0.0.1"


def etroc2_column_row_to_base_address(block: str, column: int, row: int, broadcast: bool = False):
    address = 0b1000_0000_0000_0000

    if block == "Pixel Config":
        pass
    elif block == "Pixel Status":
        address = address | 0b0100_0000_0000_0000
    else:
        raise RuntimeError("The etroc2 register block must be either 'Pixel Config' or 'Pixel Status'")

    if broadcast:
        address = address | 0b0010_0000_0000_0000

    if column > 15 or column < 0:
        raise RuntimeError("The etroc2 column must be between 0 and 15")
    address = address | (column << 9)

    if row > 15 or row < 0:
        raise RuntimeError("The etroc2 row must be between 0 and 15")
    address = address | (row << 5)

    return address


register_model = {
    "ETROC2": {  # Address Space (i.e. separate I2C memory spaces)
        "Memory Size": 65536,  # 16 bit memory space
        "Address Bitlength": 16,
        "Address Endianness": 'little',
        "Word Bitlength": 8,
        "Word Endianness": 'big',
        "Register Blocks": {
            "Peripheral Config": {  # Register Block (i.e. group of registers to be handled as one unit)
                "Base Address": 0x0000,
                "Registers": {
                    "PeriCfg0": {
                        "offset": 0x0000,
                        "default": 0x2C,
                    },
                    "PeriCfg1": {
                        "offset": 0x0001,
                        "default": 0x98,
                    },
                    "PeriCfg2": {
                        "offset": 0x0002,
                        "default": 0x29,
                    },
                    "PeriCfg3": {
                        "offset": 0x0003,
                        "default": 0x18,
                    },
                    "PeriCfg4": {
                        "offset": 0x0004,
                        "default": 0x21,
                    },
                    "PeriCfg5": {
                        "offset": 0x0005,
                        "default": 0x00,
                    },
                    "PeriCfg6": {
                        "offset": 0x0006,
                        "default": 0x03,
                    },
                    "PeriCfg7": {
                        "offset": 0x0007,
                        "default": 0xA3,
                    },
                    "PeriCfg8": {
                        "offset": 0x0008,
                        "default": 0xE3,
                    },
                    "PeriCfg9": {
                        "offset": 0x0009,
                        "default": 0xE3,
                    },
                    "PeriCfg10": {
                        "offset": 0x000A,
                        "default": 0xD0,
                    },
                    "PeriCfg11": {
                        "offset": 0x000B,
                        "default": 0x10,
                    },
                    "PeriCfg12": {
                        "offset": 0x000C,
                        "default": 0x00,
                    },
                    "PeriCfg13": {
                        "offset": 0x000D,
                        "default": 0x80,
                    },
                    "PeriCfg14": {
                        "offset": 0x000E,
                        "default": 0xF0,
                    },
                    "PeriCfg15": {
                        "offset": 0x000F,
                        "default": 0x60,
                    },
                    "PeriCfg16": {
                        "offset": 0x0010,
                        "default": 0x90,
                    },
                    "PeriCfg17": {
                        "offset": 0x0011,
                        "default": 0x98,
                    },
                    "PeriCfg18": {
                        "offset": 0x0012,
                        "default": 0x00,
                    },
                    "PeriCfg19": {
                        "offset": 0x0013,
                        "default": 0x56,
                    },
                    "PeriCfg20": {
                        "offset": 0x0014,
                        "default": 0x40,
                    },
                    "PeriCfg21": {
                        "offset": 0x0015,
                        "default": 0x2C,
                    },
                    "PeriCfg22": {
                        "offset": 0x0016,
                        "default": 0x00,
                    },
                    "PeriCfg23": {
                        "offset": 0x0017,
                        "default": 0x00,
                    },
                    "PeriCfg24": {
                        "offset": 0x0018,
                        "default": 0x00,
                    },
                    "PeriCfg25": {
                        "offset": 0x0019,
                        "default": 0x00,
                    },
                    "PeriCfg26": {
                        "offset": 0x001A,
                        "default": 0xC5,
                    },
                    "PeriCfg27": {
                        "offset": 0x001B,
                        "default": 0x8C,
                    },
                    "PeriCfg28": {
                        "offset": 0x001C,
                        "default": 0xC7,
                    },
                    "PeriCfg29": {
                        "offset": 0x001D,
                        "default": 0xAC,
                    },
                    "PeriCfg30": {
                        "offset": 0x001E,
                        "default": 0xBB,
                    },
                    "PeriCfg31": {
                        "offset": 0x001F,
                        "default": 0x0B,
                    },
                },
            },
            "Peripheral Status": {  # Register Block
                "Base Address": 0x0100,
                "Registers": {
                    "PeriSta0": {
                        "offset": 0x0000,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta1": {
                        "offset": 0x0001,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta2": {
                        "offset": 0x0002,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta3": {
                        "offset": 0x0003,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta4": {
                        "offset": 0x0004,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta5": {
                        "offset": 0x0005,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta6": {
                        "offset": 0x0006,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta7": {
                        "offset": 0x0007,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta8": {
                        "offset": 0x0008,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta9": {
                        "offset": 0x0009,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta10": {
                        "offset": 0x000A,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta11": {
                        "offset": 0x000B,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta12": {
                        "offset": 0x000C,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta13": {
                        "offset": 0x000D,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta14": {
                        "offset": 0x000E,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PeriSta15": {
                        "offset": 0x000F,
                        "default": 0x00,
                        "read_only": True,
                    },
                },
                "read_only": True,
            },
            "Pixel Config": {  # Register Block
                "Indexer": {
                    "vars": ["block", "column", "row"],
                    "min": [None, 0, 0],
                    "max": [None, 16, 16],
                    "function": etroc2_column_row_to_base_address,
                },
                "Registers": {
                    "PixCfg0": {
                        "offset": 0x0000,
                        "default": 0x5C,
                    },
                    "PixCfg1": {
                        "offset": 0x0001,
                        "default": 0x06,
                    },
                    "PixCfg2": {
                        "offset": 0x0002,
                        "default": 0x0F,
                    },
                    "PixCfg3": {
                        "offset": 0x0003,
                        "default": 0x05,
                    },
                    "PixCfg4": {
                        "offset": 0x0004,
                        "default": 0x00,
                    },
                    "PixCfg5": {
                        "offset": 0x0005,
                        "default": 0x28,
                    },
                    "PixCfg6": {
                        "offset": 0x0006,
                        "default": 0xC2,
                    },
                    "PixCfg7": {
                        "offset": 0x0007,
                        "default": 0x01,
                    },
                    "PixCfg8": {
                        "offset": 0x0008,
                        "default": 0x81,
                    },
                    "PixCfg9": {
                        "offset": 0x0009,
                        "default": 0xFA,
                    },
                    "PixCfg10": {
                        "offset": 0x000A,
                        "default": 0x10,
                    },
                    "PixCfg11": {
                        "offset": 0x000B,
                        "default": 0x00,
                    },
                    "PixCfg12": {
                        "offset": 0x000C,
                        "default": 0x08,
                    },
                    "PixCfg13": {
                        "offset": 0x000D,
                        "default": 0x02,
                    },
                    "PixCfg14": {
                        "offset": 0x000E,
                        "default": 0x80,
                    },
                    "PixCfg15": {
                        "offset": 0x000F,
                        "default": 0x10,
                    },
                    "PixCfg16": {
                        "offset": 0x0010,
                        "default": 0x00,
                    },
                    "PixCfg17": {
                        "offset": 0x0011,
                        "default": 0x42,
                    },
                    "PixCfg18": {
                        "offset": 0x0012,
                        "default": 0x00,
                    },
                    "PixCfg19": {
                        "offset": 0x0013,
                        "default": 0x20,
                    },
                    "PixCfg20": {
                        "offset": 0x0014,
                        "default": 0x08,
                    },
                    "PixCfg21": {
                        "offset": 0x0015,
                        "default": 0x00,
                    },
                    "PixCfg22": {
                        "offset": 0x0016,
                        "default": 0x42,
                    },
                    "PixCfg23": {
                        "offset": 0x0017,
                        "default": 0x00,
                    },
                    "PixCfg24": {
                        "offset": 0x0018,
                        "default": 0x02,
                    },
                    "PixCfg25": {
                        "offset": 0x0019,
                        "default": 0x00,
                    },
                    "PixCfg26": {
                        "offset": 0x001A,
                        "default": 0x00,
                    },
                    "PixCfg27": {
                        "offset": 0x001B,
                        "default": 0x00,
                    },
                    "PixCfg28": {
                        "offset": 0x001C,
                        "default": 0x00,
                    },
                    "PixCfg29": {
                        "offset": 0x001D,
                        "default": 0x00,
                    },
                    "PixCfg30": {
                        "offset": 0x001E,
                        "default": 0x00,
                    },
                    "PixCfg31": {
                        "offset": 0x001F,
                        "default": 0x00,
                    },
                },
            },
            "Pixel Status": {  # Register Block
                "Indexer": {
                    "vars": ["block", "column", "row"],
                    "min": [None, 0, 0],
                    "max": [None, 16, 16],
                    "function": etroc2_column_row_to_base_address,
                },
                "Registers": {
                    "PixSta0": {
                        "offset": 0x0000,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta1": {
                        "offset": 0x0001,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta2": {
                        "offset": 0x0002,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta3": {
                        "offset": 0x0003,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta4": {
                        "offset": 0x0004,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta5": {
                        "offset": 0x0005,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta6": {
                        "offset": 0x0006,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "PixSta7": {
                        "offset": 0x0007,
                        "default": 0x00,
                        "read_only": True,
                    },
                },
                "read_only": True,
            },
        },
    },
    "Waveform Sampler": {  # Address Space
        "Memory Size": 48,
        "Address Bitlength": 8,
        "Address Endianness": 'big',
        "Word Bitlength": 8,
        "Word Endianness": 'big',
        "Register Blocks": {
            "Config": {
                "Base Address": 0x0000,
                "Registers": {
                    "regOut00": {
                        "offset": 0x0000,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut01": {
                        "offset": 0x0001,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut02": {
                        "offset": 0x0002,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut03": {
                        "offset": 0x0003,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut04": {
                        "offset": 0x0004,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut05": {
                        "offset": 0x0005,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut06": {
                        "offset": 0x0006,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut07": {
                        "offset": 0x0007,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut08": {
                        "offset": 0x0008,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut09": {
                        "offset": 0x0009,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut0A": {
                        "offset": 0x000A,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut0B": {
                        "offset": 0x000B,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut0C": {
                        "offset": 0x000C,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut0D": {
                        "offset": 0x000D,
                        "default": 0x18,
                    },
                    "regOut0E": {
                        "offset": 0x000E,
                        "default": 0x00,
                    },
                    "regOut0F": {
                        "offset": 0x000F,
                        "default": 0x00,
                    },
                    "regOut10": {
                        "offset": 0x0010,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut11": {
                        "offset": 0x0011,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut12": {
                        "offset": 0x0012,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut13": {
                        "offset": 0x0013,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut14": {
                        "offset": 0x0014,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut15": {
                        "offset": 0x0015,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut16": {
                        "offset": 0x0016,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut17": {
                        "offset": 0x0017,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut18": {
                        "offset": 0x0018,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut19": {
                        "offset": 0x0019,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut1A": {
                        "offset": 0x001A,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut1B": {
                        "offset": 0x001B,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut1C": {
                        "offset": 0x001C,
                        "default": 0x00,
                    },
                    "regOut1D": {
                        "offset": 0x001D,
                        "default": 0x00,
                    },
                    "regOut1E": {
                        "offset": 0x001E,
                        "default": 0x00,
                        "display": False,
                    },
                    "regOut1F": {
                        "offset": 0x001F,
                        "default": 0xCF,
                    },
                },
            },
            "Status": {
                "Base Address": 0x0020,
                "Registers": {
                    "regIn20": {
                        "offset": 0x0000,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "regIn21": {
                        "offset": 0x0001,
                        "default": 0x00,
                        "read_only": True,
                    },
                },
                "read_only": True,
            },
        },
    },
}

register_decoding = {
    "ETROC2": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks": {
            "Peripheral Config": {  # Register Block (i.e. group of registers to be handled as one unit)
                "PLLclkgen_disCLK": {
                    "bits": 1,
                    "position": [
                        ("PeriCfg0", "0", "0")
                    ],  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                    "info": "{0} disables the internal clock buffers and ½ clock divider in prescaler, active high. Debugging use only.\nWhen {0} is high, all output clocks are disabled.",
                    "show_binary": False,
                    "group": "test",
                },
                "PLLclkgen_disDES": {
                    "bits": 1,
                    "position": [("PeriCfg0", "1", "0")],
                    "info": "{0} disables output clocks for deserializer, active high. Debugging use only.\nWhen {0} is high, the following clocks are disabled:\n - clk2g56Qp\n - clk2g56Qn\n - clk2g56Ip\n - clk2g56In\n(clk2g56Q is the 2.56 GHz clock for test in ETROC_PLL. clk2g56Q is used as Waveform Sampler clock in ETROC2)",
                    "show_binary": False,
                },
                "PLLclkgen_disEOM": {
                    "bits": 1,
                    "position": [("PeriCfg0", "2", "0")],
                    "info": "{0} disables output clocks for EOM. Debugging use only.\nWhen {0} is high, the following clocks are disabled:\n - clk5g12EOMp\n - clk5g12EOMn",
                    "show_binary": False,
                },
                "PLLclkgen_disSER": {
                    "bits": 1,
                    "position": [("PeriCfg0", "3", "0")],
                    "info": "{0} disables output clocks for serializer, active high. Debugging use only.\nWhen {0} is high, the following clocks are disabled:\n - clk2g56S\n - clk2g56SN\n - clk5g12S\n - clk5g12SN",
                    "show_binary": False,
                },
                "PLLclkgen_disVCO": {
                    "bits": 1,
                    "position": [("PeriCfg0", "4", "0")],
                    "info": "{0} disables VCO output buffer (associated with clk5g12lshp, clk5g12lshn), active high. clk5g12lsh is the output clock of the first input buffer in prescaler, and the source clock for all output clocks. Once disabled, all output clocks are disabled. Debugging use only.",
                    "show_binary": False,
                },
                "CLKSel": {
                    "bits": 1,
                    "position": [("PeriCfg0", "5", "0")],
                    "info": "{0} selects the PLL clock or off-chip clock for TDC and readout. Debug use only.\n - Low: use off-chip clocks for TDC and readout\n - High: use PLL clocks for TDC and readout",
                    "show_binary": False,
                },
                "PLL_FBDiv_clkTreeDisable": {
                    "bits": 1,
                    "position": [("PeriCfg0", "6", "0")],
                    "info": "Disable the feedback divider, active high. Debugging use only.\n - 0b0: all output clocks with different frequencies (40MHz-2.56GHz) are enabled.\n - 0b1 The input clk2G56 from the prescaler and all output clocks are disabled.",
                    "show_binary": False,
                },
                "PLL_FBDiv_skip": {
                    "bits": 1,
                    "position": [("PeriCfg0", "7", "0")],
                    "info": "{0} adjusts the phase of the output clk1G28 of the freqPrescaler in the feedback divider (N=64) by one skip from low to high. Debugging use only.",
                    "show_binary": False,
                },
                "PLL_BiasGen_CONFIG": {
                    "bits": 4,
                    "position": [("PeriCfg1", "3-0", "3-0")],
                    "info": "Charge pump bias current selection, [0 : 8 : 120] uA. Debugging use only",
                    "show_binary": False,
                },
                "PLL_CONFIG_I_PLL": {
                    "bits": 4,
                    "position": [("PeriCfg1", "7-4", "3-0")],
                    "info": "Bias current selection of the I-filter unit cell in PLL mode [0 : 1.1 : 8] uA. Debugging use only.",
                    "show_binary": False,
                },
                "PLL_CONFIG_P_PLL": {
                    "bits": 4,
                    "position": [("PeriCfg2", "3-0", "3-0")],
                    "info": "Bias current selection of the P-filter unit cell in PLL mode [0 : 5.46 : 82] uA. Debugging use only.",
                    "show_binary": False,
                },
                "PLL_R_CONFIG": {
                    "bits": 4,
                    "position": [("PeriCfg2", "7-4", "3-0")],
                    "info": "Resistor selection of the P-path in PLL mode [R = 1/2 * 79.8k / CONFIG] Ohm. Debugging use only.",
                    "show_binary": False,
                },
                "PLL_vcoDAC": {
                    "bits": 4,
                    "position": [("PeriCfg3", "3-0", "3-0")],
                    "info": "Bias current selection of the VCO core [0 : 0.470 : 7.1] mA. Debugging use only.",
                    "show_binary": False,
                },
                "PLL_vcoRailMode": {
                    "bits": 1,
                    "position": [("PeriCfg3", "4", "0")],
                    "info": "Output rail-to-rail mode selection of the VCO, active low. Debugging use only.\n - 0b0: rail-to-rail output\n - 0b1: CML output",
                    "show_binary": False,
                },
                "PLL_ENABLEPLL": {
                    "bits": 1,
                    "position": [("PeriCfg3", "5", "0")],
                    "info": "Enable PLL mode, active high. Debugging use only.",
                    "show_binary": False,
                },
                "VrefGen_PD": {
                    "bits": 1,
                    "position": [("PeriCfg3", "7", "0")],
                    "info": "Power down voltage reference generator, active high.\n - High: the voltage reference generator is down\n - Low: the voltage reference generator is up",
                    "show_binary": False,
                },
                "PS_CPCurrent": {
                    "bits": 4,
                    "position": [("PeriCfg4", "3-0", "3-0")],
                    "info": "Charge pump current control bits, range from 0 to 15 uA for charge and discharge. Debugging use only.",
                    "show_binary": False,
                },
                "PS_CapRst": {
                    "bits": 1,
                    "position": [("PeriCfg4", "4", "0")],
                    "info": "Reset the control voltage of DLL to power supply, active high. Debugging use only.",
                    "show_binary": False,
                },
                "PS_Enable": {
                    "bits": 1,
                    "position": [("PeriCfg4", "5", "0")],
                    "info": "{0} enables DLL, active high. Debugging use only.",
                    "show_binary": False,
                },
                "PS_ForceDown": {
                    "bits": 1,
                    "position": [("PeriCfg4", "6", "0")],
                    "info": "Force to pull down the output of the phase detector, active high. Debugging use only.",
                    "show_binary": False,
                },
                "TS_PD": {
                    "bits": 1,
                    "position": [("PeriCfg4", "7", "0")],
                    "info": "Power down the temperature sensor, active high.\n - High: the temperature sensor is down\n - Low: the temperature sensor is up",
                    "show_binary": False,
                },
                "PS_PhaseAdj": {
                    "bits": 8,
                    "position": [("PeriCfg5", "7-0", "7-0")],
                    "info": "Phase selecting control bits, {0}[7:3] for coarse, {0}[2:0] for fine",
                    "show_binary": False,
                },
                "RefStrSel": {
                    "bits": 8,
                    "position": [("PeriCfg6", "7-0", "7-0")],
                    "info": "TDC reference strobe selection",
                    "show_binary": False,
                },
                "CLK40_EnRx": {
                    "bits": 1,
                    "position": [("PeriCfg7", "0", "0")],
                    "info": "Enable the Rx for the 40 MHz reference clock, active high.",
                    "show_binary": False,
                },
                "CLK40_EnTer": {
                    "bits": 1,
                    "position": [("PeriCfg7", "1", "0")],
                    "info": "Enable internal termination of the Rx for the 40 MHz reference clock, active high.",
                    "show_binary": False,
                },
                "CLK40_Equ": {
                    "bits": 2,
                    "position": [("PeriCfg7", "3-2", "1-0")],
                    "info": "Equalization strength of the Rx for the 40 MHz reference clock.\n - 0b00: equalization is turned off\n - 0b11: maximal equalization",
                    "show_binary": "New Line",
                },
                "CLK40_InvData": {
                    "bits": 1,
                    "position": [("PeriCfg7", "4", "0")],
                    "info": "Inverting data of the Rx for the 40 MHz reference clock, active high.",
                    "show_binary": False,
                },
                "CLK40_SetCM": {
                    "bits": 1,
                    "position": [("PeriCfg7", "5", "0")],
                    "info": "Set common voltage of the Rx for the 40 MHz reference clock to ½ vdd, active high.",
                    "show_binary": False,
                },
                "GRO_Start": {"bits": 1, "position": [("PeriCfg7", "6", "0")], "info": "GROStart, active high", "show_binary": False},
                "GRO_TOARST_N": {
                    "bits": 1,
                    "position": [("PeriCfg7", "7", "0")],
                    "info": "GRO TOA reset, active low",
                    "show_binary": False,
                },
                "CLK1280_EnRx": {
                    "bits": 1,
                    "position": [("PeriCfg8", "0", "0")],
                    "info": "Enable the Rx for the 1.26 GHz clock, active high.",
                    "show_binary": False,
                },
                "CLK1280_EnTer": {
                    "bits": 1,
                    "position": [("PeriCfg8", "1", "0")],
                    "info": "Enable the internal termination of the Rx for the 1.28 GHz clock, active high.",
                    "show_binary": False,
                },
                "CLK1280_Equ": {
                    "bits": 2,
                    "position": [("PeriCfg8", "3-2", "1-0")],
                    "info": "Equalization strength of the Rx for the 1.28 GHz clock.\n - 0b00: equalization is turned off\n - 0b11: maximal equalization",
                    "show_binary": "New Line",
                },
                "CLK1280_InvData": {
                    "bits": 1,
                    "position": [("PeriCfg8", "4", "0")],
                    "info": "Inverting data of the Rx for the 1.28 GHz clock, active high.",
                    "show_binary": False,
                },
                "CLK1280_SetCM": {
                    "bits": 1,
                    "position": [("PeriCfg8", "5", "0")],
                    "info": "Set common voltage of the Rx for the 1.28 GHz clock to  ½ vdd, active high.",
                    "show_binary": False,
                },
                "GRO_TOA_CK": {"bits": 1, "position": [("PeriCfg8", "6", "0")], "info": "GRO TOA clock", "show_binary": False},
                "GRO_TOA_Latch": {"bits": 1, "position": [("PeriCfg8", "7", "0")], "info": "GRO TOA latch clock", "show_binary": False},
                "FC_EnRx": {
                    "bits": 1,
                    "position": [("PeriCfg9", "0", "0")],
                    "info": "Enable the Rx for the fast command, active high.",
                    "show_binary": False,
                },
                "FC_EnTer": {
                    "bits": 1,
                    "position": [("PeriCfg9", "1", "0")],
                    "info": "Enable the internal termination of the Rx for the fast command, active high.",
                    "show_binary": False,
                },
                "FC_Equ": {
                    "bits": 2,
                    "position": [("PeriCfg9", "3-2", "1-0")],
                    "info": "Equalization strength of the Rx for the fast command.\n - 0b00: equalization is turned off\n - 0b11: maximal equalization",
                    "show_binary": "New Line",
                },
                "FC_InvData": {
                    "bits": 1,
                    "position": [("PeriCfg9", "4", "0")],
                    "info": "Inverting data of the Rx for the fast command, active high",
                    "show_binary": False,
                },
                "FC_SetCM": {
                    "bits": 1,
                    "position": [("PeriCfg9", "5", "0")],
                    "info": "Set common voltage of the Rx for the fast command to  ½ vdd, active high.",
                    "show_binary": False,
                },
                "GRO_TOTRST_N": {
                    "bits": 1,
                    "position": [("PeriCfg9", "6", "0")],
                    "info": "GRO TOT reset, active low",
                    "show_binary": False,
                },
                "GRO_TOT_CK": {"bits": 1, "position": [("PeriCfg9", "7", "0")], "info": "GRO TOT clock", "show_binary": False},
                "BCIDoffset": {
                    "bits": 12,
                    "position": [("PeriCfg10", "7-0", "7-0"), ("PeriCfg11", "3-0", "11-8")],
                    "info": "BCID when BCID is reset",
                    "show_binary": False,
                },
                "emptySlotBCID": {
                    "bits": 12,
                    "position": [("PeriCfg11", "7-4", "3-0"), ("PeriCfg12", "7-0", "11-4")],
                    "info": "empty BCID slot for synchronization",
                    "show_binary": False,
                },
                "readoutClockDelayPixel": {
                    "bits": 5,
                    "position": [("PeriCfg13", "4-0", "4-0")],
                    "info": "Phase delay of pixel readout clock, 780 ps a step",
                    "show_binary": False,
                },
                "asyAlignFastcommand": {
                    "bits": 1,
                    "position": [("PeriCfg13", "5", "0")],
                    "info": "Align fastCommand issued by I2C. Initializing the clock phase alignment process at its rising edge (sychronized by the 40 MHz PLL clock)",
                    "show_binary": False,
                },
                "asyLinkReset": {
                    "bits": 1,
                    "position": [("PeriCfg13", "6", "0")],
                    "info": "Link reset signal from I2C, active high.",
                    "show_binary": False,
                },
                "asyPLLReset": {
                    "bits": 1,
                    "position": [("PeriCfg13", "7", "0")],
                    "info": "Reset PLL from I2C, active low.",
                    "show_binary": False,
                },
                "readoutClockWidthPixel": {
                    "bits": 5,
                    "position": [("PeriCfg14", "4-0", "4-0")],
                    "info": "Positive pulse width of pixel clock, 780 ps a step",
                    "show_binary": False,
                },
                "asyResetChargeInj": {
                    "bits": 1,
                    "position": [("PeriCfg14", "5", "0")],
                    "info": "Reset charge injection module, active low.",
                    "show_binary": False,
                },
                "asyResetFastcommand": {
                    "bits": 1,
                    "position": [("PeriCfg14", "6", "0")],
                    "info": "Reset fastcommand from I2C, active low.",
                    "show_binary": False,
                },
                "asyResetGlobalReadout": {
                    "bits": 1,
                    "position": [("PeriCfg14", "7", "0")],
                    "info": "Reset globalReadout module, active low.",
                    "show_binary": False,
                },
                "readoutClockDelayGlobal": {
                    "bits": 5,
                    "position": [("PeriCfg15", "4-0", "4-0")],
                    "info": "Phase deloay of global readout clock, 780 ps a step",
                    "show_binary": False,
                },
                "asyResetLockDetect": {
                    "bits": 1,
                    "position": [("PeriCfg15", "5", "0")],
                    "info": "Reset lock detect, active low.",
                    "show_binary": False,
                },
                "asyStartCalibration": {
                    "bits": 1,
                    "position": [("PeriCfg15", "6", "0")],
                    "info": "Start PLL calibration process, active high.",
                    "show_binary": False,
                },
                "readoutClockWidthGlobal": {
                    "bits": 5,
                    "position": [("PeriCfg16", "4-0", "4-0")],
                    "info": "Positive pulse width of global readout clock, 780 ps a step",
                    "show_binary": False,
                },
                "LTx_AmplSel": {
                    "bits": 3,
                    "position": [("PeriCfg16", "7-5", "2-0")],
                    "info": "Left Tx amplitude selection.\n - 0b000: min amplitude (50mV)\n - 0b111: max amplitude (320mV)\nStep size is about 40mV",
                    "show_binary": "New Line",
                },
                "chargeInjectionDelay": {
                    "bits": 5,
                    "position": [("PeriCfg17", "4-0", "4-0")],
                    "info": "The charge injection delay to the 40MHz clock rising edge. Start from the rising edge to the 40 MHz clock, each step is 781 ps. The pulse width is fixed to 50 ns",
                    "show_binary": False,
                },
                "RTx_AmplSel": {
                    "bits": 3,
                    "position": [("PeriCfg17", "7-5", "2-0")],
                    "info": "Right Tx amplitude selection.\n - 0b000: min amplitude (50mV)\n - 0b111: max amplitude (320mV)\nStep size is about 40mV",
                    "show_binary": "New Line",
                },
                "disPowerSequence": {
                    "bits": 1,
                    "position": [("PeriCfg18", "0", "0")],
                    "info": "{0} disabled the power up sequence, active high.",
                    "show_binary": False,
                },
                "softBoot": {
                    "bits": 1,
                    "position": [("PeriCfg18", "1", "0")],
                    "info": "{0} resets the power sequencer controller, active high.",
                    "show_binary": False,
                },
                "fcSelfAlignEn": {
                    "bits": 1,
                    "position": [("PeriCfg18", "2", "0")],
                    "info": "Fast command decoder self-alignment mode enable, active high.\n - High: Self-alignment mode enabled\n - Low: manual alignment mode enabled",
                    "show_binary": False,
                },
                "fcClkDelayEn": {
                    "bits": 1,
                    "position": [("PeriCfg18", "3", "0")],
                    "info": "Fast command decoder self-alignment mode enable, active high.\n - High: Self-alignment mode enabled\n - Low: manual alignment mode enabled",
                    "show_binary": False,
                },
                "fcDataDelayEn": {
                    "bits": 1,
                    "position": [("PeriCfg18", "4", "0")],
                    "info": "Enable data delay in fast command manual alignment mode, active high",
                    "show_binary": False,
                },
                "onChipL1AConf": {
                    "bits": 2,
                    "position": [("PeriCfg18", "6-5", "1-0")],
                    "info": "On-chip L1A mode:\n - 0b0x: on-chip L1A disable\n - 0b10: periodic L1A\n - 0b11: random L1A",
                    "show_binary": "New Line",
                },
                "disLTx": {"bits": 1, "position": [("PeriCfg18", "7", "0")], "info": "Left Tx disable, active high", "show_binary": False},
                "disScrambler": {
                    "bits": 1,
                    "position": [("PeriCfg19", "0", "0")],
                    "info": "Disable scrambler:\n - Low: scrambler enabled\n - High: scrambler disabled",
                    "show_binary": False,
                },
                "linkResetTestPattern": {
                    "bits": 1,
                    "position": [("PeriCfg19", "1", "0")],
                    "info": "Link reset test pattern selection:\n - 0: PRBS\n - 1: fixed pattern",
                    "show_binary": False,
                },
                "serRateLeft": {
                    "bits": 2,
                    "position": [("PeriCfg19", "3-2", "1-0")],
                    "info": "Data rate selection of the left data port:\n - 0b00: 320 Mbps\n - 0b01: 640 Mbps\n - 0b10: 1280 Mbps",
                    "show_binary": "New Line",
                },
                "serRateRight": {
                    "bits": 2,
                    "position": [("PeriCfg19", "5-4", "1-0")],
                    "info": "Data rate selection of the right data port:\n - 0b00: 320 Mbps\n - 0b01: 640 Mbps\n - 0b10: 1280 Mbps",
                    "show_binary": "New Line",
                },
                "singlePort": {
                    "bits": 1,
                    "position": [("PeriCfg19", "6", "0")],
                    "info": "Enable single port or both ports:\n - Low: use both left and right serial ports\n - use right serial port only",
                    "show_binary": False,
                },
                "disRTx": {"bits": 1, "position": [("PeriCfg19", "7", "0")], "info": "Right Tx disable, active high", "show_binary": False},
                "mergeTriggerData": {
                    "bits": 1,
                    "position": [("PeriCfg20", "0", "0")],
                    "info": "Merge trigger and data in a port:\n - Low: trigger and data in separate port, only valid when singlePort os Low\n - High: trigger and data are merged in serial port",
                    "show_binary": False,
                },
                "triggerGranularity": {
                    "bits": 3,
                    "position": [("PeriCfg20", "3-1", "2-0")],
                    "info": "The trigger data size varies from 0, 1, 2, 4, 8, 16\n - 0: trigger data size is 0\n - 1: trigger data size is 1",
                    "show_binary": False,
                },
                "EFuse_TCKHP": {
                    "bits": 4,
                    "position": [("PeriCfg20", "7-4", "3-0")],
                    "info": "The register controlling the SCLK pulse width, ranges from 3 us to 10 us with step of 0.5us. The default value is 4, corresponding to 5 us pulse width. Debugging use only.",
                    "show_binary": False,
                },
                "EFuse_EnClk": {
                    "bits": 1,
                    "position": [("PeriCfg21", "0", "0")],
                    "info": "EFuse clock enable.\n - High: enables the clock of the EFuse controller\n - Low: disables the clock of the EFuse controller",
                    "show_binary": False,
                },
                "EFuse_Mode": {
                    "bits": 2,
                    "position": [("PeriCfg21", "2-1", "1-0")],
                    "info": "Operation mode of the eFuse:\n - 0b01: programming mode\n - 0b10: reading mode",
                    "show_binary": False,
                },
                "EFuse_Rstn": {
                    "bits": 1,
                    "position": [("PeriCfg21", "3", "0")],
                    "info": "Reset signal of the uFuse controller, active low",
                    "show_binary": False,
                },
                "EFuse_Start": {
                    "bits": 1,
                    "position": [("PeriCfg21", "4", "0")],
                    "info": "Start signal of the eFuse programming. A positive pulse will start programming.",
                    "show_binary": False,
                },
                "EFuse_Bypass": {
                    "bits": 1,
                    "position": [("PeriCfg21", "5", "0")],
                    "info": "Bypass eFuse\n - 0b0: eFuse output Q[31-0] is output\n - 0b1: eFuse raw data form I2C (EFuse_Prog) is output.",
                    "show_binary": False,
                },
                "EFuse_Prog": {
                    "bits": 32,
                    "position": [
                        ("PeriCfg22", "7-0", "7-0"),
                        ("PeriCfg23", "7-0", "15-8"),
                        ("PeriCfg24", "7-0", "23-16"),
                        ("PeriCfg25", "7-0", "31-24"),
                    ],
                    "info": "Data to be written into EFuse",
                    "show_binary": False,
                },
                "linkResetFixedPattern": {
                    "bits": 32,
                    "position": [
                        ("PeriCfg26", "7-0", "7-0"),
                        ("PeriCfg27", "7-0", "15-8"),
                        ("PeriCfg28", "7-0", "23-16"),
                        ("PeriCfg29", "7-0", "31-24"),
                    ],
                    "info": "User-specified pattern to be sent during link reset, LSB-first",
                    "show_binary": False,
                },
                "lfLockThrCounter": {
                    "bits": 4,
                    "position": [("PeriCfg30", "3-0", "3-0")],
                    "info": "If the number of instantLock is true for 256 (1 << 8) in a row, the PLL is locked in the initial status.",
                    "show_binary": False,
                },
                "lfReLockThrCounter": {
                    "bits": 4,
                    "position": [("PeriCfg30", "7-4", "3-0")],
                    "info": "If the number of instatLock is true for 256 (1 << 8) in a row, the PLL is relocked before the unlock status is confirmed.",
                    "show_binary": False,
                },
                "lfUnLockThrCounter": {
                    "bits": 4,
                    "position": [("PeriCfg31", "3-0", "3-0")],
                    "info": "If the number of instantLock is false for 256 (1 << 8) in a row, the PLL is unlocked.",
                    "show_binary": False,
                },
                "TDCClockTest": {
                    "bits": 1,
                    "position": [("PeriCfg31", "4", "0")],
                    "info": "The TDC clock testing enable.\n - High: sending TDC clock at the left serial port\n - Low: sending left serializer data at the left port",
                    "show_binary": False,
                },
                "TDCStrobeTest": {
                    "bits": 1,
                    "position": [("PeriCfg31", "5", "0")],
                    "info": "The TDC reference strobe testing enable.\n - High: sending TDC reference strobe at the right serial port\n - Low: sending right serializer data at the right port",
                    "show_binary": False,
                },
            },
            "Peripheral Status": {  # Register Block
                "PS_Lat": {
                    "bits": 1,
                    "position": [("PeriSta0", "7", "0")],
                    "info": "Phase Shifter late",
                    "show_binary": False,
                    "read_only": True,
                },
                "AFCcalCap": {
                    "bits": 6,
                    "position": [("PeriSta0", "6-1", "5-0")],
                    "info": "AFC capacitance",
                    "show_binary": False,
                    "read_only": True,
                },
                "AFCBusy": {
                    "bits": 1,
                    "position": [("PeriSta0", "0", "0")],
                    "info": "AFC busy",
                    "show_binary": False,
                    "read_only": True,
                },
                "fcAlignFinalState": {
                    "bits": 4,
                    "position": [("PeriSta1", "7-4", "3-0")],
                    "info": "fast command alignment FSM state",
                    "show_binary": False,
                    "read_only": True,
                },
                "controllerState": {
                    "bits": 4,
                    "position": [("PeriSta1", "3-0", "3-0")],
                    "info": "global control FSM",
                    "show_binary": False,
                    "read_only": True,
                },
                "fcAlignStatus": {
                    "bits": 4,
                    "position": [("PeriSta2", "7-4", "3-0")],
                    "info": "fast command alignment status",
                    "show_binary": False,
                    "read_only": True,
                },
                "fcBitAlignError": {
                    "bits": 1,
                    "position": [("PeriSta2", "0", "0")],
                    "info": "fast command bit alignment error",
                    "show_binary": False,
                    "read_only": True,
                },
                "invalidFCCount": {
                    "bits": 12,
                    "position": [("PeriSta4", "3-0", "11-8"), ("PeriSta3", "7-0", "7-0")],
                    "info": "?",
                    "show_binary": False,
                    "read_only": True,
                },
                "pllUnlockCount": {
                    "bits": 12,
                    "position": [("PeriSta5", "7-0", "11-4"), ("PeriSta4", "7-4", "3-0")],
                    "info": "?",
                    "show_binary": False,
                    "read_only": True,
                },
                "EFuseQ": {
                    "bits": 32,
                    "position": [
                        ("PeriSta9", "7-0", "31-24"),
                        ("PeriSta8", "7-0", "23-16"),
                        ("PeriSta7", "7-0", "15-8"),
                        ("PeriSta6", "7-0", "7-0"),
                    ],
                    "info": "32-bit EFuse output",
                    "show_binary": False,
                    "read_only": True,
                },
            },
            "Pixel Config": {  # Register Block
                "CLSel": {
                    "bits": 2,
                    "position": [("PixCfg0", "1-0", "1-0")],
                    "info": "{0} selects the load capacitance of the preamp first stage. Debugging use only.\n - 0b00: 0 fC\n - 0b01: 80 fC\n - 0b10: 80 fC\n - 0b11: 160 fC",
                    "show_binary": True,
                },
                "IBSel": {
                    "bits": 3,
                    "position": [("PixCfg0", "4-2", "2-0")],
                    "info": "{0} sets the bias current of the input transistor in the preamp.\n - 0b000: I1\n - 0b001, 0b010, 0b100: I2\n - 0b011, 0b110, 0b101: I3\n - 0b111: I4\nI1 > I2 > I3 > I4",
                    "show_binary": True,
                },
                "RFSel": {
                    "bits": 2,
                    "position": [("PixCfg0", "6-5", "1-0")],
                    "info": "{0} sets the feedback resistance.\n - 0b00: 20 kOHm\n - 0b01: 10 kOHm\n - 0b10: 5.7 kOHm\n - 0b11: 4.4 kOHm",
                    "show_binary": True,
                },
                "HysSel": {
                    "bits": 4,
                    "position": [("PixCfg2", "3-0", "3-0")],
                    "info": "{0} sets the hysteresis voltage.\n - 0b0000: Vhys1\n - 0b0001: Vhys2\n - 0b0011: Vhys3\n - 0b0111: Vhys4\n - 0b1111: Vhys5\nVhys1 > Vhys2 > Vhys3 > Vhys4 = Vhys5 = 0",
                    "show_binary": True,
                },
                "PD_DACDiscri": {
                    "bits": 1,
                    "position": [("PixCfg2", "4", "0")],
                    "info": "{0} powers down the DAC and the discriminator in pixels.\nWhen {0} is High, the DAC and the discriminator are powered down.",
                    "show_binary": False,
                },
                "QSel": {
                    "bits": 5,
                    "position": [("PixCfg1", "4-0", "4-0")],
                    "info": "{0} selects the injected charge. From 1 fC(0b00000) to 32 fC(0b11111).",
                    "show_binary": False,
                },
                "QInjEn": {
                    "bits": 1,
                    "position": [("PixCfg1", "5", "0")],
                    "info": "{0} enables the charge injection of the respective pixel.\nWhen {0} is High, the charge injection is active.",
                    "show_binary": False,
                },
                "autoReset_TDC": {
                    "bits": 1,
                    "position": [("PixCfg6", "5", "0")],
                    "info": "{0} defines if the TDC automatically resets the controller for every clock period.",
                    "show_binary": False,
                },
                "enable_TDC": {
                    "bits": 1,
                    "position": [("PixCfg6", "7", "0")],
                    "info": "{0} enables the TDC.\n - 0b1: enable TDC conversion\n - 0b0: disable TDC conversion",
                    "show_binary": False,
                },
                "level_TDC": {
                    "bits": 3,
                    "position": [("PixCfg6", "3-1", "2-0")],
                    "info": "{0} sets the bit width of bubble tolerant in TDC encode (?). It is up to 0b011",
                    "show_binary": False,
                },
                "resetn_TDC": {
                    "bits": 1,
                    "position": [("PixCfg6", "6", "0")],
                    "info": "{0} resets the TDC encoder, active low.",
                    "show_binary": False,
                },
                "testMode_TDC": {
                    "bits": 1,
                    "position": [("PixCfg6", "4", "0")],
                    "info": "{0} enables test mode of TDC, active high.\nIn test mode, the TDC generates a fixed test pulse as input signal for test for every 25 ns.",
                    "show_binary": False,
                },
                "Bypass_THCal": {
                    "bits": 1,
                    "position": [("PixCfg3", "2", "0")],
                    "info": "{0} bypasses control of the in-pixel threshold calibration block.\n - 1: bypass the in-pixel threshold calibration block. DAC is applied to TH. Users can control the threshold voltage through DAC.\n - 0: calibrated threshold is applied to TH. TH = BL + TH_offset",
                    "show_binary": False,
                },
                "DAC": {
                    "bits": 10,
                    "position": [("PixCfg4", "7-0", "7-0"), ("PixCfg5", "1-0", "9-8")],
                    "info": "{0} sets the threshold when Bypass_THCal is High: TH = DAC",
                    "show_binary": False,
                },
                "TH_offset": {
                    "bits": 6,
                    "position": [("PixCfg5", "7-2", "5-0")],
                    "info": "{0} sets the threshold offset for the calibrated baseline when Bypass_THCal is Low: TH = BL + TH_offset",
                    "show_binary": False,
                },
                "RSTn_THCal": {
                    "bits": 1,
                    "position": [("PixCfg3", "0", "0")],
                    "info": "Reset of threshold calibration block, active low.",
                    "show_binary": False,
                },
                "ScanStart_THCal": {
                    "bits": 1,
                    "position": [("PixCfg3", "4", "0")],
                    "info": "A rising edge of {0} initializes the threshold calibration",
                    "show_binary": False,
                },
                "BufEn_THCal": {
                    "bits": 1,
                    "position": [("PixCfg3", "1", "0")],
                    "info": "{0} enables the threshold clalibration buffer.\n - 0b1: enable the buffer between discriminator output and the TH_Ctrl\n - 0b0: disable the buffer between discriminator output and the TH_Ctrl",
                    "show_binary": False,
                },
                "CLKEn_THCal": {
                    "bits": 1,
                    "position": [("PixCfg3", "3", "0")],
                    "info": "{} enables the clock for threshold calibration. It is only used when the threshold calibration block is bypassed.\n - 0b1: enable the clock for measuring average discriminator output\n - 0b0: disable the clock. Measurement of the average discriminator output is not available.",
                    "show_binary": False,
                },
                "workMode": {
                    "bits": 2,
                    "position": [("PixCfg7", "4-3", "1-0")],
                    "info": "{0} selects the readout work mode.\n - 0b00: normal\n - 0b01: self test, periodic trigger fixed TDC data\n - 0b10: self test, random TDC data\n - 11: reserved",
                    "show_binary": True,
                },
                "L1Adelay": {
                    "bits": 9,
                    "position": [("PixCfg8", "7", "0"), ("PixCfg9", "7-0", "8-1")],
                    "info": "{0} sets the L1A latency",
                    "show_binary": False,
                },
                "disDataReadout": {
                    "bits": 1,
                    "position": [("PixCfg7", "1", "0")],
                    "info": "{0} disables the signal of the TDC data readout.\n - 0b1: disable the TDC data readout of the current pixel\n - 0b0: enable the TDC data readout of the current pixel",
                    "show_binary": False,
                },
                "disTrigPath": {
                    "bits": 1,
                    "position": [("PixCfg7", "2", "0")],
                    "info": "{0} disables the signal of the trigger readout.\n - 0b1: disable the trigger readout of the current pixel\n - 0b0: enable the trigger readout of the current pixel",
                    "show_binary": False,
                },
                "upperTOATrig": {
                    "bits": 10,
                    "position": [("PixCfg21", "7-0", "7-0"), ("PixCfg22", "1-0", "9-8")],
                    "info": "TOA upper threshold for the trigger readout",
                    "show_binary": False,
                },
                "lowerTOATrig": {
                    "bits": 10,
                    "position": [("PixCfg19", "7-6", "1-0"), ("PixCfg20", "7-0", "9-2")],
                    "info": "TOA lower threshold for the trigger readout",
                    "show_binary": False,
                },
                "upperTOTTrig": {
                    "bits": 9,
                    "position": [("PixCfg23", "7-3", "4-0"), ("PixCfg24", "3-0", "8-5")],
                    "info": "TOT upper threshold for the trigger readout",
                    "show_binary": False,
                },
                "lowerTOTTrig": {
                    "bits": 9,
                    "position": [("PixCfg22", "7-2", "5-0"), ("PixCfg23", "2-0", "8-6")],
                    "info": "TOT lower threshold for the trigger readout",
                    "show_binary": False,
                },
                "upperCalTrig": {
                    "bits": 10,
                    "position": [("PixCfg18", "7-4", "3-0"), ("PixCfg19", "5-0", "9-4")],
                    "info": "Cal upper threshold for the trigger readout",
                    "show_binary": False,
                },
                "lowerCalTrig": {
                    "bits": 10,
                    "position": [("PixCfg17", "7-2", "5-0"), ("PixCfg18", "3-0", "9-6")],
                    "info": "Cal lower threshold for the trigger readout",
                    "show_binary": False,
                },
                "upperTOA": {
                    "bits": 10,
                    "position": [("PixCfg13", "7-6", "1-0"), ("PixCfg14", "7-0", "9-2")],
                    "info": "TOA upper threshold for the TDC data readout",
                    "show_binary": False,
                },
                "lowerTOA": {
                    "bits": 10,
                    "position": [("PixCfg12", "7-4", "3-0"), ("PixCfg13", "5-0", "9-4")],
                    "info": "TOA lower threshold for the TDC data readout",
                    "show_binary": False,
                },
                "upperTOT": {
                    "bits": 9,
                    "position": [("PixCfg16", "7-1", "6-0"), ("PixCfg17", "1-0", "8-7")],
                    "info": "TOT upper threshold for the TDC data readout",
                    "show_binary": False,
                },
                "lowerTOT": {
                    "bits": 9,
                    "position": [("PixCfg15", "7-0", "7-0"), ("PixCfg16", "0", "8")],
                    "info": "TOT lower threshold for the TDC data readout",
                    "show_binary": False,
                },
                "upperCal": {
                    "bits": 10,
                    "position": [("PixCfg11", "7-2", "5-0"), ("PixCfg12", "3-0", "9-6")],
                    "info": "Cal upper threshold for the TDC data readout",
                    "show_binary": False,
                },
                "lowerCal": {
                    "bits": 10,
                    "position": [("PixCfg10", "7-0", "7-0"), ("PixCfg11", "1-0", "9-8")],
                    "info": "Cal lower threshold for the TDC data readout",
                    "show_binary": False,
                },
                "addrOffset": {
                    "bits": 1,
                    "position": [("PixCfg7", "0", "0")],
                    "info": "{0} enables the circular buffer (CB) write address offset by the pixel ID, active high.\n - 0b1: enable the CB write address offset\n - 0b0: disable the CB write address offset",
                    "show_binary": False,
                },
                "selfTestOccupancy": {
                    "bits": 7,
                    "position": [("PixCfg8", "6-0", "6-0")],
                    "info": "Self-test data occupancy.\n - 1: 1%\n - 2: 2%\n - 5: 5%\n - 10: 10%",
                    "show_binary": False,
                },
            },
            "Pixel Status": {  # Register Block
                "ACC": {
                    "bits": 16,
                    "position": [("PixSta5", "7-0", "7-0"), ("PixSta6", "7-0", "15-8")],
                    "info": "Accumulator of the threshold calibration",
                    "show_binary": "New Line",
                    "read_only": True,
                },
                "ScanDone": {
                    "bits": 1,
                    "position": [("PixSta1", "0", "0")],
                    "info": "Scan done signal of the threshold calibration",
                    "show_binary": False,
                    "read_only": True,
                },
                "BL": {
                    "bits": 10,
                    "position": [("PixSta2", "7-0", "7-0"), ("PixSta3", "1-0", "9-8")],
                    "info": "Baseline obtained from threshold calibration",
                    "show_binary": False,
                    "read_only": True,
                },
                "NW": {
                    "bits": 4,
                    "position": [("PixSta1", "4-1", "3-0")],
                    "info": "Noise width from threshold calibration (expected less than 10)",
                    "show_binary": False,
                    "read_only": True,
                },
                "TH": {
                    "bits": 10,
                    "position": [("PixSta3", "7-6", "1-0"), ("PixSta4", "7-0", "9-2")],
                    "info": "10-bit threshold applied to the DAC input",
                    "show_binary": False,
                    "read_only": True,
                },
                "THState": {
                    "bits": 3,
                    "position": [("PixSta1", "7-5", "2-0")],
                    "info": "Threshold calibration state machine output",
                    "show_binary": False,
                    "read_only": True,
                },
                "PixelID": {
                    "bits": 8,
                    "position": [("PixSta0", "7-0", "7-0")],
                    "info": "Col[3:0],Row[3:0]",
                    "show_binary": True,
                    "read_only": True,
                },
                "PixelID-Col": {
                    "bits": 4,
                    "position": [("PixSta0", "7-4", "3-0")],
                    "info": "Col",
                    "show_binary": False,
                    "read_only": True,
                },
                "PixelID-Row": {
                    "bits": 4,
                    "position": [("PixSta0", "3-0", "3-0")],
                    "info": "Row",
                    "show_binary": False,
                    "read_only": True,
                },
            },
        }
    },
    "Waveform Sampler": {  # Address Space
        "Register Blocks": {
            "Config": {
                "CTRL": {
                    "bits": 2,
                    "position": [("regOut0D", "4-3", "1-0")],
                    "info": "Sampling MEM Effect Reduction",
                    "show_binary": "New Line",
                },
                "comp_cali": {
                    "bits": 3,
                    "position": [("regOut0D", "7-5", "2-0")],
                    "info": "Comparator calibration",
                    "show_binary": "New Line",
                },
                "DDT": {"bits": 16, "position": [("regOut0E", "7-0", "7-0"), ("regOut0F", "7-0", "15-8")], "info": "Time skew calibration"},
                "rd_addr": {
                    "bits": 10,
                    "position": [("regOut1C", "7-6", "1-0"), ("regOut1D", "7-0", "9-2")],
                    "info": "Memory read address",
                },
                "mem_rstn": {"bits": 1, "position": [("regOut1F", "0", "0")], "info": "Memory reset"},
                "en_clk": {"bits": 1, "position": [("regOut1F", "1", "0")], "info": "Enable signal for lock delivery from PLL"},
                "rd_en_I2C": {"bits": 1, "position": [("regOut1F", "2", "0")], "info": "read enable"},
                "clk_gen_rstn": {"bits": 1, "position": [("regOut1F", "3", "0")], "info": "ADC clock generation reset"},
                "sel3": {"bits": 1, "position": [("regOut1F", "5", "0")], "info": "on-chip/off-chip write enable selection"},
                "sel2": {"bits": 1, "position": [("regOut1F", "6", "0")], "info": "WS power-on/power-down mode selction"},
                "sel1": {"bits": 1, "position": [("regOut1F", "7", "0")], "info": "VGA/Bypass mode selction"},
            },
            "Status": {
                "dout": {
                    "bits": 14,
                    "position": [("regIn20", "7-2", "5-0"), ("regIn21", "7-0", "13-6")],
                    "info": "WS digital output. Data from the waveform sampler internal memory being pointed to by rd_addr",
                    "show_binary": "New Line",
                    "read_only": True,
                },
            },
        }
    },
}


efficient_block_lengths = {
    "ETROC2": {
        "Peripheral Config": 34,
        "Peripheral Status": 16,
        "Pixel Config": 32,
        "Pixel Status": 8,
    },
    "Waveform Sampler": {
        "Config": 32,
        "Status": 2,
    },
}


class ETROC2_Chip(Base_Chip):
    _indexer_info = {
        "vars": ["block", "column", "row", "broadcast"],
        "min": [None, 0, 0, 0],
        "max": [None, 15, 15, 1],  # Max is inclusive, i.e. the interval is defined as [min, max]
    }

    def __init__(
        self,
        etroc2_i2c_address,
        waveform_sampler_i2c_address,
        i2c_connection: I2C_Connection_Helper,
        logger: logging.Logger,
    ):
        super().__init__(
            chip_name="ETROC2",
            i2c_connection=i2c_connection,
            logger=logger,
            software_version=etroc2_version,
            register_model=register_model,
            register_decoding=register_decoding,
            indexer_info=self._indexer_info,
        )

        self._etroc2_i2c_address = etroc2_i2c_address
        self._waveform_sampler_i2c_address = waveform_sampler_i2c_address

        address_space: Address_Space_Controller = self._address_space["ETROC2"]
        address_space.update_i2c_address(self._etroc2_i2c_address)

        address_space: Address_Space_Controller = self._address_space["Waveform Sampler"]
        address_space.update_i2c_address(self._waveform_sampler_i2c_address)

    @property
    def etroc2_i2c_address(self) -> int:
        return self._etroc2_i2c_address

    @etroc2_i2c_address.setter
    def etroc2_i2c_address(self, address: int):
        self._etroc2_i2c_address = address

        address_space: Address_Space_Controller = self._address_space["ETROC2"]
        address_space.update_i2c_address(self._etroc2_i2c_address)

    @property
    def waveform_sampler_i2c_address(self) -> int:
        return self._waveform_sampler_i2c_address

    @waveform_sampler_i2c_address.setter
    def waveform_sampler_i2c_address(self, address: int):
        self._waveform_sampler_i2c_address = address

        address_space: Address_Space_Controller = self._address_space["Waveform Sampler"]
        address_space.update_i2c_address(self._waveform_sampler_i2c_address)

    @property
    def broadcast(self) -> bool:
        value = self._indexer_vars['broadcast']['variable']
        if value == 0:
            return False
        else:
            return True

    @broadcast.setter
    def broadcast(self, value: bool):
        if value:
            self.set_indexer('broadcast', 1)
        else:
            self.set_indexer('broadcast', 0)

    @property
    def row(self) -> int:
        return self._indexer_vars['row']['variable']

    @row.setter
    def row(self, value: int):
        self.set_indexer('row', value)

    @property
    def col(self) -> int:
        return self._indexer_vars['column']['variable']

    @col.setter
    def col(self, value: int):
        self.set_indexer('column', value)

    #  Since there is the broadcast feature, we can not allow to write a full adress space
    # because the broadcast feature would overwrite previous addresses, so we write in blocks
    # since they do not cover the broadcast range
    def write_all_address_space(self, address_space_name: str, readback_check: bool = True, no_message: bool = True):
        if address_space_name == "ETROC2":
            if not no_message:
                self._logger.info("Writing full address space: {}".format(address_space_name))
            success = True
            for block in self._register_model[address_space_name]["Register Blocks"]:
                if not self.write_all_block(address_space_name, block, full_array=True, readback_check=readback_check, no_message=True):
                    success = False
            return success
        else:
            return super().write_all_address_space(address_space_name, readback_check=readback_check, no_message=no_message)

    #  We need to overload the write block method so that we intercept the call for the broadcast feature
    def write_all_block(
        self, address_space_name: str, block_name: str, full_array: bool = False, readback_check: bool = True, no_message: bool = True
    ):
        if (
            address_space_name == "ETROC2"
            and "Indexer" in self._register_model[address_space_name]["Register Blocks"][block_name]
            and self.broadcast
        ):
            block_ref, params = self._gen_block_ref_from_indexers(
                address_space_name=address_space_name,
                block_name=block_name,
                full_array=False,  # Always specifically set to false since we always want to address a single "element" of the array due to the broadcast feature
            )
            params['broadcast'] = True

            if not no_message:
                self._logger.info(
                    "Broadcast writing block {} from address space {} of chip {}".format(block_ref, address_space_name, self._chip_name)
                )

            # Fetch the base address for the broadcast block array
            broadcast_base_address = etroc2_column_row_to_base_address(**params)

            address_space: Address_Space_Controller = self._address_space[address_space_name]
            block_info = address_space._blocks[block_ref]
            block_length = block_info["Length"]

            # Temporarily disable the read-only property on the broadcast address
            for offset in range(block_length):
                broadcast_address = broadcast_base_address + offset
                address_space._read_only_map[broadcast_address] = False

            return_status = address_space.write_memory_block(broadcast_base_address, block_length, readback_check=readback_check)

            # Re-enable the read-only on the broadcast address
            for offset in range(block_length):
                broadcast_address = broadcast_base_address + offset
                address_space._read_only_map[broadcast_address] = True

            # TODO: Validate broadcast write

            return return_status
        else:
            return super().write_all_block(
                address_space_name=address_space_name,
                block_name=block_name,
                full_array=full_array,
                readback_check=readback_check,
                no_message=no_message,
            )

    #  We need to overload the write register method so that we intercept the call for the broadcast feature
    def write_register(self, address_space_name: str, block_name: str, register: str, readback_check: bool = True, no_message: bool = True):
        if (
            address_space_name == "ETROC2"
            and "Indexer" in self._register_model[address_space_name]["Register Blocks"][block_name]
            and self.broadcast
        ):
            block_ref, params = self._gen_block_ref_from_indexers(
                address_space_name=address_space_name,
                block_name=block_name,
                full_array=False,
            )
            params['broadcast'] = True

            if not no_message:
                self._logger.info(
                    "Broadcast writing register {} from block {} of address space {} of chip {}".format(
                        register, block_ref, address_space_name, self._chip_name
                    )
                )

            # Fetch the base address for the broadcast block array
            broadcast_base_address = etroc2_column_row_to_base_address(**params)
            offset = self._register_model[address_space_name]["Register Blocks"][block_name]['Registers'][register]['offset']
            broadcast_address = broadcast_base_address + offset

            address_space: Address_Space_Controller = self._address_space[address_space_name]

            # Temporarily disable the read-only property on the broadcast address
            address_space._read_only_map[broadcast_address] = False

            return_status = address_space.write_memory_block(broadcast_address, 1, readback_check=readback_check)

            # Re-enable the read-only on the broadcast address
            address_space._read_only_map[broadcast_address] = True

            # TODO: Validate broadcast write

            return return_status
        else:
            return super().write_register(
                address_space_name=address_space_name,
                block_name=block_name,
                register=register,
                readback_check=readback_check,
                no_message=no_message,
            )

    #  We need to overload the write register method so that we intercept the call for the broadcast feature
    def write_decoded_value(
        self, address_space_name: str, block_name: str, decoded_value_name: str, write_check: bool = True, no_message: bool = False
    ):
        if (
            address_space_name == "ETROC2"
            and "Indexer" in self._register_model[address_space_name]["Register Blocks"][block_name]
            and self.broadcast
        ):
            value_info = self._register_decoding[address_space_name]['Register Blocks'][block_name][decoded_value_name]

            for position in value_info['position']:
                self.broadcast = 1
                register = position[0]
                self.write_register(address_space_name, block_name, register, write_check, no_message=no_message)
        else:
            return super().write_decoded_value(
                address_space_name=address_space_name,
                block_name=block_name,
                decoded_value_name=decoded_value_name,
                write_check=write_check,
                no_message=no_message,
            )

    def write_all_efficient(self, readback_check: bool = True):
        """This write function will only write the named register addresses in the ETROC2 manual.
        There are many addresses which are not named and as a result are not written. In principle,
        these addresses are not used for anything and may not even be implemented in the chip,
        but by using this function we are essentially not setting these unnamed addresses"""
        for address_space_name in self._address_space:
            address_space: Address_Space_Controller = self._address_space[address_space_name]
            for block_name in address_space._blocks:
                if (
                    block_name in register_model[address_space_name]["Register Blocks"]
                    and "Indexer" in register_model[address_space_name]["Register Blocks"][block_name]
                ):
                    continue

                if block_name not in register_model[address_space_name]["Register Blocks"]:
                    length = efficient_block_lengths[address_space_name][block_name.split(":")[0]]
                else:
                    length = efficient_block_lengths[address_space_name][block_name]
                address_space.write_memory_block(address_space._blocks[block_name]["Base Address"], length, readback_check=readback_check)

                # No need to write the SEU counters, but the code block to do so is below in case it is seen to be needed
                # if address_space_name == "ETROC2" and block_name == "Peripheral Status":
                #    address_space.write_memory_block(0x0120, 4)

    def read_all_efficient(self):
        """This read function will only read the named register addresses in the ETROC2 manual.
        There are many addresses which are not named and as a result are not read. In principle,
        these addresses are not used for anything and may not even be implemented in the chip,
        but by using this function we are essentially blind to what is happening on these unnamed
        addresses"""
        for address_space_name in self._address_space:
            address_space: Address_Space_Controller = self._address_space[address_space_name]
            for block_name in address_space._blocks:
                if (
                    block_name in register_model[address_space_name]["Register Blocks"]
                    and "Indexer" in register_model[address_space_name]["Register Blocks"][block_name]
                ):
                    continue

                if block_name not in register_model[address_space_name]["Register Blocks"]:
                    length = efficient_block_lengths[address_space_name][block_name.split(":")[0]]
                else:
                    length = efficient_block_lengths[address_space_name][block_name]
                address_space.read_memory_block(address_space._blocks[block_name]["Base Address"], length)

                # Add reading of the SEU counters
                if address_space_name == "ETROC2" and block_name == "Peripheral Status":
                    address_space.read_memory_block(0x0120, 4)
            # self.read_all_address_space(address_space)
