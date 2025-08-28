import readline

class AutoCompleter:
    def __init__(self, options):
        self.options = sorted(options)
        
    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options 
                               if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

def setup_autocomplete(commands):
    completer = AutoCompleter(commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    readline.set_completer_delims(' \t\n')
