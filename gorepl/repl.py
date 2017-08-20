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
    
    def generate_code(self):
        _code = (
            'package main\n'
            %s
            'function main() {'
            %s
            '}'
        ) % (self._state.import_node.code(), self._state.main_statement_node.code())
    
        