import argparse






if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("server", nargs='?', default="localhost")
    fields = parser.parse_args()
