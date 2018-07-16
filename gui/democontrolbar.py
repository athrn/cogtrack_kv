from kivy.lang import Builder
from demo import run_widget

build = """
BoxLayout:
  orientation: 'vertical'
  ControlBar:
    size_hint: (1.0, 0.1)
    SquareDemoButton:
    SquareDemoButton:
    DemoButton:
    SquareDemoButton:
    SquareDemoButton:
  BoxLayout:
    DemoButton:
"""

if __name__ == "__main__":
    Builder.load_file('demo.kv')
    Builder.load_file('mainview.kv')
    root = Builder.load_string(build)
    run_widget(root)
    
