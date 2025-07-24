import sys
import segno
from tqdm import tqdm
import time

import secrets
import base64
import hmac
import hashlib
import struct


# ========= function for generating a secret ========
def generate_shared_secret():
    return secrets.token_bytes(10)


# ========= function for generating the QR code ========
def gen_qr(user_id):
    # Example URI: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    code1 = "otpauth://totp/Google%20Authenticator:"
    code2 = "?secret="
    code3 = "&issuer=Google%20Authenticator"

    secret = base64.b32encode(generate_shared_secret()).decode('utf-8')  # generate secret key
    
    uri = code1 + user_id + code2 + secret + code3
    print(" >> URI generated: ", uri)

    # Store secret into a file named "secret.txt"
    with open("secret.txt", "w") as file:
        file.write(secret)

    # Generate QR code based on the URI using segno
    qrcode = segno.make(uri, micro=False)
    qrcode.save('qr_code.png')

    print(" >> QR code saved as qr_code.png")
    return


# ========= function for generating the One-Time Password ========
def generate_otp(secret_base32, digits=6, time_step=30):
    key = base64.b32decode(secret_base32, casefold=True)

    # Get the current time step (TOTP counter)
    current_time = int(time.time())
    counter = current_time // time_step

    # Convert the counter to an 8-byte big-endian byte array
    counter_bytes = struct.pack(">Q", counter)

    # Create an HMAC-SHA1 hash using the secret key and the counter
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Get the offset from the last nibble
    offset = hmac_hash[-1] & 0x0F

    selected_bytes = hmac_hash[offset:offset+4]

    # Convert those 4 bytes to a big-endian integer
    code_int = struct.unpack(">I", selected_bytes)[0]

    # Remove the sign bit
    code_int = code_int & 0x7FFFFFFF

    # Get only the number of digits requested
    otp = code_int % (10 ** digits)

    # Pad with leading zeros if necessary
    return str(otp).zfill(digits)


# ========= function for displaying OTP every 30 sec ========
def get_otp(t=30):
    # Open and read file containing secret
    try:
        with open("secret.txt", "r") as file:
            secret = file.readline().strip()
    except FileNotFoundError:
        print(" >> Error: 'secret.txt' not found. Please generate the QR code first.")
        return

    while True:
        otp = generate_otp(secret)
        seconds_left = int(t - (time.time() % t))
        print(" > Generated OTP:", otp, "| Valid for", seconds_left, "seconds")

        for _ in tqdm(range(seconds_left), desc="Waiting…", ncols=75):
            time.sleep(1)


# ========= main function for command handling ========
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")
    elif sys.argv[1] == "--generate-qr" and len(sys.argv) == 3:
        gen_qr(sys.argv[2])
    elif sys.argv[1] == "--get-otp" and len(sys.argv) == 2:
        get_otp()
    else:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")
