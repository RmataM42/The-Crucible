from argparse import Namespace, ArgumentParser

parser = ArgumentParser(description='It does frame IO... stuff..')

parser.add_argument("--baselight", help="Baselight stuff")
parser.add_argument("--xytech", help="Xytech stuff")
parser.add_argument("--process", help="Process stuff")
parser.add_argument("--output", help="Output stuff")

args = parser.parse_args()
