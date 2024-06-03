
# Author: Samet Azaboglu, M.Sc.
# The IO class is a base class that provides common I/O operations.
# The collect_files method is a static method that collects files with a specific extension from a directory.
# The decompress_files method is a static method that decompresses files in a directory.


import os
from modules.decompressor import PrefetchDecompressor
from modules.pf_data import PrefetchData


class IO:
    @staticmethod
    def collect_files(directory, extension):
        collected_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    collected_files.append(os.path.join(root, file))
                    print(f'[Success] File collected: {file}')

        return collected_files

    @staticmethod
    def decompress_files(files, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f'[Success] Output directory created: {output_dir}')
        for file in files:
            decomp = PrefetchDecompressor(
                file,
                os.path.join(output_dir, os.path.basename(file) + '_decompressed')
            )
            decomp.decompress_file(), True

    @staticmethod
    def read_prefetch_file_data(file):
        prefetch_data = PrefetchData()
        file_name, file_run_count, file_date_time = prefetch_data.read_prefetch_file(file)
        return file_name, file_run_count, file_date_time
