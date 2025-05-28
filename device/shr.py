# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# shr.py - Device characteristics and support classes/functions/data
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

from exceptions import Success
import json
from adafruit_httpserver import Request, Response, InvalidPathError, BAD_REQUEST_400, FormData

global logger
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

_bad_title = 'Bad Alpaca Request'


# --------------------------
# Alpaca Device/Server Info
# --------------------------
# Static metadata not subject to configuration changes
class DeviceMetadata:
    """ Metadata describing the Alpaca Device/Server """
    Version = '0.1'
    Description = 'Alpyca32'
    Manufacturer = 'ASCOM Initiative'

# --------------------------------
# NAME/VALUE PAIRS FOR DEVICESTATE
# --------------------------------
class StateValue:
    def __init__(self, name, value):
        self.Name = name
        self.Value = value

# ---------------
# Data Validation
# ---------------
_bools = ['true', 'false']                               # Only valid JSON bools allowed
def to_bool(str: str) -> bool:
    val = str.lower()
    if val not in _bools:
        raise InvalidPathError(_bad_title, f'Bad boolean value "{val}"')
    return val == _bools[0]

# ---------------------------------------------------------
# Get parameter/field from query string or body "form" data
# If default is missing then the field is required. Maybe the
# field name is smisspelled, or mis-cased (for PUT), or
# missing. In any case, raise a 400 BAD REQUEST. Optional
# caseless (mostly for the ClientID and ClientTransactionID)
# ---------------------------------------------------------
def get_request_field(name: str, req: Request, caseless: bool = False, default: str = None) -> str:
    bad_desc = f'Missing, empty, or misspelled parameter "{name}"'
    lcName = name.lower()
    if req.method == 'GET':
        for param in req.query_params.items():        # [name,value] tuples
            if param[0].lower() == lcName:
                if param[1] == None:
                    return default
                return param[1]
        if default == None:
            raise InvalidPathError(_bad_title, bad_desc)                # Missing or incorrect casing
        return default                          # not in args, return default
    else:                                       # Assume PUT since we never route other methods
        formdata = get_form_data(req)
        if caseless:
            for fn in formdata.keys():
                if fn.lower() == lcName:
                    return formdata[fn]
        else:
            if name in formdata and formdata[name] != '':
                return formdata[name]
        if default == None:
            raise InvalidPathError(_bad_title, bad_desc)                # Missing or incorrect casing
        return default
    
def get_form_data(req: Request):
    if req._form_data == None: # adafruit_httpserver only parses form data on POST, so we have to do it manually ourselves
        req._form_data = FormData(req.body, req.headers, debug=req.server.debug)
    return req.form_data

#
# Log the request as soon as the resource handler gets it so subsequent
# logged messages are in the right order. Logs PUT body as well.
#
def log_request(req: Request):
    msg = f'{req.client_address} -> {req.method} {req.path}'
    logger.info(msg)
    if req.method == 'PUT' and req.body.count != 0:
        logger.info(f'{req.client_address} -> {get_form_data(req)}')

# ------------------------------------------------
# Incoming Pre-Logging and Request Quality Control
# ------------------------------------------------
class PreProcessRequest():
    """Decorator for responders that quality-checks an incoming request

    If there is a problem, this causes a ``400 Bad Request`` to be returned
    to the client, and logs the problem.

    """
    def __init__(self, maxdev):
        self.maxdev = maxdev
        """Initialize a ``PreProcessRequest`` decorator object.

        Args:
            maxdev: The maximun device number. If multiple instances of this device
                type are supported, this will be > 0.

        """

    #
    # Quality check of numerical value for trans IDs
    #
    @staticmethod
    def _pos_or_zero(val: str) -> bool:
        try:
            test = int(val)
            return test >= 0
        except ValueError:
            return False

    def _check_request(self, req: Request, devnum: str):  # Raise on failure
        if not self._pos_or_zero(devnum):
            msg = f'Request has bad Alpaca device number value {devnum}'
            logger.error(msg)
            raise InvalidPathError(_bad_title, msg)
        if int(devnum) > self.maxdev:
            msg = f'Device number {devnum} does not exist. Maximum device number is {self.maxdev}.'
            logger.error(msg)
            raise InvalidPathError(_bad_title, msg)
        test: str = get_request_field('ClientID', req, True, '0')   # Caseless, default = 0 if missing
        if not self._pos_or_zero(test):
            msg = f'Request has bad Alpaca ClientID value {test}'
            logger.error(msg)
            raise InvalidPathError(_bad_title, msg)
        if test == '0':
            req.query_params._add_field_value('ClientID', '0')                            # In case it's missing
        test: str = get_request_field('ClientTransactionID', req, True, '0') # Caseless, default = 0 if missing
        if not self._pos_or_zero(test):
            msg = f'Request has bad Alpaca ClientTransactionID value {test}'
            logger.error(msg)
            raise InvalidPathError(_bad_title, msg)
        if test == '0':
            req.query_params._add_field_value('ClientTransactionID', '0')                 # In case it's missing

    #
    # params contains {'devnum': n } from the URI template matcher
    # and format converter. This is the device number from the URI
    #
    def __call__(self, func):
        def wrapper(req: Request, devnum: str):        
            log_request(req)                            # Log even a bad request
            try:
                self._check_request(req, devnum)   # Raises to 400 error on check failure
                return func(req, devnum)
            except InvalidPathError as e:
                return Response(req, str(e), status=BAD_REQUEST_400)
        return wrapper

# ------------------
# PropertyResponse
# ------------------
class PropertyResponse():
    """JSON response for an Alpaca Property (GET) Request"""
    def __init__(self, value, req: Request, err = Success()):
        """Initialize a ``PropertyResponse`` object.

        Args:
            value:  The value of the requested property, or None if there was an
                exception.
            req: The Falcon Request property that was provided to the responder.
            err: An Alpaca exception class as defined in the exceptions
                or defaults to :py:class:`~exceptions.Success`

        Notes:
            * Bumps the ServerTransactionID value and returns it in sequence
        """
        self.ServerTransactionID = getNextTransId()
        self.ClientTransactionID = int(get_request_field('ClientTransactionID', req, False, 0))  #Caseless on GET
        if err.Number == 0 and not value is None:
            self.Value = value
            logger.info(f'{req.client_address} <- {str(value)}')
        self.ErrorNumber = err.Number
        self.ErrorMessage = err.Message

    @property
    def json(self) -> str:
        """Return the JSON for the Property Response"""
        return json.dumps(self.dict)
    
    @property
    def dict(self):
        response_obj = {"ServerTransactionID": self.ServerTransactionID, "ClientTransactionID": self.ClientTransactionID, "ErrorNumber": self.ErrorNumber, "ErrorMessage": self.ErrorMessage}
        if hasattr(self, "Value"):
            if isinstance(self.Value, list):
                simplified = []
                for state_value in self.Value:
                    if isinstance(state_value, StateValue):
                        simplified.append({"Name": state_value.Name, "Value": state_value.Value})
                    else:
                        simplified.append(state_value)
                response_obj["Value"] = simplified
            else:
                response_obj["Value"] = self.Value
        return response_obj

# --------------
# MethodResponse
# --------------
class MethodResponse():
    """JSON response for an Alpaca Method (PUT) Request"""
    def __init__(self, req: Request, err = Success(), value = None): # value useless unless Success
        """Initialize a MethodResponse object.

        Args:
            req: The Falcon Request property that was provided to the responder.
            err: An Alpaca exception class as defined in the exceptions
                or defaults to :py:class:`~exceptions.Success`
            value:  If method returns a value, or defaults to None

        Notes:
            * Bumps the ServerTransactionID value and returns it in sequence
        """
        self.ServerTransactionID = getNextTransId()
        # This is crazy ... if casing is incorrect here, we're supposed to return the default 0
        # even if the caseless check coming in returned a valid number. This is for PUT only.
        self.ClientTransactionID = int(get_request_field('ClientTransactionID', req, False, 0))
        if err.Number == 0 and not value is None:
            self.Value = value
            logger.info(f'{req.client_address} <- {str(value)}')
        self.ErrorNumber = err.Number
        self.ErrorMessage = err.Message


    @property
    def json(self) -> str:
        """Return the JSON for the Method Response"""
        return json.dumps(self.dict)
    
    @property
    def dict(self):
        response_obj = {"ServerTransactionID": self.ServerTransactionID, "ClientTransactionID": self.ClientTransactionID, "ErrorNumber": self.ErrorNumber, "ErrorMessage": self.ErrorMessage}
        if hasattr(self, "Value"):
            if isinstance(self.Value, list):
                simplified = []
                for state_value in self.Value:
                    if isinstance(state_value, StateValue):
                        simplified.append({"Name": state_value.Name, "Value": state_value.Value})
                    else:
                        simplified.append(state_value)
                response_obj["Value"] = simplified
            else:
                response_obj["Value"] = self.Value
        return response_obj


_stid = 0

def getNextTransId() -> int:
    global _stid
    _stid += 1
    return _stid