import os, json, re, functools
import matcher


class scaner(object):

    def __init__(self, options):
        self.resultes = {
            'classes': {},
            'methods': [],
            }
        self.sources = options['sources']
        self.verbose = options['verbose']
        self.target = os.path.abspath('./intermediate/result.json')
        self.class_file_types = ['.h']
        self.matcher = matcher.matcher()
    
    # results
    def clear_resultes(self):
        self.resultes.clear()
        os.remove(self.target)

    def show_resultes(self):
        print('scan results:\n%s' % json.dumps(self.resultes))

    def save_resultes(self):
        if os.path.exists(self.target):
            return
        with open(file=self.target, mode='w') as f:
            json.dump(self.resultes, f)

    # classes
    def add_classes(self, classes, path):
        if len(classes) > 0:
            cs = list(map(lambda c: {c: path}, classes))
            for c in cs:
                self.resultes['classes'].update(c)


    def clear_classes(self):
        self.resultes['classes'] = {}

    def show_classes(self):
        print('scan classes:\n%s' % json.dumps(self.resultes['classes']))

    # methods
    def add_methods(self, methods):
        if len(methods) > 0:
            self.resultes['methods'].extend(methods)

    def clear_methods(self):
        self.resultes['methods'] = []

    def show_methods(self):
        print('scan methods:\n%s' % json.dumps(self.resultes['methods']))


    # scan
    def filter_directories(self, path):
        directoryPaths = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        directories = list(filter(lambda d: os.path.isdir(d), directoryPaths))
        directoryPaths = list(map(lambda d: os.path.join(path, d), directories))
        return directoryPaths

    def filter_file_types(self, path):
        filePaths = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        files = list(filter(lambda fp: os.path.isfile(fp), filePaths))
        if self.verbose == True:      
            print('files:\n\t%s' % files)
        tfs = list(files)
        for f in tfs:
            ext = os.path.splitext(f)
            if len(ext) == 2:
                if ext[1] in self.class_file_types:
                    continue
                else:
                    files.remove(f)
            else:
                files.remove(f)
        filePaths = list(map(lambda f: os.path.join(path, f), files))
        if self.verbose == True:     
            print('filted files:\n\t%s' % filePaths)
        return filePaths

    def match(self, pattern, content):
        if self.verbose == True:     
            print('match pattern: %s' % pattern)
        cp = re.compile(pattern=pattern)
        r = cp.findall(string=content)
        if self.verbose == True:     
            print('matched: %s' % r)
        return r
    
    def scan(self):
        if os.path.exists(self.target):
            return
        assert len(self.sources) != 0, 'empty source paths'
        print('=== start scanning ===')
        for p in self.sources:
            print(p)
            self.scan_file(p)
        print('=== stop scanning ===')
        # self.show_resultes()
    
    def scan_file(self, path):
        print('scanning path:\n%s' % path)
        # 1. scan file
        # 1.1 filter specified file types
        filePaths = self.filter_file_types(path=path);
        # 1.2 match
        for fp in filePaths:
            if self.verbose == True:     
                print('file:\n%s' % fp)
            with open(fp) as f:
                content = f.read()
                # 1.2.1 match classes
                classes = self.match(pattern=self.matcher.class_objc_pattern(), content=content)
                # 1.2.2 add classes
                self.add_classes(classes, fp)
                # # 1.2.3 match methods
                # methods = self.match(pattern=self.matcher.method_objc_pattern(), content=content)
                # # 1.2.4 add methods
                # self.add_methods(methods)
        # # 2. scan sub directories
        directoryPaths = self.filter_directories(path)
        for d in directoryPaths:
            self.scan_file(d)
