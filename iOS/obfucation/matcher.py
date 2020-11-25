import re

class matcher(object):
    
    def __init__(self):
        pass

    # Class
    def class_objc_pattern(self):
        return r'\@interface{1}[\s]+([\w]+)[\s]+[\:]{1}'

    #  Method
    def method_objc_pattern(self):
        return r''
