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

import io
import logging
import tkinter as tk
import tkinter.ttk as ttk  # For themed widgets (gives a more native visual to the elements)

from .base_gui import Base_GUI


class Logging_Helper:
    _parent: Base_GUI
    _log_levels = {
        "Detailed Trace": logging.DETAILED_TRACE,  # (Custom)
        "Trace": logging.TRACE,  # (Custom)
        "Debug": logging.DEBUG,
        "Info": logging.INFO,
        "Warning": logging.WARNING,
        "Error": logging.ERROR,
        "Critical": logging.CRITICAL,
    }
    _default_log_level = "Info"

    def __init__(
        self,
        parent: Base_GUI,
        logger: logging.Logger,
    ):
        self._parent = parent
        self._logger = logger

        self._do_logging = False
        self._logger.disabled = True

        self._stream = io.StringIO()
        self._stream_handler = logging.StreamHandler(self._stream)
        self._stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s:%(name)s:%(message)s'))
        self._logger.handlers.clear()

        self._logging_window_status_var = tk.StringVar()
        self._logging_window_status_var.set("Logging Disabled")

        self._autorefresh_var = tk.BooleanVar(value=False)
        self._log_to_terminal_var = tk.BooleanVar(value=self._logger.propagate)
        self._log_level_var = tk.StringVar()
        self._log_level_var.trace_add('write', self._update_log_level)
        self._log_level_var.set(self._default_log_level)

    def _update_log_level(self, var=None, index=None, mode=None):
        self._logger.detailed_trace("Logging_Helper._update_log_level: Entered")

        new_level = self._log_level_var.get()
        if new_level not in self._log_levels:
            self._log_level_var.set(self._default_log_level)
            new_level = self._default_log_level

        numeric_level = self._log_levels[new_level]

        self._logger.setLevel(numeric_level)

    @property
    def is_logging(self):
        return self._do_logging

    @is_logging.setter
    def is_logging(self, value):
        self._logger.detailed_trace(f"Logging_Helper.is_logging setter: Entered with value {value}")

        if value not in [True, False]:
            raise TypeError("Logging can only be true or false")

        self._do_logging = value

        if self._do_logging:
            if self._stream_handler not in self._logger.handlers:
                self._logger.addHandler(self._stream_handler)
            # self._log_level_option.config(state = 'disabled')
            self._logger.disabled = False
            self._logging_window_status_var.set("Logging Enabled")
        else:
            if self._stream_handler in self._logger.handlers:
                self._logger.removeHandler(self._stream_handler)
            # self._log_level_option.config(state = 'normal')
            self._logger.disabled = True
            self._logging_window_status_var.set("Logging Disabled")

    def get_log(self):
        return self._stream.getvalue()

    def display_logging(self):
        if hasattr(self, "_logging_window"):
            self._logger.info("Logging window already open")
            self._logging_window.focus()
            return

        self._logging_window = tk.Toplevel(self._parent._root)
        self._logging_window.title(self._parent._title + " - Event Log")
        self._logging_window.protocol('WM_DELETE_WINDOW', self.close_logging_window)
        self._logging_window.columnconfigure(100, weight=1)
        self._logging_window.rowconfigure(100, weight=1)

        self._frame = ttk.Frame(self._logging_window, padding="5 5 5 5")
        self._frame.grid(column=100, row=100, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._frame.columnconfigure(100, weight=1)
        self._frame.rowconfigure(100, weight=1)

        self._text_frame = ttk.Frame(self._frame)
        self._text_frame.grid(column=100, row=100, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._text_frame.columnconfigure(100, weight=1)
        self._text_frame.rowconfigure(100, weight=1)

        self._text_display = tk.Text(self._text_frame, state='disabled', width=150, wrap='none')
        self._text_display.grid(column=100, row=100, sticky=(tk.N, tk.W, tk.E, tk.S))

        self._scrollbar = ttk.Scrollbar(self._text_frame, command=self._text_display.yview)
        self._scrollbar.grid(row=100, column=101, sticky='nsew')
        self._text_display.config(yscrollcommand=self._scrollbar.set)

        self._control_frame = ttk.Frame(self._frame)
        self._control_frame.grid(column=100, row=200, sticky=(tk.N, tk.W, tk.E, tk.S))

        self._toggle_logging_button = ttk.Button(self._control_frame, text="Enable Logging", command=self.toggle_logging)
        self._toggle_logging_button.grid(column=100, row=100, sticky=(tk.W, tk.E), padx=(0, 5))

        self._clear_logging_button = ttk.Button(self._control_frame, text="Clear Log", command=self.clear_log)
        self._clear_logging_button.grid(column=110, row=100, sticky=(tk.W, tk.E), padx=(0, 5))

        self._log_level_option = ttk.OptionMenu(
            self._control_frame, self._log_level_var, self._log_level_var.get(), *self._log_levels.keys()
        )
        self._log_level_option.grid(column=120, row=100, sticky=(tk.W, tk.E), padx=(0, 5))

        self._logging_status_label = ttk.Label(self._control_frame, textvariable=self._logging_window_status_var)
        self._logging_status_label.grid(column=200, row=100, sticky=(tk.W, tk.E), padx=(0, 30))
        self._control_frame.columnconfigure(200, weight=1)

        self._log_to_terminal_check = ttk.Checkbutton(
            self._control_frame, text="Log to Terminal", variable=self._log_to_terminal_var, command=self.toggle_log_to_terminal
        )
        self._log_to_terminal_check.grid(column=300, row=100, sticky=(tk.W, tk.E), padx=(0, 10))

        self._autorefresh_check = ttk.Checkbutton(
            self._control_frame, text="Auto-refresh", variable=self._autorefresh_var, command=self.toggle_autorefresh
        )
        self._autorefresh_check.grid(column=400, row=100, sticky=(tk.W, tk.E), padx=(0, 10))

        self._refresh_button = ttk.Button(self._control_frame, text="Refresh", command=self.refresh_logging)
        self._refresh_button.grid(column=500, row=100, sticky=(tk.W, tk.E))

        self._logging_window.update()
        self._logging_window.minsize(self._logging_window.winfo_width(), self._logging_window.winfo_height())

    def close_logging_window(self):
        if not hasattr(self, "_logging_window"):
            self._logger.info("Logging window does not exist")
            return

        self.is_logging = False

        self._logging_window.destroy()
        del self._logging_window

    def clear_log(self):
        self._stream.truncate(0)
        self._stream.seek(0)
        self.refresh_logging()

    def toggle_logging(self):
        self.is_logging = not self.is_logging

        button_text = "Enable Logging"
        if self.is_logging:
            button_text = "Disable Logging"

        self._toggle_logging_button.config(text=button_text)

    def toggle_autorefresh(self):
        autorefresh = self._autorefresh_var.get()
        if autorefresh:
            # self.send_message("Turn on logging auto-refresh")
            self.autorefresh_logging()
            self._refresh_button.configure(state='disabled', text="Disabled")
        else:
            # self.send_message("Turn off logging auto-refresh")
            self._refresh_button.configure(state='normal', text="Refresh")

    def toggle_log_to_terminal(self):
        log_to_terminal = self._log_to_terminal_var.get()
        if log_to_terminal:  # The order here is important so that the turn-on/off is always logged to the terminal
            self._logger.propagate = log_to_terminal
            # self.send_message("Turn on logging to terminal")
        else:
            # self.send_message("Turn off logging to terminal")
            self._logger.propagate = log_to_terminal

    def autorefresh_logging(self):
        self.refresh_logging()

        autorefresh = self._autorefresh_var.get()
        if autorefresh:
            self._text_display.after(500, self.autorefresh_logging)

    def refresh_logging(self):
        # pos = self._scrollbar.get()
        vw = self._text_display.yview()

        # print(pos)
        # print(vw)
        # TODO: Scrollbar is still jumping around when updating. It is related to when the lines of text wrap to the next line
        # Disabling line wrapping seems to have "fixed" (hidden) the issue

        self._text_display.configure(state='normal')
        self._text_display.delete("1.0", tk.END)
        self._text_display.insert('end', self.get_log())
        self._text_display.configure(state='disabled')
        # self._text_display.yview_moveto(pos[0])
        self._text_display.yview_moveto(vw[0])
