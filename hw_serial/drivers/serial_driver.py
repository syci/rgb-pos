# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import os
import logging

_logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    _logger.error('Odoo module hw_serial depends on the pyserial python module')
    serial = None


class SerialDriver:
    def serial_do_operation(self, operation, params):
        result = {}
        ser = self.serial_open(params)
        if ser:
            try:
                if operation == 'read':
                    data = ser.readline()
                    result['data'] = data
                else:
                    ser.write(params.get('data', ''))
                result['status'] = 'ok'
            except serial.SerialException, message:
                result['status'] = 'error'
                result['message'] = str(message)
        else:
            result['status'] = 'error'
            result['message'] = 'The serial port was not found!'
        if ser:
            ser.close()
        return result

    def serial_open(self, params):
        try:
            port = params.get('port', '/dev/ttyUSB0')
            if not os.path.exists(port):
                _logger.error('Serial port not found')
                return None
            return serial.Serial(port,
                                 baudrate=params.get('baudrate', 9600),
                                 bytesize=params.get('bytesize', 8),
                                 stopbits=params.get('stopbits', 1),
                                 parity=params.get('parity', 'E'),
                                 timeout=float(params.get('timeout', 20)) / 1000,
                                 writeTimeout=float(params.get('timeout', 20)) / 1000)
        except Exception as e:
            _logger.error(str(e))
            return None