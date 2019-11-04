data_types = {
    0xFD: 'Light',
    0xFE: 'Temperature'
}


class DataReader:
    @staticmethod
    def decode_and_return_data(data):
        current_data_type = None
        sequence_start_index = 0
        sequence_started = False

        temp_data = {}

        for i in range(len(data)):
            if data[i] in data_types.keys() and not sequence_started:
                current_data_type = data[i]
                sequence_start_index = i + 1
                sequence_started = True

            if sequence_started:
                if data[i] is 0x00 and data[i - 1] is current_data_type and data[i - 2] is 0x00:
                    sequence_started = False
                    sequence_stop_index = i - 2

                    if current_data_type in temp_data.keys():
                        temp_data[current_data_type].extend(data[sequence_start_index:sequence_stop_index])
                    else:
                        temp_data[current_data_type] = data[sequence_start_index:sequence_stop_index]

                    current_data_type = None

        return temp_data
