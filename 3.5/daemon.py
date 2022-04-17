from pathlib import *
from subprocess import *
from sys import *
from time import *

command = f'cls && python main.py {argv[1]}'
observables = [Path('main.py'), Path(argv[1])]

last_mtimes = {x: None for x in observables}
while True:
    mtimes = {x: x.stat().st_mtime for x in observables}
    for it in observables:
        if last_mtimes[it] != mtimes[it]:
            run(command.format(it), shell=True)
    last_mtimes = mtimes
    sleep(1)
