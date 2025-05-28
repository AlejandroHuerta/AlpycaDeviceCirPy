
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# rotator.py - Alpaca API responders for Rotator
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------

from adafruit_httpserver import Request, Response, JSONResponse, Server, Route, GET, PUT, BAD_REQUEST_400, InvalidPathError
from adafruit_logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
## EDIT FOR YOUR DEVICE ##
class RotatorMetadata:
    """ Metadata describing the Rotator Device. Edit for your device"""
    Name = 'Sample Rotator'
    Version = '##DRIVER VERSION AS STRING##'
    Description = 'My ASCOM Rotator'
    DeviceType = 'Rotator'
    DeviceID = '##GENERATE A NEW GUID AND PASTE HERE##' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements IRotator\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = ##YOUR DEVICE INTERFACE VERSION##        # IRotatorVxxx


# --------------------
# RESOURCE CONTROLLERS
# --------------------

class action:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandblind:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandbool:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandstring:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class connect:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------
            ### CONNECT THE DEVICE ###
            # ------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Connect failed', ex)).dict)

class connected:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # -------------------------------------
            is_conn = ### READ CONN STATE ###
            # -------------------------------------
            return JSONResponse(req, PropertyResponse(is_conn, req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req, DriverException(0x500, 'Rotator.Connected failed', ex)).dict)

    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails

        try:
            # --------------------------------------
            ### CONNECT OR DISCONNECT THE DEVICE ###
            # --------------------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Connected failed', ex)).dict)

class connecting:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------------
            val = ## GET CONNECTING STATE ##
            # ------------------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Connecting failed', ex)).dict)

class description:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse(RotatorMetadata.Description, req).dict)

class devicestate:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        try:
            # ----------------------
            val = []
            # val.append(StateValue('## NAME ##', ## GET VAL ##))
            # Repeat for each of the operational states per the device spec
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'rotator.Devicestate failed', ex)).dict)


class disconnect:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ---------------------------
            ### DISCONNECT THE DEVICE ###
            # ---------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Disconnect failed', ex)).dict)

class driverinfo:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse(RotatorMetadata.Info, req).dict)

class interfaceversion:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse(RotatorMetadata.InterfaceVersion, req).dict)

class driverversion():
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse(RotatorMetadata.Version, req).dict)

class name():
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse(RotatorMetadata.Name, req).dict)

class supportedactions:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        return JSONResponse(req, PropertyResponse([], req).dict)  # Not PropertyNotImplemented

class canreverse:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Canreverse failed', ex)).dict)

class ismoving:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Ismoving failed', ex)).dict)

class mechanicalposition:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Mechanicalposition failed', ex)).dict)

class position:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Position failed', ex)).dict)

class reverse:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).dict)

    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        reversestr = get_request_field('Reverse', req)      # Raises 400 bad request if missing
        try:
            reverse = to_bool(reversestr)
        except:
             return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Reverse {reversestr} not a valid boolean.')).dict)

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).dict)

class stepsize:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Stepsize failed', ex)).dict)

class targetposition:
    @PreProcessRequest(maxdev)
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Targetposition failed', ex)).dict)

class halt:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Halt failed', ex)).dict)

class move:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        positionstr = get_request_field('Position', req)      # Raises 400 bad request if missing
        try:
            position = float(positionstr)
        except:
             return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Position {positionstr} not a valid number.')).dict)
        ### RANGE CHECK AS NEEDED ###  # Raise Alpaca InvalidValueException with details!
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Move failed', ex)).dict)

class moveabsolute:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        positionstr = get_request_field('Position', req)      # Raises 400 bad request if missing
        try:
            position = float(positionstr)
        except:
             return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Position {positionstr} not a valid number.')).dict)
        ### RANGE CHECK AS NEEDED ###  # Raise Alpaca InvalidValueException with details!
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Moveabsolute failed', ex)).dict)

class movemechanical:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        positionstr = get_request_field('Position', req)      # Raises 400 bad request if missing
        try:
            position = float(positionstr)
        except:
             return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Position {positionstr} not a valid number.')).dict)
        ### RANGE CHECK AS NEEDED ###  # Raise Alpaca InvalidValueException with details!
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Movemechanical failed', ex)).dict)

class sync:
    @PreProcessRequest(maxdev)
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        positionstr = get_request_field('Position', req)      # Raises 400 bad request if missing
        try:
            position = float(positionstr)
        except:
             return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Position {positionstr} not a valid number.')).dict)
        ### RANGE CHECK AS NEEDED ###  # Raise Alpaca InvalidValueException with details!
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
             return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Rotator.Sync failed', ex)).dict)

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
