"""
This file contains a handler for standardized logging.
Casey Johnson, Spring 2020
"""

class LoggingError(Exception): pass
class NoMessageProvidedError(Exception): pass

class LoggingHandler:
    def __init__(self, log_file, echo=False):
        """
        log_file:   relative path to log output file.
        echo:       used to display logs in the terminal in addition to logging in a file (default: False).
        """
        self.log_file = log_file
        self.echo = echo
        with open(log_file, 'w') as f: pass

    def log(self, text):
        """
        text:       string data to be logged.
        """
        if not text:
            raise NoMessageProvidedError()
        with open(self.log_file, 'a') as f:
            f.write(text)
            f.write('\n')
        if self.echo:
            print(text)
