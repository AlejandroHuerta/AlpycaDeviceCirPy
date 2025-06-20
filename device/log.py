# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# logging.py - Shared global logging object
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/AlpycaDevice
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2024 Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import adafruit_logging as logging
import storage
from config import Config

global logger
#logger: logging.Logger = None  # Master copy (root) of the logger
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

def init_logging():
    """ Create the logger - called at app startup

        **MASTER LOGGER**

        This single logger is used throughout. The module name (the param for
        get_logger()) isn't needed and would be 'root' anyway, sort of useless.
        Logs time stamps in UTC/ISO format, and with fractional seconds. Since
        our config options allow for suppression of logging to stdout, we remove
        the default stdout handler. Thank heaven that Python logging is
        thread-safe!

        This logger is passed around throughout the app and may be used
        throughout, even the device control. The :py:class:`config.Config` class
        has options to control the number of back generations of logs to keep,
        as well as the max size (at which point the log will be rotated). Also
        there is an option to cause logged messages to go to the console for
        debugging purposes. A new log is started each time the app is started.

    Returns:
        Customized Python logger.

    """

    logger = logging.getLogger()                # Root logger, see above
    logger.setLevel(Config.log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%dT%H:%M:%S')
    logging._default_handler.setFormatter(formatter)  # This is the stdout handler, level set above
    
    fat = storage.getmount("/")
    if not fat.readonly:
        # Add a logfile handler, same formatter and level
        handler = logging.RotatingFileHandler('alpyca.log',
                                                        mode='w',
                                                        maxBytes=Config.max_size_mb * 1000000,
                                                        backupCount=Config.num_keep_logs)
        handler.setLevel(Config.log_level)
        handler.setFormatter(formatter)
        handler.doRollover()                                            # Always start with fresh log
        logger.addHandler(handler)

    if not Config.log_to_stdout:
        """
            This allows control of logging to stdout by simply
            removing the stdout handler from the logger's
            handler list. It's always handler[0] as created
            by logging.basicConfig()
        """
        logger.debug('Logging to stdout disabled in settings')
        logger._default_handler = logging.NullHandler()    # This is the stdout handler
    return logger