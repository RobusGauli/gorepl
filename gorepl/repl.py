import os
import collections 
import itertools
import functools
import subprocess
import re
import sys
import random

#i will start from the first no
class rdict(dict):
    
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val

class ImportNode:
    def __init__(self):
        self.imports = set()
    
    def add_import(self, import_statement):
        self.imports.add(import_statement)
    
    def code(self):
        #this should return the valid code
        return '\n'.join(import_line for import_line in self.imports)

class MainStatementNode:
    
    def __init__(self):
        self.main_statements = []
    
    def add_main_statements(self, statement):
        self.main_statements.append(statement)
    
    def code(self):
        return '\n'.join(st_line for st_line in self.main_statements)
    

class Repl:
    '''This is the main instance that will represent the state tree for the interactive REPL'''

    def __init__(self):
        self._state = rdict()
        #initiate import tree
        self._state.import_node = ImportNode()
        self._state.main_statement_node = MainStatementNode()
        self._state.statement_node = None
        #a stack to keep track of all the single line that is input by the user
        self.code_stack = collections.deque()
        self._file_name = 'test.go'

        #a current_running statem, which has a unknown return code, 
        self._current_state = rdict()
        self._current_state.import_node = ImportNode()
        self._current_state.main_statement_node = MainStatementNode()
        self._current_state.statement_node = None
    
    
    def generate_code(self):
        return (
            'package main\n'
            '%s\n'
            'func main() {'
            '%s\n'
            '%s\n'
            '}'
        ) % ('\n'.join(self._state.import_node.imports.union(self._current_state.import_node.imports)),
             self._state.main_statement_node.code(),
             self._current_state.main_statement_node.code()
             )

    
    def write_to_file(self):
        _file = open(self._file_name, mode='w+')
        _file.write(self.generate_code())
        _file.close()
    
    def _merge_state(self):
        '''when the return code is 0'''

        self._state.import_node.imports.update(self._current_state.import_node.imports)
        self._state.main_statement_node.main_statements.extend(self._current_state.main_statement_node.main_statements)
    
    def run(self):
        #runt the code for the given file
        return_code = subprocess.call('go run test.go'.split(), stdout=sys.stdin, stderr=sys.stderr)
        if return_code == 0:
            #that means we can union the both  state and _current_state
            self._merge_state()
        else:
            print('return code ', return_code, 'bad')
            self._current_state.import_node.imports.clear()
            self._current_state.main_statement_node.main_statements.clear()
