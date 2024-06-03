# Description: This script is used to decompress prefetch files.

import binascii
import ctypes
import struct
import sys


class PrefetchDecompressor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.SIZE_T = ctypes.c_uint
        self.DWORD = ctypes.c_uint32
        self.USHORT = ctypes.c_uint16
        self.UCHAR  = ctypes.c_ubyte
        self.ULONG = ctypes.c_uint32

    @staticmethod
    def to_hex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress_file(self):
        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
        except AttributeError:
            sys.exit('Windows version >=8.')

        RtlGetCompressionWorkSpaceSize = \
            ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

        with open(self.input_file, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()

            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF
            if magic != 0x004d414d :
                sys.exit('[Error] Invalid file signature. Please ensure you are using a valid prefetch file.')
            if magic == 0x53434341:
                sys.exit('[Error] File is already decompressed.')

            if crcck:
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L',0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)
                if crc != file_crc:
                    sys.exit('[Error] File integrity check failed. CRC {0:x} - {1:x}!'.format(crc, file_crc))

            compressed_size = len(compressed)

            ntCompressBufferWorkSpaceSize = self.ULONG()
            ntCompressFragmentWorkSpaceSize = self.ULONG()

            ntstatus = RtlGetCompressionWorkSpaceSize(self.USHORT(calgo),
                ctypes.byref(ntCompressBufferWorkSpaceSize),
                ctypes.byref(ntCompressFragmentWorkSpaceSize))

            if ntstatus:
                sys.exit('[Error] Failed to get workspace size. Error code: {}'.format(
                    self.to_hex(ntstatus, 32)))

            ntCompressed = (self.UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (self.UCHAR * decompressed_size)()
            ntFinalUncompressedSize = self.ULONG()
            ntWorkspace = (self.UCHAR * ntCompressFragmentWorkSpaceSize.value)()

            ntstatus = RtlDecompressBufferEx(
                self.USHORT(calgo),
                ctypes.byref(ntDecompressed),
                self.ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                self.ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))

            if ntstatus:
                sys.exit('[Error] Decompression failed. Error code: {}'.format(
                    self.to_hex(ntstatus, 32)))

            if ntFinalUncompressedSize.value != decompressed_size:
                print('[Warning] The decompressed file size does not match the original file size.')

            with open(self.output_file, 'wb') as fout:
                fout.write(bytearray(ntDecompressed))

            print('[Success] File decompressed successfully. Output file: {}'.format(self.output_file))
