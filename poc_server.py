from Server import Server

import time
import random
import hashlib



def main():

    # Setup
    s = Server('localhost', 8000)
    s.run()

    secret = generate_secret()
    s.send(secret)
    ack = s.recv()

    if ack == secret:
        print("Secret sharing was successful")

    # Loop
    challenge = 0
    responded = True

    while True:

        command, potential = get_command()
        if responded:
            challenge = generate_challenge()

        payload = create_payload(command, potential, challenge)
        print(f"Sending-> command = {command}, potential = {potential}, challenge = {challenge}")
        s.send(encrypt_payload(payload, secret))

        expected_response = solve_challenge(challenge)
        print(f"Expected response: {expected_response}, ", end="")

        incoming = decrypt_incoming(s.recv(), secret)
        print(f"Actual response: {incoming} | ", end="")

        if incoming == str(expected_response):
            print("Match")
            responded = True
            secret = mutate_secret(incoming, secret)
            print(f"Secret mutated. New secret is: {secret}")
            
        else:
            print("Different")
            responded = False

    time.sleep(0.2) #       

def generate_secret():

    low_32 = int("1"+(("0")*31), 2)
    high_32 = int("1"*32, 2)

    return str(random.randint(low_32, high_32))

def generate_challenge():

    low_16 = int("1" + (("0")*15), 2)
    high_16 = int("1" * 16, 2)

    return random.randint(low_16, high_16)

def get_command():
    # Returns command and potential from physical controls.
    command = random.randint(0, 255) # 1 Byte for command
    potential = random.randint(0, 255) # 1 Byte for potential. Potential is analogue from physical controls

    return (command, potential)

def create_payload(command, potential, challenge):

    payload = command
    payload += potential << 8
    payload += challenge << 16

    return payload

def encrypt_payload(payload, secret):

    encrypted_payload = int(payload) ^ int(secret) # Crude "encryption" for PoC purposes

    return str(encrypted_payload)

def decrypt_incoming(incoming, secret):

    return str(int(incoming) ^ int(secret))

def solve_challenge(challenge):

    md5 = hashlib.md5(challenge.to_bytes(8, 'big'))
    return int(md5.hexdigest()[:8], 16) # 4 hex pairs = 4 bytes = 32 bits

def mutate_secret(modifier, secret):

    return str(int(secret) ^ int(modifier))

if __name__ == "__main__":

    main()