import controlpanel.view.setupwindows as setupwindows

import random


class SunBlindModel:
    def __init__(self, module):
        self.min_roll_out = 0
        self.max_roll_out = 2.5
        self.status_sun_blind = "open"
        self.status_light_sensor = "Not Available"
        self.status_temp_sensor = "good"
        self.status_ultrasoon_sensor = "good"
        self.data_x = []
        self.data_temp = []
        self.data_light = []
        self.data_ultrasoon = []
        self.module = module

    def set_min_roll_out(self, min_roll_out):
        if min_roll_out < self.max_roll_out:
            self.min_roll_out = round(min_roll_out, 2)
            print("self.min_roll_out is set to " + str(self.min_roll_out))
        else:
            setupwindows.MakeWindows.make_min_error()

    def set_max_roll_out(self, max_roll_out):
        if max_roll_out > self.min_roll_out:
            self.max_roll_out = round(max_roll_out, 2)
            print("self.max_roll_out is set to " + str(self.max_roll_out))
        else:
            setupwindows.MakeWindows.make_max_error()

    def get_min_roll_out(self):
        return self.min_roll_out

    def get_max_roll_out(self):
        return self.max_roll_out

    def get_status(self):
        status = (self.status_light_sensor, self.status_temp_sensor, self.status_ultrasoon_sensor,
                  self.status_sun_blind)
        return status

    def set_status_light_sensor(self, status):
        self.status_light_sensor = status

    def set_status_temp_sensor(self, status):
        self.status_temp_sensor = status

    def set_status_ultrasoon_sensor(self, status):
        self.status_ultrasoon_sensor = status

    def set_status_sun_blind(self, status):
        self.status_sun_blind = status

    def roll_out(self, unit):
        self.status = "open"
        print("sun blind is " + self.status)
        # call serial with unit and give self.max_roll_out as param
        pass

    def roll_in(self, unit):
        self.status = "closed"
        print("sun blind is " + self.status)
        # call serial with unit and give self.min_roll_out as param
        pass

    def get_data_x(self):
        return self.data_x

    def get_data_temp(self):
        return self.data_temp

    def get_data_light(self):
        return self.data_light

    def get_last_data_temp(self):
        if len(self.data_temp) > 0 and self.status_temp_sensor == "good":
            return self.data_temp[len(self.data_temp) - 1]
        else:
            return "Not Available"

    def get_last_data_light(self):
        if len(self.data_light) > 0 and self.status_light_sensor == "good":
            return self.data_light[len(self.data_light) - 1]
        else:
            return "Not Available"

    def get_last_data_ultrasoon(self):
        if len(self.data_ultrasoon) > 0 and self.status_ultrasoon_sensor == "good":
            return self.data_ultrasoon[len(self.data_ultrasoon) - 1]
        else:
            return "Not Available"

    def generate_new_data(self):
        received_data = self.module.decode_retrieved_data()
        self.add_new_data(received_data)

        # Sends instructions to module to return temperature and light
        self.module.send_data(0xFD)  # Light
        self.module.send_data(0xFE)  # Temperature

    def add_new_data(self, data):
        if 'Temperature' in data:
            for temp in data['Temperature']:
                self.data_temp.append(temp)
                if len(self.data_temp) > 100:
                    self.data_temp.pop(0)
        if 'Light' in data:
            for light in data['Light']:
                self.data_light.append(light)
                if len(self.data_light) > 100:
                    self.data_light.pop(0)
        if 'Ultrasoon' in data:
            for ultrasoon in data['ultrasoon']:
                self.data_ultrasoon.append(ultrasoon)
                if len(self.data_ultrasoon) > 100:
                    self.data_ultrasoon.pop(0)
        if 'Status' in data:
            if 'SunBlind' in data['Status']:
                self.status_sun_blind = data['Status']['SunBlind']
            if 'Temperature' in data['Status']:
                self.status_temp_sensor = data['Status']['Temperature']
            if 'Light' in data['Status']:
                self.status_light_sensor = data['Status']['Light']
            if 'Ultrasoon' in data['Status']:
                self.status_ultrasoon_sensor = data['Status']['Ultrasoon']
