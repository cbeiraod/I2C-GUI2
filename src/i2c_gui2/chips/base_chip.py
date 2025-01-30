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

import itertools
import logging
import pickle

from ..i2c_connection_helper import I2C_Connection_Helper
from .address_space_controller import Address_Space_Controller


class Base_Chip:
    newid = itertools.count()

    def __init__(
        self,
        chip_name: str,
        i2c_connection: I2C_Connection_Helper,
        logger: logging.Logger,
        software_version: str = "",
        register_model=None,
        register_decoding=None,
        indexer_info=None,
    ):
        self._id = next(Base_Chip.newid)

        self._chip_name = chip_name
        self._unique_name = chip_name + "_{}".format(self._id)
        self._software_version = software_version

        self._i2c_connection = i2c_connection
        self._logger = logger

        self._address_space = {}
        self._register_model = register_model
        self._register_decoding = register_decoding

        self._enable_readback = True

        self._indexer_vars = {}
        if indexer_info is not None:
            self._build_indexer_vars(indexer_info)

        for address_space in self._register_model:
            # decoding = None
            # if address_space in self._register_decoding:
            #    decoding = self._register_decoding[address_space]
            self._register_address_space(address_space, None, self._register_model[address_space])  # , decoding)

    def __getitem__(self, index):
        address_space_name, block_name, register = index

        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=False,
        )

        return self._address_space[address_space_name][block_ref, register]

    def __setitem__(self, index, value):
        address_space_name, block_name, register = index

        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=False,
        )

        self._address_space[address_space_name][block_ref, register] = value

    @property
    def id(self):
        return self._id

    @property
    def enable_readback(self):
        return self._enable_readback

    @enable_readback.setter
    def enable_readback(self, value: bool):
        self._enable_readback = value

    def _build_indexer_vars(self, indexer_info):
        indexer_variables = indexer_info["vars"]
        variables_min = indexer_info["min"]
        variables_max = indexer_info["max"]

        if len(indexer_variables) != len(variables_min) or len(indexer_variables) != len(variables_max):
            raise RuntimeError(f"Lengths of control structures for the indexer of {self._chip_name} do not match")

        for idx in range(len(indexer_variables)):
            variable = indexer_variables[idx]
            minimum = variables_min[idx]
            maximum = variables_max[idx]

            if variable == "block" and minimum is None and maximum is None:
                continue

            if minimum is None and maximum is None:
                continue
            value = minimum
            if value is None:
                value = maximum

            self._indexer_vars[variable] = {"variable": value, "min": minimum, "max": maximum}

    def _register_address_space(self, name: str, address: int, address_space_model):
        if name in self._address_space:
            raise ValueError("An address space with the name '{}' already exists".format(name))

        size = address_space_model["Memory Size"]
        if "Address Bitlength" in address_space_model:
            address_bitlength = address_space_model["Address Bitlength"]
        else:
            address_bitlength = 8
        if "Word Bitlength" in address_space_model:
            word_bitlength = address_space_model["Word Bitlength"]
        else:
            word_bitlength = 8
        if "Address Endianness" in address_space_model:
            address_endianness = address_space_model["Address Endianness"]
        else:
            address_endianness = "big"
        if "Word Endianness" in address_space_model:
            word_endianness = address_space_model["Word Endianness"]
        else:
            word_endianness = "little"
        if "Read Type" in address_space_model:
            read_type = address_space_model["Read Type"]
        else:
            read_type = "Normal"
        if "Write Type" in address_space_model:
            write_type = address_space_model["Write Type"]
        else:
            write_type = "Normal"

        self._address_space[name] = Address_Space_Controller(
            name=name,
            i2c_address=address,
            address_space_size=size,
            logger=self._logger,
            i2c_connection=self._i2c_connection,
            address_bitlength=address_bitlength,
            address_endianness=address_endianness,
            word_bitlength=word_bitlength,
            word_endianness=word_endianness,
            read_type=read_type,
            write_type=write_type,
            address_space_map=address_space_model["Register Blocks"],
        )

    def _gen_block_ref_from_indexers(self, address_space_name: str, block_name: str, full_array: bool):
        block_ref = block_name
        params = {'block': block_name}

        if "Indexer" in self._register_model[address_space_name]["Register Blocks"][block_name] and not full_array:
            indexers = self._register_model[address_space_name]["Register Blocks"][block_name]["Indexer"]["vars"]
            min_vals = self._register_model[address_space_name]["Register Blocks"][block_name]["Indexer"]["min"]
            max_vals = self._register_model[address_space_name]["Register Blocks"][block_name]["Indexer"]["max"]

            block_ref = ""
            params = {}
            for idx in range(len(indexers)):
                indexer = indexers[idx]
                min_val = min_vals[idx]
                max_val = max_vals[idx]

                if block_ref != "":
                    block_ref += ":"

                if indexer == "block" and min_val is None and max_val is None:
                    block_ref += block_name
                    params[indexer] = block_name
                else:
                    val = self._indexer_vars[indexer]['variable']
                    if val == "":
                        val = 0
                    block_ref += f"{val}"
                    params[indexer] = val

        return block_ref, params

    def get_indexer_info(self, name):
        if name not in self._indexer_vars:
            return None, None, None
        return self._indexer_vars[name]['variable'], self._indexer_vars[name]['min'], self._indexer_vars[name]['max']

    # Promote this to a standalone function
    def get_indexer_array(self, indexer_info):
        indexer_variables = indexer_info["vars"]
        variables_min = indexer_info["min"]
        variables_max = indexer_info["max"]

        indexer_array = {}
        tmp = {}
        for idx in range(len(indexer_variables)):
            variable = indexer_variables[idx]
            if variable == "block":
                if len(indexer_array) == 0:
                    tmp[""] = {"arguments": ["{block}"]}
                else:
                    for tag in indexer_array:
                        tmp[tag] = {"arguments": indexer_array[tag]["arguments"] + ["{block}"]}
            else:
                minimum = variables_min[idx]
                maximum = variables_max[idx]

                if minimum is None and maximum is None:
                    continue

                if minimum is None or maximum is None:
                    if minimum is not None:
                        my_range = [minimum]
                    else:
                        my_range = [maximum]
                elif minimum == 0 and maximum == 1:
                    my_range = [False, True]
                else:
                    my_range = range(minimum, maximum)

                for value in my_range:
                    if len(indexer_array) == 0:
                        tmp["{}".format(value)] = {"arguments": ["{}".format(value)]}
                    else:
                        for tag in indexer_array:
                            if tag == "":
                                index = "{}".format(value)
                            else:
                                index = "{}_{}".format(tag, value)
                            tmp[index] = {"arguments": indexer_array[tag]["arguments"] + [value]}

            indexer_array = tmp
            tmp = {}

        return indexer_array

    def set_indexer(self, name, value):
        minVal = self._indexer_vars[name]['min']
        maxVal = self._indexer_vars[name]['max']
        if minVal is not None and maxVal is not None:
            if value < minVal:
                raise RuntimeError(f"The indexer '{name}' should not have a value smaller than {minVal}, tried to set {value}")
            if value > maxVal:
                raise RuntimeError(f"The indexer '{name}' should not have a value greater than {maxVal}, tried to set {value}")
        self._indexer_vars[name]['variable'] = value

    def read_all(self):
        for address_space in self._address_space:
            self.read_all_address_space(address_space)

    def write_all(self, readback_check: bool = True):
        success = True
        for address_space in self._address_space:
            if not self.write_all_address_space(address_space, readback_check=readback_check):
                success = False

        return success

    def read_all_address_space(self, address_space_name: str, no_message: bool = True):
        if not no_message:
            self._logger.info("Reading full address space: {}".format(address_space_name))
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        address_space.read_all()

    def write_all_address_space(self, address_space_name: str, readback_check: bool = True, no_message: bool = True):
        if not no_message:
            self._logger.info("Writing full address space: {}".format(address_space_name))
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        return address_space.write_all(readback_check=readback_check)

    def read_all_block(self, address_space_name: str, block_name: str, full_array: bool = False, no_message: bool = True):
        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=full_array,
        )

        if not no_message:
            self._logger.info(f"Reading block {block_ref} from address space {address_space_name} of chip {self._chip_name}")
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        address_space.read_block(block_ref)

    def write_all_block(
        self, address_space_name: str, block_name: str, full_array: bool = False, readback_check: bool = True, no_message: bool = True
    ):
        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=full_array,
        )

        if not no_message:
            self._logger.info(f"Writing block {block_ref} from address space {address_space_name} of chip {self._chip_name}")
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        return address_space.write_block(block_ref, readback_check=readback_check)

    def read_register(self, address_space_name: str, block_name: str, register: str, no_message: bool = True):
        self._logger.detailed_trace(f'Base_Chip::read_register("{address_space_name}", "{block_name}", "{register}", {no_message})')
        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=False,
        )
        # self._logger.detailed_trace(f'   Got block_ref={block_ref}')

        if not no_message:
            self._logger.info(
                "Reading register {} from block {} of address space {} of chip {}".format(
                    register, block_ref, address_space_name, self._chip_name
                )
            )
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        address_space.read_register(block_ref, register)

    def write_register(self, address_space_name: str, block_name: str, register: str, readback_check: bool = True, no_message: bool = True):
        self._logger.detailed_trace(
            f'Base_Chip::write_register("{address_space_name}", "{block_name}", "{register}", "{readback_check}", {no_message})'
        )
        block_ref, _ = self._gen_block_ref_from_indexers(
            address_space_name=address_space_name,
            block_name=block_name,
            full_array=False,
        )

        if not no_message:
            self._logger.info(
                "Writing register {} from block {} of address space {} of chip {}".format(
                    register, block_ref, address_space_name, self._chip_name
                )
            )
        address_space: Address_Space_Controller = self._address_space[address_space_name]
        return address_space.write_register(block_ref, register, readback_check=readback_check)

    def read_decoded_value(self, address_space_name: str, block_name: str, decoded_value_name: str, no_message: bool = False):
        value_info = self._register_decoding[address_space_name]['Register Blocks'][block_name][decoded_value_name]

        for position in value_info['position']:
            register = position[0]
            self.read_register(address_space_name, block_name, register, no_message=no_message)

    def write_decoded_value(
        self, address_space_name: str, block_name: str, decoded_value_name: str, write_check: bool = True, no_message: bool = False
    ):
        value_info = self._register_decoding[address_space_name]['Register Blocks'][block_name][decoded_value_name]

        for position in value_info['position']:
            register = position[0]
            self.write_register(address_space_name, block_name, register, write_check, no_message=no_message)

    def get_decoded_value(self, address_space_name: str, block_name: str, decoded_value_name: str):
        self._logger.detailed_trace(f'Base_Chip::get_decoded_value("{address_space_name}", "{block_name}", "{decoded_value_name}")')
        value_info = self._register_decoding[address_space_name]['Register Blocks'][block_name][decoded_value_name]

        value = 0
        for position in value_info['position']:
            register = position[0]
            if "-" in position[1]:
                use_bits_max, use_bits_min = position[1].split("-")
                position_bits = int(position[2].split("-")[1])
            else:
                use_bits_max = position[1]
                use_bits_min = position[1]
                position_bits = int(position[2])

            register_value = self.__getitem__((address_space_name, block_name, register))

            use_bits_min = int(use_bits_min)
            use_bits_max = int(use_bits_max)

            use_bit_mask = 0
            for i in range(use_bits_max + 1):
                if i >= use_bits_min and i <= use_bits_max:
                    use_bit_mask += 0x1 << i
            transform_value = (register_value & use_bit_mask) >> use_bits_min
            value += transform_value << position_bits

        return value

    def set_decoded_value(self, address_space_name: str, block_name: str, decoded_value_name: str, value: int):
        self._logger.detailed_trace(f'Base_Chip::set_decoded_value("{address_space_name}", "{block_name}", "{decoded_value_name}")')
        value_info = self._register_decoding[address_space_name]['Register Blocks'][block_name][decoded_value_name]

        bit_length = value_info['bits']
        value_bitmask = 0
        for i in range(bit_length):
            value_bitmask += 0x1 << i
        value = value & value_bitmask

        for position in value_info['position']:
            register = position[0]
            if "-" in position[1]:
                reg_bits_max, reg_bits_min = position[1].split("-")
                value_bits_max, value_bits_min = position[2].split("-")
            else:
                reg_bits_max = position[1]
                reg_bits_min = position[1]
                value_bits_max = position[2]
                value_bits_min = position[2]

            reg_bits_min = int(reg_bits_min)
            reg_bits_max = int(reg_bits_max)
            value_bits_min = int(value_bits_min)
            value_bits_max = int(value_bits_max)

            register_value = self.__getitem__((address_space_name, block_name, register))
            register_mask = 0x0
            for i in range(reg_bits_max + 1):
                if i >= reg_bits_min and i <= reg_bits_max:
                    register_mask += 0x1 << i
            register_mask = ~register_mask
            register_value = register_value & register_mask  # Remove bits we are trying to set

            value_tmp = value >> value_bits_min
            value_mask = 0
            for i in range(value_bits_max - value_bits_min + 1):
                value_mask += 0x1 << i

            register_value += (value_tmp & value_mask) << reg_bits_min

            register_value = self.__setitem__((address_space_name, block_name, register), register_value)

    def save_pickle_file(self, config_file: str, object):
        save_object = {
            'object': object,
            'chip': self._chip_name,
            'version': self._software_version,
        }

        with open(config_file, 'wb') as f:
            pickle.dump(save_object, f)

    def load_pickle_file(self, config_file: str):
        loaded_obj = None
        with open(config_file, 'rb') as f:
            loaded_obj = pickle.load(f)

        if 'chip' not in loaded_obj:
            self._logger.error("The pickle file does not have the correct format")
            return None

        if loaded_obj['chip'] != self._chip_name:
            self._logger.error(
                "Wrong config file type. It was saved for the chip: {}; expected {}".format(loaded_obj['chip'], self._chip_name)
            )
            return None

        # TODO: for the version we should probably implement some sort of semantic versioning
        if loaded_obj['version'] != self._software_version:
            self._logger.error(
                "Wrong config file type. It was saved for a different version of this chip: {}; expected {}".format(
                    loaded_obj['version'], self._software_version
                )
            )
            return None

        return loaded_obj['object']

    def save_config(self, config_file: str):
        info = {}

        for address_space_name in self._address_space:
            address_space: Address_Space_Controller = self._address_space[address_space_name]
            size = address_space._address_space_size

            conf = [None for _ in range(size)]

            for idx in range(size):
                conf[idx] = address_space._memory[idx]

            info[address_space_name] = conf

        self.save_pickle_file(config_file, info)

    def load_config(self, config_file: str):
        info = self.load_pickle_file(config_file)

        for address_space_name in self._address_space:
            address_space: Address_Space_Controller = self._address_space[address_space_name]
            size = address_space._address_space_size

            for idx in range(size):
                address_space._memory[idx] = info[address_space_name][idx]

    def reset_config_to_default(self):
        for name in self._address_space:
            self._address_space[name].reset_to_defaults()
