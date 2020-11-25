import os, json, re
import mapper

class substituter(object):
    
    def __init__(self, sources = [], scan_results_path = './result.json'):
        self.sources = sources
        self.scan_results_path = scan_results_path
        self.scan_results = {}
        self.file_types = ['.h', '.m', '.mm']
        self.mapper = mapper.mapper()

    def load_scan_results(self):
        with open(self.scan_results_path, 'r') as f:
            self.scan_results = json.load(f)

    def substitute(self):
        assert bool(self.scan_results), 'empty scan results'
        print('=== start substituting ===')
        for p in self.sources:
            self.substitute_files(p)
            self.substitute_codes(p)
        print('=== stop substituting ===')

    def filter_file_types(self, path):
        filePaths = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        files = list(filter(lambda fp: os.path.isfile(fp), filePaths))
        print('files:\n\t%s' % files)
        tfs = list(files)
        for f in tfs:
            ext = os.path.splitext(f)
            if len(ext) == 2:
                if ext[1] in self.file_types:
                    continue
                else:
                    files.remove(f)
            else:
                files.remove(f)
        filePaths = list(map(lambda f: os.path.join(path, f), files))
        print('filtered files:\n\t%s' % filePaths)
        return filePaths

    def filter_directories(self, path):
        directoryPaths = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        directories = list(filter(lambda d: os.path.isdir(d), directoryPaths))
        directoryPaths = list(map(lambda d: os.path.join(path, d), directories))
        return directoryPaths

    # files
    def substitute_files(self, path):
        print('substitute files path:\n%s' % path)
        # 1. substitute file
        # 1.1 filter specified file types
        filePaths = self.filter_file_types(path)
        # 1.2 substitute
        for fp in filePaths:
            fn = os.path.basename(fp)
            maped_fn = self.mapper.map(fn)
            if fn != maped_fn:
                p = os.path.split(fp)[0]
                maped_fp = os.path.join(p, maped_fn)
                os.rename(fp, maped_fp)
                print('transfer:\n%s => %s' % (fp, maped_fp))
        # 2. substitute sub directories
        directoryPaths = self.filter_directories(path)
        for d in directoryPaths:
            self.substitute_files(d)


    # codes
    def substitute_codes(self, path):
        pass
