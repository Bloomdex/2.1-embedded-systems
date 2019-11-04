import controlpanel.view.setupwindows as setupwindows
import random

class SunBlindModel:
    def __init__(self):
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
        self.status_sun_blindr = status

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
        if len(self.data_x) != 0:
            self.data_x.append(self.data_x[len(self.data_x) - 1] + 1)
        else:
            self.data_x.append(0)
        self.data_temp.append(random.randint(10, 50))
        self.data_light.append(random.randint(40, 100))
        if len(self.data_x) > 100:
            self.data_x.pop(0)
            self.data_temp.pop(0)
            self.data_light.pop(0)

