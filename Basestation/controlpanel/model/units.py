import controlpanel.model.sunblindmodel as sunblindmodel


class Units:
    units = []

    @staticmethod
    def fill_units(arduinos):
        for arduino in arduinos:
            arduinos[arduino].reader.start()
            Units.units.append(sunblindmodel.SunBlindModel(arduinos[arduino]))

    @staticmethod
    def add_unit_to_units(arduino):
        Units.units.append(arduino)

    @staticmethod
    def set_unit_min(unit, value):
        sunblind = Units.units[unit]
        sunblind.set_min_roll_out(value)

    @staticmethod
    def set_unit_max(unit, value):
        sunblind = Units.units[unit]
        sunblind.set_max_roll_out(value)

    @staticmethod
    def get_unit_min(unit):
        sunblind = Units.units[unit]
        return sunblind.get_min_roll_out()

    @staticmethod
    def get_unit_max(unit):
        sunblind = Units.units[unit]
        return sunblind.get_max_roll_out()

    @staticmethod
    def set_unit_light_intensity(unit, value):
        sunblind = Units.units[unit]
        sunblind.set_light_intensity(value)

    @staticmethod
    def set_unit_temp(unit, value):
        sunblind = Units.units[unit]
        sunblind.set_temp(value)

    @staticmethod
    def get_unit_light_intensity(unit):
        sunblind = Units.units[unit]
        return sunblind.get_light_intensity()

    @staticmethod
    def get_unit_temp(unit):
        sunblind = Units.units[unit]
        return sunblind.get_temp()

    @staticmethod
    def get_status(unit):
        sunblind = Units.units[unit]
        return sunblind.get_status()

    @staticmethod
    def set_status_light_sensor(status, unit):
        sunblind = Units.units[unit]
        sunblind.set_status_light_sensor(status)

    @staticmethod
    def set_status_temp_sensor(status, unit):
        sunblind = Units.units[unit]
        sunblind.set_status_temp_sensor(status)

    @staticmethod
    def set_status_ultrasoon_sensor(status, unit):
        sunblind = Units.units[unit]
        sunblind.set_status_ultrasoon_sensor(status)

    @staticmethod
    def set_status_sun_blind(status, unit):
        sunblind = Units.units[unit]
        sunblind.set_status_sun_blind(status)

    @staticmethod
    def roll_out_unit(unit):
        sunblind = Units.units[unit]
        sunblind.roll_out()

    @staticmethod
    def roll_in_unit(unit):
        sunblind = Units.units[unit]
        sunblind.roll_in()

    @staticmethod
    def get_data_x(unit):
        sunblind = Units.units[unit]
        return sunblind.get_data_x()

    @staticmethod
    def get_data_temp(unit):
        sunblind = Units.units[unit]
        return sunblind.get_data_temp()

    @staticmethod
    def get_data_light(unit):
        sunblind = Units.units[unit]
        return sunblind.get_data_light()

    @staticmethod
    def get_last_data_x(unit):
        sunblind = Units.units[unit]
        return sunblind.get_last_data_x()

    @staticmethod
    def get_last_data_temp(unit):
        sunblind = Units.units[unit]
        return sunblind.get_last_data_temp()

    @staticmethod
    def get_last_data_light(unit):
        sunblind = Units.units[unit]
        return sunblind.get_last_data_light()

    @staticmethod
    def get_last_data_ultrasoon(unit):
        sunblind = Units.units[unit]
        return sunblind.get_last_data_ultrasoon()

    @staticmethod
    def generate_new_data(unit):
        sunblind = Units.units[unit]
        sunblind.generate_new_data()

    @staticmethod
    def check_if_module_is_connected(unit):
        sunblind = Units.units[unit]
        return sunblind.module.is_connected

    @staticmethod
    def check_weather_unit(unit):
        sunblind = Units.units[unit]
        return sunblind.check_weather()
