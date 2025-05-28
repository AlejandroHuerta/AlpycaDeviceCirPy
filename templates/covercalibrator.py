
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# covercalibrator.py - Alpaca API responders for Covercalibrator
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------

from adafruit_httpserver import Request, JSONResponse, Server, Route, GET, PUT
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
class CovercalibratorMetadata:
    """ Metadata describing the Covercalibrator Device. Edit for your device"""
    Name = 'Sample Covercalibrator'
    Version = '##DRIVER VERSION AS STRING##'
    Description = 'My ASCOM Covercalibrator'
    DeviceType = 'Covercalibrator'
    DeviceID = '##GENERATE A NEW GUID AND PASTE HERE##' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements ICovercalibrator\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = ##YOUR DEVICE INTERFACE VERSION##        # ICovercalibratorVxxx

# --------------
# SYMBOLIC ENUMS
# --------------
#

class CalibratorStatus():
    NotPresent = 0,
    Off = 1,
    NotReady = 2,
    Ready = 3,
    Unknown = 4,
    Error = 5

class CoverStatus():
    NotPresent = 0,
    Closed = 1,
    Moving = 2,
    Open = 3,
    Unknown = 4,
    Error = 5

# --------------------
# RESOURCE CONTROLLERS
# --------------------

class action:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandblind:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandbool:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class commandstring:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        return JSONResponse(req, MethodResponse(req, NotImplementedException()).dict)

class connect:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        try:
            # ------------------------
            ### CONNECT THE DEVICE ###
            # ------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Connect failed', ex)).dict)

class connected:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        try:
            # -------------------------------------
            is_conn = ### READ CONN STATE ###
            # -------------------------------------
            return JSONResponse(req, PropertyResponse(is_conn, req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req, DriverException(0x500, 'Covercalibrator.Connected failed', ex)).dict)

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails

        try:
            # --------------------------------------
            ### CONNECT OR DISCONNECT THE DEVICE ###
            # --------------------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Connected failed', ex)).dict)

class connecting:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        try:
            # ------------------------------
            val = ## GET CONNECTING STATE ##
            # ------------------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Covercalibrator.Connecting failed', ex)).dict)

class description:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse(CovercalibratorMetadata.Description, req).dict)

class devicestate:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
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
                            DriverException(0x500, 'covercalibrator.Devicestate failed', ex)).dict)


class disconnect:
    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        try:
            # ---------------------------
            ### DISCONNECT THE DEVICE ###
            # ---------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Disconnect failed', ex)).dict)

class driverinfo:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse(CovercalibratorMetadata.Info, req).dict)

class interfaceversion:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse(CovercalibratorMetadata.InterfaceVersion, req).dict)

class driverversion():
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse(CovercalibratorMetadata.Version, req).dict)

class name():
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse(CovercalibratorMetadata.Name, req).dict)

class supportedactions:
    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        return JSONResponse(req, PropertyResponse([], req).dict)  # Not PropertyNotImplemented

class brightness:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
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
                            DriverException(0x500, 'Covercalibrator.Brightness failed', ex)).dict)

class calibratorchanging:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
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
                            DriverException(0x500, 'Covercalibrator.Calibratorchanging failed', ex)).dict)

class calibratorstate:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
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
                            DriverException(0x500, 'Covercalibrator.Calibratorstate failed', ex)).dict)

class covermoving:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
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
                            DriverException(0x500, 'Covercalibrator.Covermoving failed', ex)).dict)

class coverstate:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req, NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Covercalibrator.Coverstate failed', ex)).dict)

class maxbrightness:

    @PreProcessRequest(maxdev)
    def on_get(req: Request, devnum: int):
        if not ##IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req, NotConnectedException()).dict)
        
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            return JSONResponse(req, PropertyResponse(val, req).dict)
        except Exception as ex:
            return JSONResponse(req, PropertyResponse(None, req,
                            DriverException(0x500, 'Covercalibrator.Maxbrightness failed', ex)).dict)

class calibratoroff:

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not ## IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Calibratoroff failed', ex)).dict)

class calibratoron:

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not ## IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req, NotConnectedException()).dict)
        
        brightnessstr = get_request_field('Brightness', req)      # Raises 400 bad request if missing
        try:
            brightness = int(brightnessstr)
        except:
            return JSONResponse(req, MethodResponse(req,
                            InvalidValueException(f'Brightness {brightnessstr} not a valid integer.')).dict)
        ### RANGE CHECK AS NEEDED ###  # Raise Alpaca InvalidValueException with details!
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Calibratoron failed', ex)).dict)

class closecover:

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not ## IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Closecover failed', ex)).dict)

class haltcover:

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not ## IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req,
                            DriverException(0x500, 'Covercalibrator.Haltcover failed', ex)).dict)

class opencover:

    @PreProcessRequest(maxdev)
    def on_put(req: Request, devnum: int):
        if not ## IS DEV CONNECTED##:
            return JSONResponse(req, PropertyResponse(None, req,
                            NotConnectedException()).dict)
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            return JSONResponse(req, MethodResponse(req).dict)
        except Exception as ex:
            return JSONResponse(req, MethodResponse(req, DriverException(0x500, 'Covercalibrator.Opencover failed', ex)).dict)
            
def init_routes(server: Server, api_version):
    server.add_routes([
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/action', PUT, action.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/commandblind', PUT, commandblind.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/commandbool', PUT, commandbool.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/commandstring', PUT, commandstring.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/connect', PUT, connect.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/connected', GET, connected.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/connected', PUT, connected.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/connecting', GET, connecting.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/description', GET, description.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/devicestate', GET, devicestate.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/disconnect', PUT, disconnect.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/driverinfo', GET, driverinfo.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/interfaceversion', GET, interfaceversion.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/driverversion', GET, driverversion.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/name', GET, name.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/supportedactions', GET, supportedactions.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/brightness', GET, brightness.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/calibratorchanging', GET, calibratorchanging.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/calibratorstate', GET, calibratorstate.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/covermoving', GET, covermoving.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/coverstate', GET, coverstate.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/maxbrightness', GET, maxbrightness.on_get),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/calibratoroff', PUT, calibratoroff.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/calibratoron', PUT, calibratoron.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/closecover', PUT, closecover.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/haltcover', PUT, haltcover.on_put),
        Route(f'/api/v{api_version}/covercalibrator/<devnum>/opencover', PUT, calibratoron.on_put),
    ])
