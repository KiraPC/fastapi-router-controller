import os
import importlib

class ControllerLoader():
    '''
        The ControllerLoader class.
    '''
    @staticmethod
    def load(directory, package):
        '''
            It is an utility to load automatically all the python module presents on a given directory
        '''
        for module in os.listdir(directory):
            sub_dir = directory + '/' + module
            if os.path.isdir(sub_dir):
                ControllerLoader.load(sub_dir, '{}.{}'.format(package, module))
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            else:
                module_import_name = '{}.{}'.format(package, module[:-3])
                importlib.import_module(module_import_name)
