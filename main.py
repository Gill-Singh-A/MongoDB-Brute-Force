#! /usr/bine/env python3

from datetime import date
from optparse import OptionParser
from colorama import Fore, Back, Style
from time import strftime, localtime, time

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

if __name__ == "__main__":
    arguments = get_arguments(('-s', "--server", "server", "Target MongoDB Server (seperated by ',')"),
                              ('-u', "--users", "users", "Target Users (seperated by ',') or File containing List of Users"),
                              ('-P', "--password", "password", "Passwords (seperated by ',') or File containing List of Passwords"),
                              ('-c', "--credentials", "credentials", "Name of File containing Credentials in format ({user}:{password})"),
                              ('-w', "--write", "write", "CSV File to Dump Successful Logins (default=current data and time)"))
    if not arguments.server:
        display('-', f"Please specify {Back.YELLOW}Target Server{Back.RESET}")
        exit(0)
    if not arguments.credentials:
        if not arguments.users:
            display('-', f"Please specify {Back.YELLOW}Target Users{Back.RESET}")
            exit(0)
        else:
            try:
                with open(arguments.users, 'r') as file:
                    arguments.users = [user for user in file.read().split('\n') if user != '']
            except FileNotFoundError:
                arguments.users = arguments.users.split(',')
            except:
                display('-', f"Error while Reading File {Back.YELLOW}{arguments.users}{Back.RESET}")
                exit(0)
            display(':', f"Users Loaded = {Back.MAGENTA}{len(arguments.users)}{Back.RESET}")
        if not arguments.password:
            display('-', f"Please specify {Back.YELLOW}Passwords{Back.RESET}")
            exit(0)
        else:
            try:
                with open(arguments.password, 'r') as file:
                    arguments.password = [password for password in file.read().split('\n') if password != '']
            except FileNotFoundError:
                arguments.password = arguments.password.split(',')
            except:
                display('-', f"Error while Reading File {Back.YELLOW}{arguments.password}{Back.RESET}")
                exit(0)
            display(':', f"Passwords Loaded = {Back.MAGENTA}{len(arguments.password)}{Back.RESET}")
        arguments.credentials = []
        for user in arguments.users:
            for password in arguments.password:
                arguments.credentials.append([user, password])
    else:
        try:
            with open(arguments.credentials, 'r') as file:
                arguments.credentials = [[credential.split(':')[0], ':'.join(credential.split(':')[1:])] for credential in file.read().split('\n') if len(credential.split(':')) > 1]
        except:
            display('-', f"Error while Reading File {Back.YELLOW}{arguments.credentials}{Back.RESET}")
            exit(0)
    if not arguments.write:
        arguments.write = f"{date.today()} {strftime('%H_%M_%S', localtime())}.csv"