import serial
            
class SerialConn(serial):
    def __init__(self) :
        self.ser=serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    def send_data(self,move):
        self.ser.flush()
        self.ser.write(b"{}".format(move))
    def wait_data(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decote('utf-8').rstrip()
            print(line)
            return line