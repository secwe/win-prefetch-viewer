# Author: Samet Azaboglu, M.Sc.
# The PrefetchData class is a class that analyze prefetch files.

import datetime


class PrefetchData:
    def __init__(self):
        self.file_name_offset = 0x10
        self.file_run_count_offset = 0xd0
        self.file_executed_time_offsets = [0x80, 0x88, 0x90, 0x98, 0xa0, 0xa8, 0xb0, 0xb8]

        self.file_names = []
        self.file_run_counts = []
        self.file_executed_times = []

    def read_prefetch_file(self, file_path):
        self.file_names.clear()
        self.file_run_counts.clear()
        self.file_executed_times.clear()

        with open(file_path, 'rb') as file:
            file.seek(self.file_name_offset)
            file_name = file.read(60).decode('utf-16').split('\x00')[0]

            file.seek(self.file_run_count_offset)
            file_run_count = int.from_bytes(file.read(4), byteorder='little')

            for offset in self.file_executed_time_offsets:
                file.seek(offset)
                file_executed_time = int.from_bytes(file.read(8), byteorder='little')
                converted_real_time = file_executed_time / 10_000_000 - 11_644_473_600
                self.file_executed_times.append(converted_real_time)

            self.file_names.append(file_name)
            self.file_run_counts.append(file_run_count)

            datetime_objects = []
            for timestamp in self.file_executed_times:
                try:
                    dt_object = datetime.datetime.fromtimestamp(timestamp)
                    datetime_objects.append(dt_object)
                except OSError as e:
                    print(f"Invalid timestamp {timestamp}: {e}")

            return self.file_names, self.file_run_counts, datetime_objects
