import prompt_toolkit
from pygments.token import Token
from pygments.styles.native import NativeStyle
from pygments.lexers.go import GoLexer

from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_pygments
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import print_tokens


from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.filters import IsReturning, IsMultiline
from prompt_toolkit.filters import Condition
from prompt_toolkit.shortcuts import Keys


manager = KeyBindingManager.for_prompt()

@manager.registry.add_binding(Keys.Enter, filter=IsMultiline())
def _(event):
	
	b = event.cli.current_buffer
	if b.document.char_before_cursor == '{':
		b.document = b.document.insert_after('\n    ')
		b.cursor_down()
	else:
		b.document = b.document.insert_after('\n')
		b.cursor_down()

@manager.registry.add_binding(Keys.Tab)
def tab_event(event):
	b = event.cli.current_buffer
	b.document = b.document.insert_after('   ')
	prompt_toolkit.buffer.indent(b, 10, 10)
	
	
  


class InteractiveShell:
  
  _style = style_from_pygments(NativeStyle)
  
  _output_style = style_from_dict({
    Token.String: '#e00000 bold'
  })

  _title_style = style_from_dict({
    Token.String: '#00ff00 bold'
  })

  def __init__(self, file_name):
    self._go_lexer = PygmentsLexer(GoLexer)
    self._file_history = FileHistory(file_name)
    self.true_color = False
    self.multiline = True
    self.mouse_support = True
  
  def render_prompt(self, cli):
    return [
      (Token.String, '#> ')
    ]

  def render_output(self, output_text):
    return [
      (Token.String, '<# '),
      (Token.String, output_text),
      (Token, '\n')
    ]
  
  def render_title(self, text):
    return [
      (Token.String, '#'),
      (Token.String, text),
      (Token, '\n'),
      (Token, '\n'),
    ]

  def continuation_tokens(self, width):
    def get_continuation_tokens(cli, width):
      return [(Token, '.' * width)]
    return get_continuation_tokens

  def input(self, multiline=True):
    result = prompt(get_prompt_tokens=self.render_prompt,
                    lexer=self._go_lexer,
                    style=InteractiveShell._style,
                    true_color=self.true_color,
                    multiline=multiline,
                    get_continuation_tokens=self.continuation_tokens(5),
                    history=self._file_history,
                    key_bindings_registry=manager.registry
										)
    return result

  def print(self, output, title=False):
    if title:
      print_tokens(self.render_title(output), style=InteractiveShell._title_style)
      return
    print_tokens(self.render_output(output), style=InteractiveShell._output_style)