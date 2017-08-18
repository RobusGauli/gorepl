import os
import collections 
import itertools
import functools
import subprocess
import re
import sys
import random

_exit_quotes = [
  'Life was fair until you came in',
  'Python ain\'t just snake in the town'
]

_go_cover = ['package main\n',
 '\n',
 'import  "fmt"\n',
 '\n',
 'func main() {\n',
 '}\n']


def process_input(buffer):
  _go_cover = ['package main\n',
    '\n',
    'import  "fmt"\n',
    '\n',
    'func main() {\n'
  ]
  _buffer = list(buffer)
  #add \n for each recv_line
  _buffer = (line + '\n' for line in _buffer)
  _go_cover.extend(_buffer)
  _go_cover.append('}\n')
  return _go_cover


class ImportNode:
  '''Represents the import statement in the golang'''

  _skeleton = 'import (\n%s\n)'

  def __init__(self):
    self.packages = set()
  
  def add_package(self, line):
    '''we assume that the string that it has have a "import somepackage"'''
    if not len(line.split()) == 2:
      raise ValueError('Bad import statement.')
     
    self.packages.add(line.split()[1].strip().rstrip(';'))
  
  def code(self):
    #this method returns the code import statement with all the packages
    _code = self._skeleton % ('\n'.join(p for p in self.packages))
    return _code
  
  def __repr__(self):
    return 'Import : {}'.format(', '.join(package for package in self.packages))



class StatementNode:

  def __init__(self):
    self._statements = []
  
  def add_statement(self, statement):
    self._statements.append(statement)
  
  def code(self) -> str:
    _code = '\n'.join(s for s in self._statements)
    return _code

  

def execute_go(import_node, statement_node):
  #create a temp fileclear
  _import_code = import_node.code()
  _statement_code = statement_node.code()
  _go_cover = ['package main\n',
    _import_code,
    '\n',
    'func main() {\n',
    _statement_code,
    '\n}'
  ]

  _file = open('test.go', mode='w+')
  _file.write(''.join(line for line in _go_cover))
  _file.flush()
  subprocess.call('go run test.go'.split())



def main():
  _buffer = []
  #initialize import node
  import_node = ImportNode()
  #initiate statement node
  statement_node = StatementNode()

  while True:
    
    try:
      
      recv_line = input('>>> ')
      
      #now check the received input
      #check to see if the command is from the 'clear ls'
      if recv_line.strip().lower() == 'clear':
        subprocess.call('clear')
        continue
      if not recv_line.strip():
        continue
      if recv_line.strip().lower() in 'exit quit \q quit() exit();'.split():
        raise KeyboardInterrupt
      if not recv_line.endswith(';;'):
        #if line starst with import statement then add the line to import node
        if recv_line.startswith('import') and len(recv_line.split()) == 2:
          import_node.add_package(recv_line)
        else:
          #this must be the statement node
          statement_node.add_statement(recv_line)
        
      else:
        #is it ends , then we need to process the input
        execute_go(import_node, statement_node)
        

    except KeyboardInterrupt:
      sys.exit(random.choice(_exit_quotes))

if __name__ == '__main__':
  if os.environ.get('a'):
    main()
