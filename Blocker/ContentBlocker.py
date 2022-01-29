import re

from PermissonExceptions import FunctionPermission, ImportPermission


class ContentBlocker:

    NOT_ALLOWED_IMPORTS = ['os']
    NOT_ALLOWED_FUNCTIONS = ['exec', 'eval', 'open']

    @classmethod
    def __not_allowed_import_checker(cls, code):
        divide_pattern = r".*[\ ,]+"
        end_pattern = r"(\W+|$)"
        for _import in cls.NOT_ALLOWED_IMPORTS:
            pattern = fr"(?:from{divide_pattern}{re.escape(_import)}{end_pattern})|(?:import{divide_pattern}{re.escape(_import)}{end_pattern})"
            match = re.search(pattern, code)
            if match is not None:
                raise ImportPermission(f'Permission for module {_import} not approved')

    @classmethod
    def __not_allowed_func_checker(cls, code):
        for function in cls.NOT_ALLOWED_FUNCTIONS:
            pattern = fr"{re.escape(function)}\(.*\)"
            match = re.search(pattern, code)
            if match is not None:
                raise FunctionPermission(f'Permission for function {function} not approved')

    @classmethod
    def check_content(cls, code):
        cls.__not_allowed_import_checker(code)
        cls.__not_allowed_func_checker(code)
