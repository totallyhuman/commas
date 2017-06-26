#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Creative Name

A language that probably hopefully does something.

Sumant Bhaskaruni
v0.1.0 (basically, don't use it)
"""

import argparse
import collections
import math
import re

commands = {
    '+': lambda stack: stack.push(stack.pop() + stack.pop()),
    '-': lambda stack: stack.push(stack.pop() - stack.pop()),
    '×': lambda stack: stack.push(stack.pop() * stack.pop()),
    '÷': lambda stack: stack.push(stack.pop() / stack.pop()),
    '%': lambda stack: stack.push(stack.pop() % stack.pop()),
    '*': lambda stack: stack.push(stack.pop() ** stack.pop()),
    '√': lambda stack: stack.push(math.sqrt(stack.pop())),
    '␣': lambda stack: print(stack.pop(), end = ''),
    '↓': lambda stack: print(chr(stack.pop()), end = ''),
    '↑': lambda stack: stack.pop(),
    '¬': lambda stack: stack.push(int(not stack.pop())),
    '∧': lambda stack: stack.push(int(stack.pop() and stack.pop())),
    '∨': lambda stack: stack.push(int(stack.pop() or stack.pop()))
}

class UnknownCommand(Exception):
    """An Exception that is raised on an invalid command."""

    def __init__(self, command):
        super(UnknownCommand,
              self).__init__('Unknown command: {}'.format(command))


class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def __len__(self):
        return len(self.items)


def tokenize(code):
    """Splits the code into tokens.

    Positional arguments:
        code (str): the code to be tokenized

    Returns:
        tokens (list): a list of all the tokens in the code
    """
    Token = collections.namedtuple('Token', ['type', 'value'])

    token_specs = [
        ('number', r'-?\d+(\.\d*)?'),
        ('string', r'(?P<q>[\'"])([^\\]|\\[\s\S])*?(?P=q)'),
        ('noop', r'[ \t\n]+'),
        ('command', r'.')
    ]
    token_regex = '|'.join(r'(?P<{}>{})'.format(*i) for i in token_specs)
    tokens = []

    for token in re.finditer(token_regex, code):
        _type = token.lastgroup
        value = token.group(_type)

        if _type == 'noop':
            pass
        elif _type == 'command':
            if value in commands:
                tokens.append(Token(_type, value))
            else:
                raise UnknownCommand(value)
        else:
            tokens.append(Token(_type, value))

    return tokens


def run(code):
    tokens = tokenize(code)
    stack = Stack()

    for token in tokens:
        if token[0] == 'number':
            try:
                stack.push(int(token[1]))
            except ValueError:
                stack.push(float(token[1]))
        elif token[0] == 'string':
            stack.push(token[1][1:-1])
        else:
            commands[token[1]](stack)

    try:
        print(stack.pop())
    except IndexError:
        print()

def main():
    parser = argparse.ArgumentParser(
        description = 'An interpreter for the Creative Name language.')
    parser.add_argument('file', help = 'program read from script file',
                        type = open)

    args = parser.parse_args()
    with args.file as f:
        run(f.read())


if __name__ == '__main__':
    main()
