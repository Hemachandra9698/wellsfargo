import argparse

# help flag provides flag help
# store_true actions stores argument as True

parser = argparse.ArgumentParser()

parser.add_argument('-port', '--port',
                    help="Flask server port number", type=int, default=5001)
parser.add_argument('-host', '--host',
                    help="Flask server host name", type=str, default='0.0.0.0')


def parse_arguments():
    args = parser.parse_args()
    return args
