import sys, os, getopt, json, shutil

import scaner
import substituter

def usage():
    print('Usages:')
    print ('    -s <source directories>     source directories, could be divided by ","')
    print ('    -c                          clear intermediate files')
    print ('    -v                          print verbose')

def handleOptions(argv):
    try:
      (opts, args) = getopt.getopt(args=argv, shortopts="hs:cv")
    except getopt.GetoptError:
        print('invalid args')
        print ('use -h to get help')
        sys.exit(2)

    options = {
        'verbose': False
    }
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-s"):
            # split paths with ","
            paths = arg.split(',')
            # translate paths to absolute paths
            options['sources'] = list(map(lambda p: os.path.abspath(p), paths))
        elif opt in ("-c"):
            # clear intermediate files
            intermediate_path = os.path.join(os.getcwd(), './intermediate')
            if os.path.exists(intermediate_path): 
                shutil.rmtree(intermediate_path)
        elif opt in ("-v"):
            # clear intermediate files
            options['verbose'] = True
    
    if 'sources' in options.keys():
        pass
    else:
        print('invalid args')
        print ('use -h to get help')
        sys.exit(2)

    return options

def create_intermediate_directory():
    intermediate_path = os.path.join(os.getcwd(), './intermediate')
    if os.path.exists(intermediate_path) == False:
        os.mkdir(intermediate_path)

def main(argv):
    options = handleOptions(argv)
    create_intermediate_directory()
    if options['verbose'] == True:
        print('obfucation info:')
        print(json.dumps(options))
    # scan all files of codes
    scanner = scaner.scaner(sources=options['sources'], verbose=options['verbose'])
    scanner.scan()
    scanner.save_resultes()
    # scanner.clear_resultes()
    
    # replace all files of codes
    substitution = substituter.substituter(sources=options['sources'], verbose=options['verbose'])
    substitution.load_scan_results()
    substitution.substitute()

    if options['verbose'] == True:
        print('done !')

if __name__ == "__main__":
    main(sys.argv[1:])

