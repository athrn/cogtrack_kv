
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
    background_color: (.1,.1,1,1)
  IconButton:
    icon: 'go-next'
    background_color: (.1,.1,1,1)
  """

if __name__ == "__main__":
    from buttons import IconButton
    root = Builder.load_string(build)
    run_widget(root)
    


    
