import json
import time

enocean_to_homedom = {
    "01A4C431": "EO_TEMPHUM_1",
    "01A4702D": "EO_TEMPHUM_2",
    "018176FF": "EO_TEMPHUM_3",
    "050B3CBE": "EO_PRESENCE_1",
    "050B3D62": "EO_PRESENCE_2",
    "050CB8B3": "EO_PRESENCE_3",
    "01805C9E": "EO_CONTACT_1",
    "0029D193": "EO_REMOTE_WHITE",
    "002B7AC5": "EO_REMOTE_PINK",
    "0032DB63": "EO_REMOTE_GREY",
    "002D2371": "EO_WALL_1",
    "002D234C": "EO_WALL_2"
}


class EnOcean:
    def __init__(self, eo_data):
        self.data = eo_data

    def get_rorg(self):
        return self.data[0:2]

    def get_type(self):
        if self.get_rorg() == 'f6':
            return 'HD_SWITCH'
        elif self.get_rorg() == 'a5':
            if (self.data[2:4] == '00') or (self.data[2:4] == '10'):
                return 'HD_TEMPHUM'
            else:
                return 'HD_PRESENCE'
        elif self.get_rorg() == 'd5':
            return 'HD_CONTACT'
        elif self.get_rorg() == 'd2':
            return 'HD_ACTUATOR'
        elif self.get_rorg() == 'd4':
            return 'HD_UTE'
        else:
            return 'HD_UNKNOWN'

    def get_id(self):
        if self.get_rorg() == 'f6':
            return 'HD_' + enocean_to_homedom.get(self.data[4:12].upper(), self.data[4:12].upper())
        elif self.get_rorg() == 'a5':
            return 'HD_' + enocean_to_homedom.get(self.data[10:18].upper(), self.data[10:18].upper())
        elif self.get_rorg() == 'd5':
            return 'HD_' + enocean_to_homedom.get(self.data[4:12].upper(), self.data[4:12].upper())
        elif self.get_rorg() == 'd2':
            return 'HD_' + enocean_to_homedom.get(self.data[8:16].upper(), self.data[8:16].upper())
        elif self.get_rorg() == 'd4':
            return 'HD_' + enocean_to_homedom.get(self.data[16:24].upper(), self.data[16:24].upper())
        else:
            return 'HD_UNKNOWN'

    def get_rssi(self):
        if self.get_rorg() == 'f6':
            return int(self.data[24:26], 16) * (-1)
        elif self.get_rorg() == 'a5':
            return int(self.data[30:32], 16) * (-1)
        elif self.get_rorg() == 'd5':
            return int(self.data[24:26], 16) * (-1)
        elif self.get_rorg() == 'd2':
            return int(self.data[28:30], 16) * (-1)
        elif self.get_rorg() == 'd4':
            return int(self.data[36:38], 16) * (-1)
        else:
            return 'HD_UNKNOWN'

    def get_data(self):
        if self.get_rorg() == 'f6':
            return self.data[2:4]
        elif self.get_rorg() == 'a5':
            return self.data[2:10]
        elif self.get_rorg() == 'd5':
            return self.data[2:4]
        elif self.get_rorg() == 'd2':
            return self.data[2:8]
        else:
            return 'HD_UNKNOWN'

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
            return '0'
        elif data == '10':
            return '1'
        elif data == '30':
            return '2'
        elif data == '50':
            return '3'
        elif data == '70':
            return '4'
        else:
            return 'HD_UNKNOWN'

    def get_occupancy(self):
        if self.is_teach_in():
            return 'HD_UNKNOWN'
        if int(self.get_data()[4:6], 16) < 128:
            return '0'
        else:
            return '1'

    def get_supply(self):
        if self.is_teach_in():
            return 'HD_UNKNOWN'
        if int(self.get_data(), 16) & 1:
            return "{0:.2f}".format((int(self.get_data()[0:2], 16) * 5) / 250.0)
        else:
            return 'HD_UNKNOWN'

    def get_contact(self):
        if self.is_teach_in():
            return 'HD_UNKNOWN'
        if int(self.get_data(), 16) & 1:
            return '1'
        else:
            return '0'

    def get_actuator_output(self):
        channel = (int(self.get_data()[2:4], 16) & 1) + 1
        if channel == 1:
            if int(self.get_data()[4:6], 16) & 127:
                #CHANNEL 1 ON
                return '0'
            else:
                #CHANNEL 1 OFF
                return '1'
        elif channel == 2:
            if int(self.get_data()[4:6], 16) & 127:
                #CHANNEL 2 ON
                return '2'
            else:
                #CHANNEL 2 OFF
                return '3'
        else:
            return 'HD_UNKNOWN'

    def get_temp(self):
        if self.is_teach_in():
            return 'HD_UNKNOWN'
        if int(self.get_data(), 16) & 2:
            return "{0:.2f}".format((int(self.get_data()[4:6], 16) * 40) / 250.0)

    def get_hum(self):
        if self.is_teach_in():
            return 'HD_UNKNOWN'
        return "{0:.2f}".format((int(self.get_data()[2:4], 16) * 100) / 250.0)

    def set_payload(self, feature, identifier, value):
        hd_payload = json.JSONEncoder().encode({
            "HD_FEATURE": feature,
            "HD_IDENTIFIER": identifier,
            "HD_VALUE": value,
            "HD_TIMESTAMP": round(time.time(), 3)
        })
        return hd_payload

    def get_payloads(self):
        payloads = []
        if self.get_type() == 'HD_SWITCH':
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_button() == 'HD_UNKNOWN' and not self.is_teach_in():
                payload = self.set_payload(self.get_type(), self.get_id(), int(self.get_button()))
                payloads.append(payload)
        elif self.get_type() == 'HD_PRESENCE':
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_occupancy() == 'HD_UNKNOWN' and not self.is_teach_in():
                payload = self.set_payload(self.get_type(), self.get_id(), int(self.get_occupancy()))
                payloads.append(payload)
        elif self.get_type() == 'HD_TEMPHUM':
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_temp() == 'HD_UNKNOWN' and not self.is_teach_in():
                payload = self.set_payload("HD_TEMPERATURE", self.get_id(), float(self.get_temp()))
                payloads.append(payload)
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_hum() == 'HD_UNKNOWN' and not self.is_teach_in():
                payload = self.set_payload('HD_HUMIDITY', self.get_id(), float(self.get_hum()))
                payloads.append(payload)
        elif self.get_type() == 'HD_CONTACT':
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_contact() == 'HD_UNKNOWN' and not self.is_teach_in():
                payload = self.set_payload(self.get_type(), self.get_id(), int(self.get_contact()))
                payloads.append(payload)
        elif self.get_type() == 'HD_ACTUATOR':
            if not self.get_id() == 'HD_UNKNOWN' and not self.get_actuator_output() == 'HD_UNKNOWN':
                payload = self.set_payload(self.get_type(), self.get_id(), int(self.get_actuator_output()))
                payloads.append(payload)
        return payloads
