

# TODO: MainView also has some logic like switch from win 1 -> win 2

from tools import PrettyProperties    

class MockGameController: pass

class MainController(object):

    def get_game_names():
        return ['2-Back', 'Trail making', 'Morning batch']
                
    def get_game_controller(self, name):
        return MockGameController(name)

    

    
