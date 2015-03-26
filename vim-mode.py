# gedit3-vim-mode: Vim-style keyboard navigation plugin for gedit3.
# Copyright 2015 Nicholas Parkanyi, licensed under GPLv3 (see 'gpl.txt')
from gi.repository import GObject, Gedit, Gdk

class VimMode(GObject.Object, Gedit.ViewActivatable):
  __gtype_name__ = "VimMode"

  view = GObject.property(type=Gedit.View)

  def __init__(self):
    GObject.Object.__init__(self)

  def do_activate(self):
    self.block = True
    self.id = self.view.connect("key-press-event", self.process_keystroke)
    self.update_cursor_iterator()
    self.line_offset = self.it.get_line_offset()

  def do_deactivate(self):
    self.view.disconnect(self.id)
    
  def do_update_state(self):
    pass
    
  def process_keystroke(self, widget, event):
    if event.keyval == 0xff1b:
      self.block = True
    #modifier combinations
    elif event.state & Gdk.ModifierType.MODIFIER_MASK != 0 \
         and event.state & Gdk.ModifierType.SHIFT_MASK == 0:
      return False
    #  'i' insert mode
    elif event.keyval == 0x069 and self.block:
      self.block = False
      return True
    elif self.block:
      self.update_cursor_iterator()
      # 'j' cursor down
      if event.keyval == 0x06a:
        self.cursor_down()
      # 'k' cursor up
      elif event.keyval == 0x06b:
        self.cursor_up()
      # 'l' cursor right
      elif event.keyval == 0x06c:
        self.cursor_right()
      # 'h' cursor left
      elif event.keyval == 0x068:
        self.cursor_left()
      # 'e' cursor to next end of word
      elif event.keyval == 0x065:
        self.cursor_right_word_end()
      # 'w' cursor to next start of word
      elif event.keyval == 0x077:
        self.cursor_right_word_start()
      # 'b' cursor to previous start of word
      elif event.keyval == 0x062:
        self.cursor_left_word_start()
      # '$' cursor to end of line
      elif event.keyval == 0x024:
        self.cursor_end_line()
      # '0' cursor to start of line
      elif event.keyval == 0x030:
        self.cursor_start_line()
        
      self.buf.place_cursor(self.it)
    return self.block

  def update_cursor_iterator(self):
    self.buf = self.view.get_buffer()
    self.it = self.buf.get_start_iter()
    self.it.set_offset(self.buf.props.cursor_position)
    
  def cursor_down(self):
    if not self.it.ends_line():
      self.line_offset = self.it.get_line_offset()
    self.it.forward_line()
    self.view.scroll_to_iter(self.it, 0.0, False, 0.0, 1.0)
    self.cursor_maintain_line_offset()
    
  def cursor_up(self):
    if not self.it.ends_line():
      self.line_offset = self.it.get_line_offset()
    self.it.backward_line()
    self.view.scroll_to_iter(self.it, 0.0, False, 0.0, 0.0)
    self.cursor_maintain_line_offset()
    
  def cursor_right(self):
    if not self.it.ends_line():
      self.it.forward_char()
    
  def cursor_left(self):
    if not self.it.starts_line():
      self.it.backward_char()
    
  def cursor_end_line(self):
    while not self.it.ends_line():
      self.it.forward_char()
  
  def cursor_start_line(self):
    while not self.it.starts_line():
      self.it.backward_char()

  def cursor_maintain_line_offset(self):
    for i in range(0, self.line_offset):
      if self.it.ends_line():
        break
      self.it.forward_char()
      
  def cursor_right_word_end(self):
    self.it.forward_word_end()
    
  def cursor_right_word_start(self):
    if not self.it.ends_word():
      self.it.forward_word_end()
    while not self.it.starts_word():
      self.it.forward_char()
      
  def cursor_left_word_start(self):
    self.it.backward_word_start()
