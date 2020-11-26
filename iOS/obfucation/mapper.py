import re, json
import matcher

class mapper(object):
    
    def __init__(self, rule_path='./rule.json'):
        self.relation_files = {}
        self.relation_classes = {}
        self.rule_path = rule_path
        self.rules = {}
        self.matcher = matcher.matcher()
        self.load_rules()
        pass

    def load_rules(self): 
        with open(self.rule_path, 'r') as f:
            self.rules = json.load(f)

    def map_file(self, name):
        assert bool(self.rules), 'no rules'
        for k in self.rules.keys():
            pattern = self.matcher.prefix_pattern(k)
            if re.match(pattern, name) != None:
                print('name: %s matched pattern: %s' %(name,pattern))
                maped_name = name.replace(k, self.rules[k])
                self.relation_files[name] = maped_name
                return maped_name
        return name
    
    def map_class(self, name):
        assert bool(self.rules), 'no rules'
        for k in self.rules.keys():
            pattern = self.matcher.prefix_pattern(k)
            if re.match(pattern, name) != None:
                print('name: %s matched pattern: %s' %(name,pattern))
                maped_name = name.replace(k, self.rules[k])
                self.relation_classes[name] = maped_name
                return maped_name
        return name
