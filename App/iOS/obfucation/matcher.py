import re

class matcher(object):
    
    def __init__(self):
        pass

    # Mapper
    def prefix_pattern(self, prefix):
        pattern = r'^' + prefix
        return pattern
    
    def suffix_pattern(self, suffix):
        pattern = suffix + r'$'
        return pattern

    # Class
    def class_objc_pattern(self):
        # @interface class :
        return r'\@interface{1}[\s]+([\w]+)[\s]*\<?[\w\s\,]*\>?[\s]*[\:]{1}'

    # #  Method
    # def method_objc_pattern(self):
    #     return r''

    # Code
    def class_objc_class_pattern(self, code):
        # _class_
        # @"class"
        # [code xxx]
        # "code+xxx"
        # "code.h"
        # (code)
        # (code*)
        # : code\n
        # <code 
        # <code*
        # code;
        # code,
        # ,code;
        return r'[\s\[\@]*[\s\[\"\(\<\:\,]{1}' + code + r'[\s\"\+\.\(\)\*\n\,\;]{1}'