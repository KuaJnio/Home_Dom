import serial
from EnOcean import EnOcean
from threading import Thread
import time
import datetime
import codecs

u8crc8table = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6A, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8D, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]


class SerialReader(Thread):
    def __init__(self, device, mqtt_client):
        Thread.__init__(self)
        self.device = device
        self.mqtt_client = mqtt_client
        try:
            self.ser = serial.Serial(self.device, 57600, timeout=0)
        except serial.SerialException:
            print('Could not connect to serial device' + device)
        self.app_version = ''
        self.api_version = ''
        self.chip_id = ''
        self.application = ''
        self.base_id = ''
        self.base_id_writes = ''
        self.data_length = ''
        self.op_data_length = ''
        self.packet_type = ''
        self.header_crc = ''
        self.total_data_length = 0
        self.serial_data = ''
        self.last_message = ''

    def clean(self):
        self.data_length = ''
        self.op_data_length = ''
        self.packet_type = ''
        self.header_crc = ''
        self.total_data_length = 0
        self.serial_data = ''

    @staticmethod
    def proccrc8(crc, u8data):
        return u8crc8table[(crc ^ u8data) & 0xff]

    def check_header_crc(self):
        u8crc_header = 0
        u8crc_header = (self.proccrc8(u8crc_header, int(self.data_length, 16) >> 8))
        u8crc_header = (self.proccrc8(u8crc_header, int(self.data_length, 16) & 0xff))
        u8crc_header = (self.proccrc8(u8crc_header, int(self.op_data_length, 16)))
        u8crc_header = (self.proccrc8(u8crc_header, int(self.packet_type, 16)))
        if u8crc_header == int(self.header_crc, 16):
            return True
        else:
            return False

    def check_data_crc(self, serial_data):
        u8crc_data = 0
        i = 0
        while i < len(serial_data) - 2:
            u8crc_data = self.proccrc8(u8crc_data, (int(serial_data[i] + serial_data[i + 1], 16) & 0xff))
            i += 2
        if u8crc_data == int(serial_data[len(serial_data) - 2] + serial_data[len(serial_data) - 1], 16):
            return True
        else:
            return False

    def check_packet_type(self, x):
        if self.packet_type == x:
            return True
        else:
            return False

    def get_serial_data(self):
        self.clean()
        s = 0
        while s != '55':
            if self.ser.inWaiting() != 0:
                s = str(codecs.encode(self.ser.read(1), 'hex'), 'utf-8')
            while self.ser.inWaiting() < 5:
                time.sleep(0.1)
        self.data_length = str(codecs.encode(self.ser.read(2), 'hex'), 'utf-8')  # read length field
        self.op_data_length = str(codecs.encode(self.ser.read(1), 'hex'), 'utf-8')  # read op length field
        self.packet_type = str(codecs.encode(self.ser.read(1), 'hex'), 'utf-8')  # read packet type field
        self.header_crc = str(codecs.encode(self.ser.read(1), 'hex'), 'utf-8')  # read header crc field

        if self.check_header_crc():
            self.total_data_length = (int(self.data_length, 16) + int(self.op_data_length, 16))
            while self.ser.inWaiting() < self.total_data_length:
                time.sleep(0.1)
            serial_data = str(codecs.encode(self.ser.read(self.total_data_length + 1), 'hex'), 'utf-8')
            if self.check_data_crc(serial_data):
                return serial_data
            return "Data CRC Failed"
        return "Header CRC Failed"

    def calc_esp3header_crc(self, telegram_header):
        u8crc = 0
        u8crc = self.proccrc8(u8crc, telegram_header[1])
        u8crc = self.proccrc8(u8crc, telegram_header[2])
        u8crc = self.proccrc8(u8crc, telegram_header[3])
        u8crc = self.proccrc8(u8crc, telegram_header[4])
        return u8crc

    def calc_esp3data_crc(self, telegram_data):
        u8crc = 0
        for index in range(len(telegram_data)):
            u8crc = self.proccrc8(u8crc, telegram_data[index])
        return u8crc

    def calc_esp3header(self, packet_type, packet_data, *arg):  # assumes 0 optional data
        p_header = [0x55]  # Start byte
        pass
        p_header.append(0x00)  # MSB data length
        p_header.append(len(packet_data))  # LSB data length
        if len(arg) == 0:
            p_header.append(0x00)  # optional data length
        else:
            p_header.append(arg[0])
        p_header.append(packet_type)  # packet type
        p_header.append(self.calc_esp3header_crc(p_header))  # Header crc
        return p_header

    def send_esp3packet(self, packet_type, packet_data):
        p_esp3packet = self.calc_esp3header(packet_type, packet_data)
        p_esp3packet += packet_data
        p_esp3packet.append(self.calc_esp3data_crc(packet_data))
        for index in range(len(p_esp3packet)):
            p_esp3packet[index] = chr(p_esp3packet[index])
            self.ser.write(p_esp3packet[index].encode('utf-8'))

    def command_read_base_id(self):
        self.send_esp3packet(0x05, [0x08])

    def parse_responde_code(self):
        if int(self.serial_data[0:1], 16) == 0x00:
            tmp_str = ""
            i = 2
            while i < 10:
                tmp_str += self.serial_data[i] + self.serial_data[i + 1]
                i += 2
            self.base_id = tmp_str
            print("BaseId: " + tmp_str)

            self.base_id_writes = self.serial_data[10] + self.serial_data[11]
        else:
            print("Error in response data:" + self.serial_data[0])

    def run(self):
        self.command_read_base_id()
        while True:
            self.serial_data = self.get_serial_data()
            self.last_message = datetime.datetime.now()
            if self.check_packet_type('01'):
                obj_enocean = EnOcean(self.serial_data)
                payloads = obj_enocean.get_payloads()
                for payload in payloads:
                    self.mqtt_client.publish("inputs", payload)
            elif self.check_packet_type('02'):
                self.parse_responde_code()


def create_serial_reader(device, mqtt_client):
    serial_reader_tmp = SerialReader(device, mqtt_client)
    serial_reader_tmp.daemon = True
    serial_reader_tmp.start()
    return serial_reader_tmp
