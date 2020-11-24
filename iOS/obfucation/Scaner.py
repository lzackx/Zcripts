import os, json, re


class Scaner(object):

    def __init__(self, sources = [], target = './result.txt'):
        self.resultes = []
        self.sources = sources
        self.target = os.path.abspath(os.path.normpath(target))
        self.fileTypes = ['.h','.m','.mm','.swift']

    def add_result(self, target):
        self.resultes.append(target)

    def clear_resultes(self):
        self.resultes.clear()
        os.remove(self.target)
        pass

    def save_resultes(self):
        with open(file=self.target, mode='w') as f:
            print('scan results: %s' % self.resultes)
            json.dump(self.resultes, f)          

    def filter_directories(self, path):
        # get directories' names of path 
        directories = list(filter(lambda d: os.path.isdir(d), os.listdir(path)))
        # 
        directoryPaths = list(map(lambda d: os.path.join(path, d), directories))
        return directoryPaths

    def match(self, pattern, content):
        cp = re.compile(pattern=pattern)
        r = cp.findall(str=content)
        return r

    def filter_file_types(self, path):
        files = list(filter(lambda f: os.path.isfile(f), os.listdir(path)))
        print('files: %s' % files)
        tfs = list(files)
        for f in tfs:
            ext = os.path.splitext(f)
            if len(ext) == 2:
                if ext[1] in self.fileTypes:
                    continue
                else:
                    files.remove(f)
            else:
                files.remove(f)
        filePaths = list(map(lambda f: os.path.join(path, f), files))
        return filePaths

    def scan(self):
        assert len(self.sources) != 0, 'empty source paths'
        print('=== start scanning ===')
        for p in self.sources:
            self.scan_file(p)
        print('=== stop scanning ===')
    
    def scan_file(self, path):
        print('scanning path: %s' % path)
        # 1. scan file
        # 1.1 filter specified file types
        filePaths = self.filter_file_types(path=path);
        print('filted files: %s' % filePaths)
        # 1.2 match
        for fp in filePaths:
            with open(fp) as f:
                content = f.read()
                matches = self.match(pattern=r'', content=content)
        # 1.3 add to result
                for m in matches:
                    self.add_result(m)

        # # 2. scan sub directories
        directoryPaths = self.filter_directories(path)
        for d in directoryPaths:
            self.scan_file(d)
