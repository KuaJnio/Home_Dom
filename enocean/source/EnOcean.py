import json


class EnOcean:
    def __init__(self, eo_data):
        self.data = eo_data

    def get_rorg(self):
        return self.data[0:2]

    def get_type(self):
        if self.get_rorg() == 'f6':
            return 'BUTTON'
        elif self.get_rorg() == 'a5':
            if (self.data[2:4] == '00') or (self.data[2:4] == '10'):
                return 'TEMPERATURE'
            else:
                return 'OCCUPANCY'
        elif self.get_rorg() == 'd5':
            return 'CONTACT'
        elif self.get_rorg() == 'd2':
            return 'ACTUATOR'
        else:
            return 'UNKNOWN'

    def get_id(self):
        if self.get_rorg() == 'f6':
            return self.data[4:12]
        elif self.get_rorg() == 'a5':
            return self.data[10:18]
        elif self.get_rorg() == 'd5':
            return self.data[4:12]
        elif self.get_rorg() == 'd2':
            return
        else:
            return 'UNKNOWN'

    def get_rssi(self):
        if self.get_rorg() == 'f6':
            return int(self.data[24:26], 16)*(-1)
        elif self.get_rorg() == 'a5':
            return int(self.data[30:32], 16)*(-1)
        elif self.get_rorg() == 'd5':
            return int(self.data[24:26], 16)*(-1)
        elif self.get_rorg() == 'd2':
            return 'UNKNOWN'
        else:
            return 'UNKNOWN'

    def get_data(self):
        if self.get_rorg() == 'f6':
            return self.data[2:4]
        elif self.get_rorg() == 'a5':
            return self.data[2:10]
        elif self.get_rorg() == 'd5':
            return self.data[2:4]
        elif self.get_rorg() == 'd2':
            return 'UNKNOWN'
        else:
            return 'UNKNOWN'

    def is_teach_in(self):
        if self.get_rorg() == 'f6':
            return False
        elif self.get_rorg() == 'a5':
            if int(self.get_data(), 16) & 8:
                return False
            return True
        elif self.get_rorg() == 'd5':
            if int(self.get_data(), 16) & 8:
                return False
            return True
        elif self.get_rorg() == 'd2':
            return False
        else:
            return False

    def get_button(self):
        data = self.get_data()
        if data == '00':
            return 'UNPRESSED'
        elif data == '10':
            return 'A1_PRESSED'
        elif data == '30':
            return 'A0_PRESSED'
        elif data == '50':
            return 'B1_PRESSED'
        elif data == '70':
            return 'B0_PRESSED'
        else:
            return 'UNKNOWN'

    def get_occupancy(self):
        if self.is_teach_in():
            return 'UNKNOWN'
        if int(self.get_data()[4:6], 16) < 128:
            return 'UNOCCUPIED'
        else:
            return 'OCCUPIED'

    def get_supply(self):
        if self.is_teach_in():
            return 'UNKNOWN'
        if int(self.get_data(), 16) & 1:
            return "{0:.2f}".format((int(self.get_data()[0:2], 16)*5)/250.0)
        else:
            return 'UNKNOWN'

    def get_contact(self):
        if self.is_teach_in():
            return 'UNKNOWN'
        if int(self.get_data(), 16) & 1:
            return 'CLOSED'
        else:
            return 'OPEN'

    def get_temp(self):
        if self.is_teach_in():
            return 'UNKNOWN'
        if int(self.get_data(), 16) & 2:
            return "{0:.2f}".format((int(self.get_data()[4:6], 16) * 40) / 250.0)

    def get_hum(self):
        if self.is_teach_in():
            return 'UNKNOWN'
        return "{0:.2f}".format((int(self.get_data()[2:4], 16) * 100) / 250.0)

    def get_payload(self):
        if self.get_type() == 'BUTTON':
            parsed_payload = json.JSONEncoder().encode({
                "type": self.get_type(),
                "id": self.get_id().upper(),
                "rssi": self.get_rssi(),
                "value": self.get_button()
            })
            return parsed_payload
        elif self.get_type() == 'OCCUPANCY':
            parsed_payload = json.JSONEncoder().encode({
                "type": self.get_type(),
                "id": self.get_id().upper(),
                "rssi": self.get_rssi(),
                "availability": self.get_occupancy(),
                "supplyVoltage": self.get_supply(),
                "TeachIn": self.is_teach_in()
            })
            return parsed_payload
        elif self.get_type() == 'TEMPERATURE':
            parsed_payload = json.JSONEncoder().encode({
                "type": self.get_type(),
                "id": self.get_id().upper(),
                "rssi": self.get_rssi(),
                "temperature": self.get_temp(),
                "humidity": self.get_hum(),
                "TeachIn": self.is_teach_in()
            })
            return parsed_payload
        elif self.get_type() == 'CONTACT':
            parsed_payload = json.JSONEncoder().encode({
                "type": self.get_type(),
                "id": self.get_id().upper(),
                "rssi": self.get_rssi(),
                "state": self.get_contact(),
                "TeachIn": self.is_teach_in()
            })
            return parsed_payload
        else:
            parsed_payload = json.JSONEncoder().encode({
                "error": "incorrect payload",
                "payload": self.data
            })
            return parsed_payload
