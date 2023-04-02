import time
from serial import Serial

class SerialPort:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser=Serial(port,baudrate,timeout)

    def readData(self):
        data=self.ser.read()
        if(data):
            return data
        else:
            self.ser.readData()

    def write(self, data):
        self.ser.write(b"{}".format(data))
        time.sleep(1)

    def close(self):
        self.port.close()