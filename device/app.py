# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# app.py - Application module
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
# Edit History:
import wifi
from adafruit_connection_manager import get_radio_socketpool
import asyncio

import discovery
import exceptions
from adafruit_httpserver import Server, Route, GET
import management
import setup
import log
from config import Config
import shr

##############################
# FOR EACH ASCOM DEVICE TYPE #
##############################
import rotator

#--------------
API_VERSION = 1
#--------------

def init_routes(server: Server):
    #########################
    # FOR EACH ASCOM DEVICE #
    #########################
    rotator.init_routes(server, API_VERSION)

async def main():
    """ Application startup"""

    logger = log.init_logging()
    # Share this logger throughout
    log.logger = logger
    exceptions.logger = logger
    rotator.start_rot_device(logger)
    discovery.logger = logger
    shr.logger = logger
    management.logger = logger

    #########################
    # FOR EACH ASCOM DEVICE #
    #########################
    rotator.logger = logger

    wifi.radio.connect(ssid=Config.wifi_ssid, password=Config.wifi_password)
    logger.info('Connected to wifi at: %s', str(wifi.radio.ipv4_address))
    
    pool = get_radio_socketpool(wifi.radio)
    server = Server(pool, "/", debug=True)
    
    server.add_routes([
        Route('/management/apiversions', GET, management.apiversions.on_get),
        Route(f'/management/v{API_VERSION}/description', GET, management.description.on_get),
        Route(f'/management/v{API_VERSION}/configureddevices', GET, management.configureddevices.on_get),
        Route('/setup', GET, setup.srvsetup.on_get),
        Route(f'/setup/v{API_VERSION}/rotator/<devnum>/setup', GET, setup.devsetup.on_get),
    ])
    
    init_routes(server)
    
    dsc = discovery.DiscoveryResponder(Config.ip_address, Config.port)
    dsc_task = asyncio.create_task(dsc.run(pool))
    
    poll_task = asyncio.create_task(poll(server))

    await asyncio.gather(poll_task, dsc_task)
    
async def poll(server: Server):
    server.start(str(wifi.radio.ipv4_address), Config.port)
    while True:
        server.poll()
        await asyncio.sleep(.01)
