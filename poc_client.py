from Client import Client

import time
import hashlib



def main():

    # Setup
    c = Client('localhost', 8000)
    c.run()

    secret = listen_for_secret(c)

    # Loop

    while True:

        incoming = decrypt_incoming(c.recv(), secret)

        command = incoming & 255
        potential = (incoming >> 8) & 255
        challenge = incoming >> 16

        print(f"Receiving-> command = {command}, potential = {potential}, challenge = {challenge}")

        response = solve_challenge(challenge)
        print(f"Challenge response: {response}")
        c.send(encrypt_response(response, secret))
        secret = mutate_secret(response, secret)
        print(f"Secret mutated. New secret is: {secret}")

        time.sleep(0.2)

def listen_for_secret(c):

    secret = c.recv()
    print("Received secret")
    c.send(secret)

    return secret

def encrypt_response(payload, secret):

    encrypted_response = int(payload) ^ int(secret) # Crude "encryption" for PoC purposes

    return str(encrypted_response)

def decrypt_incoming(incoming, secret):

    return int(incoming) ^ int(secret)

def solve_challenge(challenge):

    md5 = hashlib.md5(challenge.to_bytes(8, 'big'))
    return int(md5.hexdigest()[:8], 16) # 4 hex pairs = 4 bytes = 32 bits

def mutate_secret(modifier, secret):

    return str(int(secret) ^ int(modifier))

if __name__ == "__main__":
    
    main()