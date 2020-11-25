import re

class matcher(object):
    
    def __init__(self):
        pass

    # Class
    def class_objc_pattern(self):
        return r'\@interface{1}[\s]+([\w]+)[\s]+[\:]{1}'

    # #  Method
    # def method_objc_pattern(self):
    #     return r''

    # Mapper
    def prefix_pattern(self, prefix):
        pattern = r'^' + prefix
        return pattern
    
    def suffix_pattern(self, suffix):
        pattern = suffix + r'$'
        return pattern