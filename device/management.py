# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# management.py - Management API for  ALpaca device
#
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

from adafruit_httpserver import Request, JSONResponse
from shr import PropertyResponse, DeviceMetadata
from config import Config
# For each *type* of device served
from rotator import RotatorMetadata

global logger
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

# -----------
# APIVersions
# -----------
class apiversions:
    def on_get(req: Request):
        apis = [ 1 ]                            # TODO MAKE CONFIG OR GLOBAL
        return JSONResponse(req, PropertyResponse(apis, req).dict)

# -------------------------
# Alpaca Server Description
# -------------------------
class description:
    def on_get(req: Request):
        desc = {
            'ServerName'   : DeviceMetadata.Description,
            'Manufacturer' : DeviceMetadata.Manufacturer,
            'Version'      : DeviceMetadata.Version,
            'Location'     : Config.location
            }
        return JSONResponse(req, PropertyResponse(desc, req).dict)

# -----------------
# ConfiguredDevices
# -----------------
class configureddevices():
    def on_get(req: Request):
        confarray = [    # TODO ADD ONE FOR EACH DEVICE TYPE AND INSTANCE SERVED
            {
            'DeviceName'    : RotatorMetadata.Name,
            'DeviceType'    : RotatorMetadata.DeviceType,
            'DeviceNumber'  : 0,
            'UniqueID'      : RotatorMetadata.DeviceID
            }
        ]
        return JSONResponse(req, PropertyResponse(confarray, req).dict)