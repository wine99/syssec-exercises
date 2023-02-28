#!/usr/bin/env python3

import random
import sys
import time
from Crypto.Cipher import AES
from datetime import datetime
import os


def encrypt(input_file, output_file):
    random.seed(int(time.time()))
    key = random.randbytes(16)
    aes = AES.new(key, AES.MODE_GCM)

    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    ciphertext, tag = aes.encrypt_and_digest(data)

    with open(output_file, 'wb') as f_out:
        f_out.write(aes.nonce)  # 16 bytes
        f_out.write(tag)        # 16 bytes
        f_out.write(ciphertext) # len(data) bytes


def dec():
    file = 'ciphertext.bin'
    with open(file, 'rb') as f_in:
        nonce = f_in.read(16)
        tag = f_in.read(16)
        cipher = f_in.read()

    seed = int(datetime.fromisoformat('2023-02-22').timestamp())
    end_search = int(datetime.fromisoformat('2023-02-21').timestamp())
    while True:
        if seed < end_search:
            raise "failed"
        print(datetime.fromtimestamp(seed))
        random.seed(seed)
        key = random.randbytes(16)
        aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            plain = aes.decrypt_and_verify(cipher, tag)
            with open('plaintext', 'wb') as f_out:
                f_out.write(plain)
            return plain
        except:
            seed -= 1


if __name__ == '__main__':
    dec()
    exit()

    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} <src-file> <dst-file>', file=sys.stderr)
        exit(1)
    encrypt(sys.argv[1], sys.argv[2])
