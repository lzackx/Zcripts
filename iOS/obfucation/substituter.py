import os, json, re
import mapper, matcher

class substituter(object):
    
    def __init__(self, options):
        self.sources = options['sources']
        self.verbose = options['verbose']
        self.scan_results_path = './intermediate/result.json'
        self.scan_results = {}
        self.file_types = ['.h', '.m', '.mm', '.pbxproj', '.pch']
        if 'rule' in options:
            self.mapper = mapper.mapper(rule_path=options['rule'])
        else:
            self.mapper = mapper.mapper()
        self.matcher = matcher.matcher()

    def load_scan_results(self):
        with open(self.scan_results_path, 'r') as f:
            self.scan_results = json.load(f)

    def substitute(self):
        assert bool(self.scan_results), 'empty scan results'
        print('=== start substituting ===')
        for p in self.sources:
            self.substitute_files(p)
            self.substitute_classes(p)
        with open(os.path.abspath('./intermediate/relation_files.json'), 'w') as f:
            json.dump(self.mapper.relation_files, f)
        with open(os.path.abspath('./intermediate/relation_classes.json'), 'w') as f:
            json.dump(self.mapper.relation_classes, f)
        print('=== stop substituting ===')

    def filter_file_types(self, path):
        filePaths = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        files = list(filter(lambda fp: os.path.isfile(fp), filePaths))
        if self.verbose == True:     
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
        if self.verbose == True:     
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
            fnp, fns = os.path.splitext(fn)
            file_include_sacan_result = False
            for k in self.scan_results['classes'].keys():
                if k in fn:
                    file_include_sacan_result = True
                    break
            if file_include_sacan_result:
                maped_fn = self.mapper.map_file(fn)
                if fn != maped_fn:
                    p = os.path.split(fp)[0]
                    maped_fp = os.path.join(p, maped_fn)
                    os.rename(fp, maped_fp)
                    print('transfer:\n%s => %s' % (fp, maped_fp))
        # 2. substitute sub directories
        directoryPaths = self.filter_directories(path)
        for d in directoryPaths:
            self.substitute_files(d)


    # classes
    def substitute_classes(self, path):
        print('substitute classes path:\n%s' % path)
        # 1. substitute file
        # 1.1 filter specified file types
        filePaths = self.filter_file_types(path)
        # 1.2 map classes
        for sr in self.scan_results['classes']:
            self.mapper.map_class(sr)
        # 1.3 substitute
        for fp in filePaths:
            content = ''
            with open(fp, 'r') as f:
                content = f.read()
            substituted_content = content
            for srk in self.scan_results['classes'].keys():
                print(srk)
                if srk in self.mapper.relation_classes:
                    print(self.matcher.class_objc_class_pattern(srk))
                    print(self.mapper.relation_classes[srk])
                    substituted_content = re.sub(self.matcher.class_objc_class_pattern(srk), 
                    lambda matched: self.substitute_code(matched = matched, source=srk, target=self.mapper.relation_classes[srk]), 
                    substituted_content)
            with open(fp, 'w') as f:
                f.write(substituted_content)
        # 2. substitute sub directories
        directoryPaths = self.filter_directories(path)
        for d in directoryPaths:
            self.substitute_classes(d)

    def substitute_code(self, matched, source, target):
        match_string = matched.group()
        substituted_string = match_string.replace(source, target)
        if self.verbose:
            print('substitute code:\n\t%s => %s' % (match_string, substituted_string))
        return substituted_string