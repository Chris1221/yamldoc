import yamldoc
import argparse

def cli():
    ''' Example of taking inputs for megazord bin'''
    parser = argparse.ArgumentParser(prog='YAML Documentation Engine')
    parser.add_argument('file',  help='YAML file.')
    parser.add_argument('-c', '--char', default = "#'", help='Metadata character prefix.')
    parser.add_argument('-d', '--debug', action = 'store_true', help='Show debug information.')
    parser.add_argument('-s', '--schema', default = None, help = "(Optional) Schema file describing variable types.")

    args = parser.parse_args()

    yamldoc.main(args.file, args.char, args.debug, args.schema)
