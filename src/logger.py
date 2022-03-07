import string
from colors import term_colors

class Logger():
    def __init__(self, name) -> None:
        if name is None:
            raise Exception("Invalid Logger name")
        self.name = name
    
    def __log(self: any,level: string, message: string) -> None:
        print(f'[{level}] \t in {self.name}: \t {message}')

    def error(self: any,message: string) -> None:
        self.__log(f'{term_colors.ERROR}Error{term_colors.ENDC}', message)

    def debug(self: any,message: string) -> None:
        self.__log(f'{term_colors.DEBUG}Debug{term_colors.ENDC}', message)
    
    def warn(self: any, message: string) -> None:
        self.__log(f'{term_colors.WARNING}Warn{term_colors.ENDC}', message)
    
    def verbose(self: any, message: string) -> None:
        self.__log(f'{term_colors.VERBOSE}Verbose{term_colors.ENDC}', message)