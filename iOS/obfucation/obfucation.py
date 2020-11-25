import sys, os, getopt, json

import scaner


def handleOptions(argv):
    try:
      (opts, args) = getopt.getopt(args=argv, shortopts="hs:t:")
    except getopt.GetoptError:
        print('invalid args')
        print ('use -h to get help')
        sys.exit(2)

    options = {}
    for opt, arg in opts:
        if opt == '-h':
            print('Usages:')
            print ('    -s <source directories>     source directories, could be divided by ","')
            print ('    -t <output file>            target file path')
            sys.exit()
        elif opt in ("-s"):
            # split paths with ","
            paths = arg.split(',')
            # translate paths to absolute paths
            options['sources'] = list(map(lambda p: os.path.abspath(os.path.normpath(p)), paths))
        elif opt in ("-t"):
            # translate paths to absolute paths
            options['target'] = os.path.abspath(os.path.normpath(arg))
    return options


def main(argv):
    options = handleOptions(argv)
    print('obfucation info:')
    print(json.dumps(options))
    # scan all files of codes
    scanner = scaner.scaner(sources=options['sources'], target=options['target'])
    scanner.scan()
    scanner.save_resultes()
    # scanner.clear_resultes()


if __name__ == "__main__":
    main(sys.argv[1:])

