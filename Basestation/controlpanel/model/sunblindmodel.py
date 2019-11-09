from serial import SerialException
import controlpanel.view.setupwindows as setupwindows
from collections import Counter


class SunBlindModel:
    def __init__(self, module):
        self.min_roll_out = 0
        self.max_roll_out = 2.5
        self.status_sun_blind = "closed"
        self.status_light_sensor = "Not Available"
        self.status_temp_sensor = "Good"
        self.status_ultrasoon_sensor = "Good"
        self.data_x = []
        self.data_temp = []
        self.data_light = []
        self.data_ultrasoon = []
        self.module = module
        self.light_intensity = 75
        self.temperature = 25

    @staticmethod
    def get_mode(data):
        n = len(data)
        if n >= 100:
            data_counter = Counter(data)
            get_mode = dict(data_counter)
            mode = [k for k, v in get_mode.items() if v == max(list(data_counter.values()))]
            if len(mode) > 1:
                return round(sum(mode) / len(mode))
            else:
                return mode[0]
        else:
            return "dataset to small"

    def check_weather(self):
        mode_light = SunBlindModel.get_mode(self.data_light)
        mode_temp = SunBlindModel.get_mode(self.data_temp)

        if isinstance(mode_light, int) and self.status_light_sensor == "Good":
            if mode_light >= self.light_intensity and self.status_sun_blind == "closed":
                return "open"
        if isinstance(mode_temp, int) and self.status_temp_sensor == "Good":
            if mode_temp >= self.temperature and self.status_sun_blind == "closed":
                return "open"
        if isinstance(mode_light, int) and isinstance(mode_temp, int) and self.status_light_sensor == "Good" and self.status_temp_sensor == "Good":
            if mode_light < self.light_intensity and mode_temp < self.temperature and self.status_sun_blind == "open":
                return "close"
        if isinstance(mode_light, int) and self.status_light_sensor == "Good" and self.status_temp_sensor == "Not Available":
            if mode_light < self.light_intensity and self.status_sun_blind == "open":
                return "close"
        if isinstance(mode_temp, int) and self.status_temp_sensor == "Good" and self.status_light_sensor == "Not Available":
            if mode_temp < self.temperature and self.status_sun_blind == "open":
                return "close"
        return None

    def set_min_roll_out(self, min_roll_out):
        if min_roll_out < self.max_roll_out:
            self.min_roll_out = round(min_roll_out, 2)
            setupwindows.MakeWindows.update_min_inputs()
        else:
            setupwindows.MakeWindows.make_min_error()

    def set_max_roll_out(self, max_roll_out):
        if max_roll_out > self.min_roll_out:
            self.max_roll_out = round(max_roll_out, 2)
            setupwindows.MakeWindows.update_max_inputs()
        else:
            setupwindows.MakeWindows.make_max_error()

    def get_min_roll_out(self):
        return self.min_roll_out

    def get_max_roll_out(self):
        return self.max_roll_out

    def set_light_intensity(self, value):
        self.light_intensity = value
        setupwindows.MakeWindows.update_light_intensity_inputs()

    def set_temp(self, value):
        self.temperature = value
        print("self.temperature is set to " + str(self.temperature))
        setupwindows.MakeWindows.update_temp_inputs()

    def get_light_intensity(self):
        return self.light_intensity

    def get_temp(self):
        return self.temperature

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

    def roll_out(self):
        self.status_sun_blind = "open"
        print("sun blind is " + self.status_sun_blind)
        # call serial with unit and give self.max_roll_out as param
        pass

    def roll_in(self):
        self.status_sun_blind = "closed"
        print("sun blind is " + self.status_sun_blind)
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

        try:
            # Sends instructions to module to return temperature and light
            self.module.send_data(0xFD)  # Light
            self.module.send_data(0xFE)  # Temperature
        except SerialException:
            self.module.close_connection()

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
