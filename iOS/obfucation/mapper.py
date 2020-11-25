import re, json
import matcher

class mapper(object):
    
    def __init__(self, rules_path='./rules.json'):
        self.relation = {}
        self.rules_path = rules_path
        self.rules = {}
        self.matcher = matcher.matcher()
        self.load_rules()
        pass

    def load_rules(self): 
        with open(self.rules_path, 'r') as f:
            self.rules = json.load(f)

    def map(self, name):
        assert bool(self.rules), 'no rules'
        for k in self.rules.keys():
            pattern = self.matcher.prefix_pattern(k)
            if re.match(pattern, name) != None:
                print('name: %s matched pattern: %s' %(name,pattern))
                maped_name = name.replace(k, self.rules[k])
                self.relation[name] = maped_name
                return maped_name
        return name
