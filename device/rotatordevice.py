# =================================================================
# ROTATORDEVICE.PY - Poor-man's simulaton of a Rotator
# =================================================================
#
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# rotatordevice.py - Poor-man's simulation of a rotator
#
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# This is only for demo purposes. It's extremely fragile, and should
# not be used as an example of a real device. Settings not remembered.
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
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Type hints
# 19-Dec-2022   rbd 0.1 Add logic for IRotatorV3 offsets
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Do not log within lock()ed sections
# 27-Dec-2022   rbd 0.1 MIT license and module header
# 15-Jan-2023   rbd 0.1 Documentation. No logic changes.
# 15-Feb-2024   rbd 0.6 Upgrade to Rotator V4 (Platform 7)
# 20-Feb-2024   rbd 0.7 Setting for Connected-Write to be sync or async
#
from adafruit_logging import Logger

class RotatorDevice:
    """Simulated rotator device that does moves in separate Timer threads.

    Properties and  methods generally follow the Alpaca interface.
    Debug tracing here via (commented out) print() to avoid locking issues.
    Hopefully you are familiar with Python threading and the need to lock
    shared data items.

    **Mechanical vs Virtual Position**

    In this code 'mech' refers to the raw mechanical position. Note the
    conversions ``_pos_to_mech()`` and ``_mech_to_pos()``. This is where
    the ``Sync()`` offset is applied.

    """
    #
    # Only override __init_()  and run() (pydoc 17.1.2)
    #
    def __init__(self, logger: Logger):
        self.name: str = 'device'
        self.logger = logger
        #
        # Rotator device constants
        #
        self._can_reverse: bool = True
        self._step_size: float = 1.0
        self._steps_per_sec: int = 6
        self._conn_time_sec: float = 5.0    # Async connect delay
        self._sync_write_connected = True;
        #
        # Rotator device state variables
        #
        self._reverse = False
        self._mech_pos = 0.0
        self._tgt_mech_pos = 0.0
        self._pos_offset = 0.0      # TODO In real life this must be persisted
        self._is_moving = False
        self._connecting = False
        self._connected = False
        #
        # Rotator engine
        #
        self._interval: float = 1.0 / self._steps_per_sec
        self._stopped: bool = True
        #
        # Connect delay
        #

    def _pos_to_mech(self, pos: float) -> float:
        mech = pos - self._pos_offset
        if mech >= 360.0:
            mech -= 360.0
        if mech < 0.0:
            mech += 360.0
        return mech

    def _mech_to_pos(self, mech: float) -> float:
        pos = mech + self._pos_offset
        if pos >= 360.0:
            pos -= 360.0
        if pos < 0.0:
            pos += 360.0
        return pos

    def _conn_complete(self):
        self._connlock.acquire()
        self.logger.info('[connected]')
        self._connecting = False
        self._connected = True
        self._connlock.release()

    def start(self, from_run: bool = False) -> None:
        #print('[start]')
        #print('[start] got lock')
        if from_run or self._stopped:
            self._stopped = False


    def _run(self) -> None:
        delta = self._tgt_mech_pos - self._mech_pos
        if delta < -180.0:
           delta += 360.0
        if delta >= 180.0:
           delta -= 360.0
        #print(f'[_run] final delta={str(delta)}')
        if abs(delta) > (self._step_size / 2.0):
            self._is_moving = True
            if delta > 0:
                #print('[_run] delta > 0 go positive')
                self._mech_pos += self._step_size
                if self._mech_pos >= 360.0:
                    self._mech_pos -= 360.0
            else:
                #print('[_run] delta < 0 go negative')
                self._mech_pos -= self._step_size
                if self._mech_pos < 0.0:
                    self._mech_pos += 360.0
            #print(f'[_run] new pos = {str(self._mech_to_pos(self._mech_pos))}')
        else:
            self._is_moving = False
            self._stopped = True
        #print('[_run] lock released')
        if self._is_moving:
            #print('[_run] more motion needed, start another timer interval')
            self.start(from_run = True)

    def stop(self) -> None:
        #print('[stop] Stopping...')
        self._stopped = True
        self._is_moving = False

    #
    # Guarded properties
    #
    @property
    def can_reverse(self) -> bool:
        res =  self._can_reverse
        return res
    
    @can_reverse.setter
    def can_reverse (self, reverse: bool):
        self._can_reverse = reverse

    @property
    def reverse(self) -> bool:
        res =  self._reverse
        return res
    @reverse.setter
    def reverse (self, reverse: bool):
        self._reverse = reverse

    @property
    def step_size(self) -> float:
        res =  self._step_size
        return res
    @step_size.setter
    def step_size (self, step_size: float):
        self._step_size = step_size

    @property
    def steps_per_sec(self) -> int:
        res =  self._steps_per_sec
        return res
    @steps_per_sec.setter
    def steps_per_sec (self, steps_per_sec: int):
        self._steps_per_sec = steps_per_sec

    @property
    def sync_write_connected(self) -> float:
        res =  self._sync_write_connected
        return res
    @sync_write_connected.setter
    def sync_write_connected (self, sync: float):
        self._sync_write_connected = sync

    @property
    def position(self) -> float:
        res = self._mech_to_pos(self._mech_pos)
        self.logger.debug(f'[position] {str(res)}')
        return res

    @property
    def mechanical_position(self) -> float:
        res = self._mech_pos
        self.logger.debug(f'[mech position] {str(res)}')
        return res

    @property
    def target_position(self) -> float:
        res =  self._mech_to_pos(self._tgt_mech_pos)
        self.logger.debug(f'[target_position] {str(res)}')
        return res

    @property
    def is_moving(self) -> bool:
        res =  self._is_moving
        self.logger.debug(f'[is_moving] {str(res)}')
        self.logger.debug(f'[is_moving] {str(res)}')
        return res

    @property
    def connected(self) -> bool:
        res = self._connected
        return res
    @connected.setter
    def connected (self, toconnect: bool):
        if (not toconnect) and self._connected and self._is_moving:
            # Yes you could call Halt() but this is for illustration
            raise RuntimeError('Cannot disconnect while rotator is moving')
        if toconnect:
            if (self.sync_write_connected):
                self._connected = True
                self.logger.info('[instant connected]')
            else:
                self.logger.info('[delayed connecting]')
        else:
            self._connected = False
            self.logger.info('[instant disconnected]')

    @property
    def connecting(self) -> bool:
        res = self._connecting
        return res

    # =======
    # Methods
    # =======

    def Connect(self) -> None:
        self.logger.debug(f'[Connect]')
        if self._connected:
            self._connecting = False
            self.logger.debug(f'[Already connected]')
            return
        self._connecting = True
        self._connected = False

    def Disconnect(self) -> None:
        self.logger.debug(f'[Disconnect]')
        if not self._connected:
            self._connecting = False
            self.logger.debug(f'[Already disconnected]')
            return
        if self._is_moving:
            # Yes you could call Halt() but this is for illustration
            raise RuntimeError('Cannot disconnect while rotator is moving')
        self._connected = False

    # TODO - This is supposed to throw if the final position is outside 0-360, but WHICH position? Mech or user????
    #
    def Move(self, delta_pos: float) -> None:
        self.logger.debug(f'[Move] pos={str(delta_pos)}')
        if self._is_moving:
            raise RuntimeError('Cannot start a move while the rotator is moving')
        self._is_moving = True
        self._tgt_mech_pos = self._mech_pos + delta_pos - self._pos_offset
        if self._tgt_mech_pos >= 360.0:
            self._tgt_mech_pos -= 360.0
        if self._tgt_mech_pos < 0.0:
            self._tgt_mech_pos += 360.0
        self.logger.debug(f'       targetpos={self._mech_to_pos(self._tgt_mech_pos)}')
        self.start()

    def MoveAbsolute(self, pos: float) -> None:
        self.logger.debug(f'[MoveAbs] pos={str(pos)}')
        if self._is_moving:
            raise RuntimeError('Cannot start a move while the rotator is moving')
        self._is_moving = True
        self._tgt_mech_pos = self._pos_to_mech(pos)
        self.start()

    def MoveMechanical(self, pos: float) -> None:
        if self._is_moving:
            raise RuntimeError('Cannot start a move while the rotator is moving')
        self.logger.debug(f'[MoveMech] pos={str(pos)}')
        self._is_moving = True
        self._tgt_mech_pos = pos
        self.start()

    def Sync(self, pos: float) -> None:
        self.logger.debug(f'[Sync] newpos={str(pos)}')
        if self._is_moving:
            raise RuntimeError('Cannot sync while rotator is moving')
        self._pos_offset = pos - self._mech_pos
        if self._pos_offset < -180.0:
           self._pos_offset += 360.0
        if self._pos_offset >= 180.0:
           self._pos_offset -= 360.0

    def Halt(self) -> None:
        self.logger.debug('[Halt]')
        self.stop()
