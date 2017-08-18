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

def execute_go(go_code):
  #create a temp file
  _file = open('test.go', mode='w+')
  _file.write(''.join(line for line in go_code))
  _file.flush()
  subprocess.call('go run test.go'.split())



def main():
  _buffer = []
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
      if not recv_line.endswith(';'):
        _buffer.append(recv_line)
        
      else:
        #is it ends , then we need to process the input
        _buffer.append(recv_line)
        go_code = process_input(_buffer)
        output = execute_go(go_code) 
        _buffer = []

    except KeyboardInterrupt:
      sys.exit(random.choice(_exit_quotes))
if __name__ == '__main__':
  main()