import paramiko
import argparse
import json


def get_filename():
    parser = argparse.ArgumentParser(description="Get file")
    parser.add_argument('-f', '--file', dest='filename', action='store', required=True)
    return parser.parse_args("-f test_file.txt".split()).filename

