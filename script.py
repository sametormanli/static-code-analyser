import sys
import os
import re


def convert(string):
    if string[-10] != '/':
        string = string[:-9] + string[-9:]
    else:
        string = string[:-9] + '/' + string[-9:]
    string.replace('/', os.sep)
    return string


def conv2(string):
    if string[-10] != '\\':
        string = string[:-9] + '\\' + string[-9:]
    return string


def fun(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            if len(line) > 79:
                print(f'line {i + 1}: s001 too long')


def s_001(line, no, path):
    if len(line) > 79:
        print(f'{conv2(convert(path))}: Line {no}: S001 Too long')


def s_002(line, no, path):
    counter = 0
    for char in line:
        if char != ' ':
            break
        counter += 1
    if counter % 4 != 0:
        print(f'{conv2(convert(path))}: Line {no}: S002 Indentation is not a multiple of four')


def s_003(line, no, path):
    if ';' in line:
        idx = line.index(';')
        former = line[:idx]
        latter = line[idx + 1:]
        if '#' not in former and not ('\'' in latter):
            print(f'{conv2(convert(path))}: Line {no}: S003 Unnecessary semicolon')
        else:
            s_003(line[idx + 1:], no, path)


def s_004(line, no, path):
    if '#' in line and not line.startswith('#'):
        line_split = line.split('#')
        if not line_split[0].endswith('  '):
            print(f'{conv2(convert(path))}: Line {no}: S004 At least two spaces before inline comment required')


def s_005(line, no, path):
    if '#' in line:
        line_split = line.split('#')
        if 'todo' in line_split[1].lower():
            print(f'{conv2(convert(path))}: Line {no}: S005 TODO found')


def s_007(line, no, path):
    if 'def' in line:
        if not re.match(r' \S', line.split('def')[1]):
            print(f'{conv2(convert(path))}: Line {no}: S007 Too many spaces after construction_name (def or class)')
            return True
    if 'class' in line:
        if not re.match(r' \S', line.split('class')[1]):
            print(f'{conv2(convert(path))}: Line {no}: S007 Too many spaces after construction_name (def or class)')
            return True


def s_008(line, no, path):
    if 'class' in line:
        if not re.match(r' [A-Z]\w*', line.split('class')[1]):
            print(f'{conv2(convert(path))}: Line {no}: S008 Class name class_name should use CamelCase')


def s_009(line, no, path):
    if 'def' in line:
        if not re.match(r' [a-z_]+', line.split('def')[1]):
            print(f'{conv2(convert(path))}: Line {no}: S009 Function name function_name should use snake_case')


def s_010(line, no, path):
    if 'def' in line:
        start = line.find('(')
        end = line.find(')')
        if end > start + 1:
            arguments = line[start+1:end].split(', ')
            for argument in arguments:
                if '=' in argument:
                    argument = argument.split('=')[0]
                if not re.match(r'[a-z_]+', argument):
                    print(f'{conv2(convert(path))}: Line {no}: S010 Argument name arg_name should be snake_case')


def s_011(line, no, path):
    if re.match(r' {4}.+ = .+', line):
        var = line.split(' = ')[0]
        if not re.match(r'[a-z._]+', var.lstrip()):
            print(f'{conv2(convert(path))}: Line {no}: S011 Variable var_name should be snake_case')


def s_012(line, no, path):
    if 'def' in line and '=' in line:
        arguments = line.split('=')
        arguments.pop(0)
        for arg in arguments:
            if arg[:2] == '[]':
                print(f'{conv2(convert(path))}: Line {no}: S012 Default argument value is mutable')


def check(filename, path):
    with open(filename) as f:
        counter = 0
        for i, line in enumerate(f):
            idx = i + 1
            # print(idx, line)
            s_001(line, idx, path)
            s_002(line, idx, path)
            s_003(line, idx, path)
            s_004(line, idx, path)
            s_005(line, idx, path)
            if line != '\n':
                if counter > 2:
                    print(f'{conv2(convert(path))}: Line {idx}: S006 Line More than two blank lines used before this line')
                counter = 0
            else:
                counter += 1
            res = s_007(line, idx, path)
            if not res:
                s_008(line, idx, path)
                s_009(line, idx, path)
            s_010(line, idx, path)
            s_011(line, idx, path)
            s_012(line, idx, path)


def main(directory):
    if os.path.isfile(directory):
        check(directory, directory)
    else:
        for dire in os.scandir(directory):
            if dire.is_file():
                check(dire, directory + dire.name)
            else:
                main(directory + dire.name)


main(sys.argv[1])