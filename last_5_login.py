import argparse
import os
from pssh.clients import ParallelSSHClient


def read_host(file):
    f = open(file.filename, 'r')
    content = f.read().splitlines()
    f.close()
    return content


"""
BIG assumption that the hostnames (or IPs) in the file to be passed in here, has
already setup the neccessary SSH key authentication, otherwise, this script will 
timeout and spit out suggesting authentication timeout error. 
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='file path for the host file')
    parser.add_argument('-f', dest="filename", required=True, type=str, help='file path for the host file')

    args = parser.parse_args()

    client = ParallelSSHClient(read_host(args))

    output = client.run_command('last -5')

    for host, host_output in output.items():
        for line in host_output.stdout:
            print(line)
