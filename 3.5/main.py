import argparse
import colorama
import contextlib
import io
import re
import sys

from transpiler import *

colorama.init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs='?', type=argparse.FileType('r', encoding='utf-8'), default=sys.stdin)
args = parser.parse_args()
original = args.input.readlines()
original = ''.join(original)
transpiled = transpile(original)
transpiled = '\n'.join(filter(lambda x: x and not x.isspace(), transpiled.splitlines()))

original = original.splitlines()
transpiled = transpiled.splitlines()
for i, it in enumerate(original):
    if i >= len(transpiled) or it.isspace() and not transpiled[i].isspace() or not it and transpiled[i]:
        transpiled.insert(i, it)
width = max(len(it) for it in original)
original = '\n'.join(original)
transpiled = '\n'.join(transpiled)

for line, original_and_transpiled in enumerate(zip(original.splitlines(), transpiled.splitlines())):
    for i, it in enumerate(original_and_transpiled):
        its_unescaped_len = len(it)
        def implw(s):
            s = s.group()
            if s in keywords.values() or s in keywords:
                return colorama.Fore.YELLOW + s + colorama.Fore.RESET
            return s
        it = re.sub(r"'(.*?)'", lambda x: colorama.Fore.LIGHTRED_EX + f"'{x.group(1)}'" + colorama.Fore.RESET, it)
        it = re.sub(r'\b\w+\b', implw, it)
        it = re.sub(r'\b\d+\b', lambda x: colorama.Fore.LIGHTYELLOW_EX + x.group() + colorama.Fore.RESET, it)
        it = re.sub('(?<=    )    ', colorama.Fore.LIGHTBLACK_EX + '│···' + colorama.Fore.RESET, it)
        it = re.sub('    ', colorama.Fore.LIGHTBLACK_EX + '····' + colorama.Fore.RESET, it)
        print(colorama.Fore.LIGHTBLACK_EX + '{:>3}'.format(line + 1) + colorama.Fore.RESET, it + ' ' * (width + 10 - its_unescaped_len) * (i == 0), end='')
        if i:
            print()

output = io.StringIO()
with contextlib.redirect_stdout(output):
    exec(transpiled)
print()
for it in output.getvalue().splitlines():
    print(colorama.Fore.BLUE + '>' + colorama.Fore.LIGHTBLUE_EX + '>' + colorama.Fore.LIGHTCYAN_EX + '>', it)