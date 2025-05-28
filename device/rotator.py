# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# rotator.py - Endpoints for members of ASCOM Alpaca Rotator Device
#
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Implements: ASCOM IRotatorV4 interface
#             https://ascom-standards.org/newdocs/rotator.html#Rotator
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
# 18-Dec-2022   rbd 0.1 For upgraded exception classes
# 19-Dec-2022   rbd 0.1 Implement all IRotatorV3 endpoints
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Logging of endpoints
# 27-Dec-2022   rbd 0.1 Revamp logging so request precedes
#               response. Minimize imported stuff. MIT license
#               and module header.
# 30-Dec-2022   rbd 0.1 Revamp request pre-processing, logging, and
#               quality control. Device number from URI.
# 31-Dec-2022   rbd 0.1 Bad boolean values return 400 Bad Request
# 15-Jan-2023   rbd 0.1 Documentation. No logic changes.
# 20-Jan-2023   rbd 0.1 Refactor for clarity
# 23-May-2023   rbd 0.2 Refactoring for  multiple ASCOM device type support
#               GitHub issue #1
# 30-May-2023   rbd 0.2 Remove redundant logging from PUT responders
# 31-May-2023   rbd 0.3 responder class names lower cased to match URI
# 08-Nov-2023   rbd 0.4 Replace exotic 'dunder' construction of error
#               messages with actual text. Just a clarification. Remove
#               superfluous () on class declarations.
# 15-Feb-2024   rbd 0.6 Upgrade to Rotator V4 (Platform 7)
# 16-Feb-2024   rbd 0.6 Passes Validtion and Protocol ConformU 2.1.0
# 20-Feb-2024   rbd 0.7 Wow. Load device from Config (and toml) ha ha.
#               Add setting for sync/async Connected write.
# 16-Sep-2024   rbd 1.0 Add logic for proper InvalidValueException on
#               string to float conversions instead of just 400 errors.
#
import time
from adafruit_httpserver import Request, Response, Server, Route, GET, PUT, BAD_REQUEST_400, InvalidPathError
from adafruit_logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes
from rotatordevice import RotatorDevice

logger: Logger = None           # Really should use Pyton 3.10 or later
#logger = None                  # Safe on Python 3.7 but no intellisense in VSCode etc.

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance

# -------------------
# ROTATOR DEVICE INFO
# -------------------
# Static metadata not subject to configuration changes
class RotatorMetadata:
    """ Metadata describing the Rotator Device. Edit for your device"""
    Name = 'Sample Rotator'
    Version = '0.6'
    Description = 'Sample ASCOM Rotator'
    DeviceType = 'Rotator'
    DeviceID = '1892ED30-92F3-4236-843E-DA8EEEF2D1CC' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements IRotatorV4\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 4        # IRotatorV4 (Platform 7)

# --------------------
# SIMULATED ROTATOR ()
# --------------------
rot_dev = None
# At app init not import :-)
def start_rot_device(logger: Logger):
    logger = logger
    global rot_dev
    rot_dev = RotatorDevice(logger)
    rot_dev.can_reverse = Config.can_reverse
    rot_dev.step_size = Config.step_size
    rot_dev.steps_per_sec = Config.steps_per_sec
    rot_dev.sync_write_connected = Config.sync_write_connected

# --------------------
# RESOURCE CONTROLLERS
# --------------------

class action:
    """Invoke the specified device-specific custom action

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Action
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        name = get_request_field('ActionName', req)
        params = get_request_field('ActionParameters', req)
        # See SupportedActions
        if name.lower() ==  'myaction':
            logger.info('MyAction called')
            # Execute rot_dev.MyAction(params)
        elif name.lower() == 'youraction':
            logger.info('YourAction called')
            # Execute rot_dev.YourAction(params)
        else:
            return Response(req, MethodResponse(req, ActionNotImplementedException()).json)
        # If you don't want to implement this at all then
        # return Response(req, MethodResponse(req, NotImplementedException()).json)


class commandblind:
    # Do not use
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return Response(req, MethodResponse(req, NotImplementedException()).json)


class commandbool:
    # Do not use
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return Response(req, MethodResponse(req, NotImplementedException()).json)


class commandstring:
    # Do not use
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return Response(req, MethodResponse(req, NotImplementedException()).json)

# Connected, though common, is implemented in rotator.py

class description:
    """Description of the device such as manufacturer and model number.
        Any ASCII characters may be used.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Description
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(RotatorMetadata.Description, req).json)


class driverinfo:
    """Descriptive and version information about the ASCOM **driver**

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DriverInfo
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(RotatorMetadata.Info, req).json)


class interfaceversion:
    """ASCOM Device interface definition version that this device supports.
        Should return 4 for this interface version IRotatorV4.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.InterfaceVersion
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(RotatorMetadata.InterfaceVersion, req).json)


class driverversion:
    """String containing only the major and minor version of the **driver**.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DriverVersion
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(RotatorMetadata.Version, req).json)


class name:
    """The short name of the **driver**, for display purposes.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Name
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(RotatorMetadata.Name, req).json)


class supportedactions:
    """Returns the list of custom action names, to be used with ``Action()``,
        supported by this driver.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.SupportedActions
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        val = []
        val.append('MyAction')
        val.append('YourAction')
        return Response(req, PropertyResponse(val, req).json)  # Not PropertyNotImplemented


class canreverse:
    """True if the rotator supports the ``Reverse`` method

        Seehttps://ascom-standards.org/newdocs/rotator.html#Rotator.CanReverse

        Always True for IRotatorV3 (InterfaceVersion >= 3).
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(True, req).json)    # IRotatorV3, CanReverse must be True


class connect:
    """Connect to the device asynchronously

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connect
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        try:
            rot_dev.Connect()
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Connect failed', ex)).json)


class connected:
    """Retrieves or sets the connected state of the device

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connected

        Notes:
            There is a setting ``sync_write_connected`` in config.toml that
            determines whether connecting by writing ``Connected = True`` behaves
            synchronously or acts asynchronously. Conform requires this to be synchronous
            per IRotatorV3 (PLatform 6).
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return Response(req, PropertyResponse(rot_dev.connected, req).json)

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        conn_str = get_request_field('Connected', req)

        try:
            conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails
            # ----------------------
            rot_dev.connected = conn
            # ----------------------
            return Response(req, MethodResponse(req).json)
        except InvalidPathError as e:
            return Response(req, str(e), status=BAD_REQUEST_400)
        except Exception as ex:
            return Response(req, MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Connected failed', ex)).json)


class connecting:
    """True while the device is undertaking an asynchronous connect or disconnect operation.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connecting
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        try:
            val = rot_dev.connecting
            return Response(req, PropertyResponse(val, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Connecting failed', ex)).json)


class devicestate:
    """List of StateValue objects representing the operational properties of this device.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DeviceState
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            now = time.localtime()
            asctime = (f"{now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}")
            val = []
            val.append(StateValue('IsMoving', rot_dev.is_moving))
            val.append(StateValue('MechanicalPosition', rot_dev.mechanical_position))
            val.append(StateValue('Position', rot_dev.position))
            val.append(StateValue('TimeStamp', asctime))
            return Response(req, PropertyResponse(val, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Camera.Devicestate failed', ex)).json)


class disconnect:
    """Disconnect from the device asynchronously.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Disconnect

        NOTE: In this sample, Disconnect is instantaneous
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        try:
            rot_dev.Disconnect()
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Disconnect failed', ex)).json)


class ismoving:
    """True if the rotator is currently moving to a new angle

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.IsMoving
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # ---------------------
            moving = rot_dev.is_moving
            # ---------------------
            return Response(req, PropertyResponse(moving, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.IsMovingfailed', ex)).json)


class mechanicalposition:
    """The raw mechanical position of the rotator in degrees.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.MechanicalPosition
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # -------------------------------
            pos = rot_dev.mechanical_position
            # -------------------------------
            return Response(req, PropertyResponse(pos, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.MechanicalPosition failed', ex)).json)


class position:
    """Current instantaneous Rotator position, allowing for any sync offset, in degrees.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Position
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # -------------------------------
            pos = rot_dev.position
            # -------------------------------
            return Response(req, PropertyResponse(pos, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Position failed', ex)).json)


class reverse:
    """The direction of rotation CCW or CW

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Reverse
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # -------------------
            rev = rot_dev.reverse
            # -------------------
            return Response(req, PropertyResponse(rev, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).json)

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        revstr = get_request_field('Reverse', req)
        try:
            rev = to_bool(revstr)
        except InvalidPathError as e:
            return Response(req, str(e), status=BAD_REQUEST_400)
        except:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Reverse {revstr} not a valid boolean.')).json)
        try:
            # ----------------------
            rot_dev.reverse = rev
            # ----------------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).json)


class stepsize:
    """Minimum rotation step size (deg)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.StepSize
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # ---------------------
            steps = rot_dev.step_size
            # ---------------------
            return Response(req, PropertyResponse(steps, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.StepSize failed', ex)).json)


class targetposition:
    """The destination angle for ``Move()`` and ``MoveAbsolute()``

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.TargetPosition
    """
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, PropertyResponse(None, req,
                            NotConnectedException()).json)
        try:
            # ---------------------------
            pos = rot_dev.target_position
            # ---------------------------
            return Response(req, PropertyResponse(pos, req).json)
        except Exception as ex:
            return Response(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.TargetPosition failed', ex)).json)


class halt:
    """Immediately stop any rotator motion

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Halt
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        try:
            # ------------
            rot_dev.Halt()
            # ------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Halt failed', ex)).json)



class move:
    """Start rotation relative to the current position (degrees)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Move
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        newpos_str = get_request_field('Position', req)    # May raise 400 bad request
        try:
            newpos = origpos = float(newpos_str)
        except:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Position {newpos_str} not a valid float.')).json)
        # The spec calls for "anything goes" requires you to range the
        # final value modulo 360 degrees.
        if newpos >= 360.0:
            newpos -= 360.0
            logger.debug('Result would be >= 360, setting to {newpos}')
        if newpos < 0:
            newpos += 360
            logger.debug('Result would be < 0, setting to {newpos}')
        try:
            # ------------------
            rot_dev.Move(newpos)    # async
            # ------------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Move failed', ex)).json)


class moveabsolute:
    """Start rotation to the given ``Position`` (degrees)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.MoveAbsolute
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Position {pos_str} not a valid float.')).json)
        if newpos < 0.0 or newpos >= 360.0:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json)
        try:
            # --------------------------
            rot_dev.MoveAbsolute(newpos)    # async
            # --------------------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.MoveAbsolute failed', ex)).json)


class movemechanical:
    """Start rotation to the given new mechanical position (degrees)

    See https://ascom-standards.org/newdocs/rotator.html#Rotator.MoveMechanical
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        formdata = req.get_media()
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Position {pos_str} not a valid float.')).json)
        if newpos < 0.0 or newpos >= 360.0:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json)
        try:
            # ----------------------------
            rot_dev.MoveMechanical(newpos)    # async
            # ----------------------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.MoveMechanical failed', ex)).json)


class sync:
    """Syncs the rotator to the specified position angle (degrees) without moving it.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Sync
    """
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        formdata = req.get_media()
        if not rot_dev.connected:
            return Response(req, MethodResponse(req,
                            NotConnectedException()).json)
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Position {pos_str} not a valid float.')).json)
        if newpos < 0.0 or newpos >= 360.0:
            return Response(req, MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json)
        try:
            # ------------------
            rot_dev.Sync(newpos)
            # ------------------
            return Response(req, MethodResponse(req).json)
        except Exception as ex:
            return Response(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Sync failed', ex)).json)

def init_routes(server: Server, api_version):
    server.add_routes([
        Route(f'/api/v{api_version}/rotator/<devnum>/action', PUT, action.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/commandblind', PUT, commandblind.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/commandbool', PUT, commandbool.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/commandstring', PUT, commandstring.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/description', GET, description.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/driverinfo', GET, driverinfo.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/interfaceversion', GET, interfaceversion.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/driverversion', GET, driverversion.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/name', GET, name.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/supportedactions', GET, supportedactions.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/canreverse', GET, canreverse.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/connect', PUT, connect.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/connected', GET, connected.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/connected', PUT, connected.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/connecting', GET, connecting.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/devicestate', GET, devicestate.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/disconnect', PUT, disconnect.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/ismoving', GET, ismoving.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/mechanicalposition', GET, mechanicalposition.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/position', GET, position.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/reverse', GET, reverse.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/reverse', PUT, reverse.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/stepsize', GET, stepsize.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/targetposition', GET, targetposition.on_get),
        Route(f'/api/v{api_version}/rotator/<devnum>/halt', PUT, halt.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/move', PUT, move.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/moveabsolute', PUT, moveabsolute.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/movemechanical', PUT, movemechanical.on_put),
        Route(f'/api/v{api_version}/rotator/<devnum>/sync', PUT, sync.on_put),
    ])
