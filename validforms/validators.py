import re

class Validator(object):
    """
    Base class for all validations
    """
    def __call__(self, subject):
        return self._validate(subject)

class RegExValidator(Validator):
    """ Subclass to validate arbitrary regular expressions
    """
    def __init__(self, re):
        self.re = re

    def _validate(self, text):
        """ Method used for form validation by django """
        return re.match(self.re, text) != None

    def client_side(self):
        """ Returns javascript validator for client """
        return """function (x){ return (""+x).match(/^%s$/) != null; }""" % (self.re)

def get_client_side_validator(v):
    """ Return simple javascript functions to correspond builtin
    validators """
    if v.__class__.__name__ == 'MaxLengthValidator':
        return """function (x){ return (""+x).length <= %d; }""" % (v.limit_value)
