
# Author: Samet Azaboglu, M.Sc.
# Description: This script decompresses prefetch files for purposes of forensic.
# This script usable for NT-based operating systems.
# Prefetch file location: C:\Windows\Prefetch or %SystemRoot%\Prefetch


"""
+----------------------------------LEGAL DISCLAIMER----------------------------------+
Usage of this script for attacking targets without prior mutual consent is illegal (like anti-forensics),
and it is the end user's responsibility to obey all applicable laws.
The author assumes no liability and is not responsible for any misuse or damage caused by this script.
+----------------------------------LEGAL DISCLAIMER----------------------------------+
"""

from modules.io import IO

if __name__ == '__main__':
    ## Decompressing prefetch files
    compressed_prefetch_location = 'C:\\Windows\\Prefetch'
    decompressed_prefetch_location = '<decompressed_folder_location>'

    print('[info] Decompressing prefetch files...')
    compressed_pf_Files = IO.collect_files(
        compressed_prefetch_location,
        '.pf'
    )

    if IO.decompress_files(compressed_pf_Files, decompressed_prefetch_location):
        print('[info] Decompression completed.')


    ## Reading prefetch file data
    decompressed_pf_Files = IO.collect_files(
        decompressed_prefetch_location,
        '.pf_decompressed'
    )

    print('[info] Reading prefetch file data...')
    for i in range(len(decompressed_pf_Files)):
        print(decompressed_pf_Files[i])
        data = IO.read_prefetch_file_data(decompressed_pf_Files[i])
        print(data)

    print('[info] Reading prefetch file data completed.')

