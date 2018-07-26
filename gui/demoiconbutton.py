
from kivy.lang import Builder
from demo import run_widget

build = """
GridLayout:
  cols: 10
  rows: 10
  # orientation: 'vertical'
  Button:
    text: 'Dummy'
  IconButton:
    size_hint: None, None
    height: '48dp'
    background_color: (.1,.1,1,1)
  IconButton:
    size_hint: None, None
    icon: 'go-next'
    height: '48dp'
    background_color: (.1,.1,1,1)
  """

if __name__ == "__main__":
    Builder.load_file('base.kv')
    root = Builder.load_string(build)
    run_widget(root)
    


    
