#!/usr/local/cs/bin/python3
"""                                                                                                                  
shuffles input by outputting a random permutation of input lines                                                     
"""

import random, sys
import argparse

def original(values):
    result = ''
    output = list(values)
    random.shuffle(output)
    for item in output:
        result += item
    return result

def repeat(values):
    result = ''
    while values:
        ele = random.choice(values)
        result += ele
        print(ele, end='')
    return result

def count_lines(num, values):
    result = ""
    output = list(values)
    random.shuffle(output)
    i = 0
    for item in output:
        if i >= num:
            break
        result += item
        i += 1
    return result


def echo(values):
    output = []
    input_list = values
    random.shuffle(input_list)
    for item in input_list:
        output.append(item)
    return output

def in_range(values):
    range_str = str(values)
    split = range_str.split("-")
    if len(split) !=2 :
        raise argparse.ArgumentTypeError("Invalid range format")
    low = int(split[0])
    high = int(split[1])
    input_list = []
    output = []
    if low > high:
        raise argparse.ArgumentTypeError("Invalid range format")
    for i in range(low, high+1):
        input_list.append(i)
    random.shuffle(input_list)
    for item in input_list:
        output.append(str(item))
    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), help = "get input")
    parser.add_argument("-e", "--echo", nargs='*', required=False, default=[], dest="echo", help="input values not read from a file")
    parser.add_argument("-i", "--input-range", action="store", required=False, default=False, dest="range", help="range of values rather than from input file")
    parser.add_argument("-n", "--head-count", type=int, required=False, default=0, dest="count", help = "input at most count number of lines given")
    parser.add_argument("-r", "--repeat", action="store_true", required=False, default=False, dest="repeat", help="repeat values from the input")
    parser.add_argument("-en", nargs='*', default = False, required=False, dest="combine")
    args = parser.parse_args()

    if args.combine:
        if args.combine[0].isdigit():
            args.count = int(args.combine[0])
            args.echo = args.combine[1:]
        else:
            parser.error("Invalid Line Count")
    
    if args.echo and args.range:
        parser.error("Cannot combine -e and -i options.")
        return

    if args.echo and args.count !=0:
        count = 0
        if args.repeat:
            while count < args.count:
                element = random.choice(args.echo)
                print(element)
                count += 1
            return
        for item in echo(args.echo):
            if count >= args.count:
                break
            print(item)
            count += 1
        return
    
    if args.range and args.count != 0:
        count_range = 0
        if args.repeat:
            random_range = in_range(args.range)
            while count_range < args.count:
                print(random.choice(random_range))
                count_range += 1
            return
        for item in in_range(args.range):
            if(count_range >= args.count):
                break
            print(item)
            count_range += 1
        return
    
    if args.range and args.repeat:
        range_str = str(args.range)
        split = range_str.split("-")
        if len(split) != 2:
            raise argparse.ArgumentTypeError("Invalid range format")
        low = int(split[0])
        high = int(split[1])
        list_range = []
        output = []
        if low > high:
            raise argparse.ArgumentTypeError("Invalid range format")
        for i in range(low, high+1):
            list_range.append(i)
        while list_range:
            ele = random.choice(list_range)
            print(ele)
        return

    if args.echo and args.repeat:
        input_list = args.echo
        while input_list:
            ele = random.choice(input_list)
            print(ele)
        return
        

    if args.echo:
        for item in echo(args.echo):
            print(item)
        return
    elif args.range:
        for item in in_range(args.range):
            print(item)
        return
    
    if args.file:
        input_file = args.file
    else:
        input_file = "-"
    
    if input_file != "-":
        lines = input_file.readlines()
    else:
        lines = sys.stdin.readlines()

    if args.repeat and args.count:
        i = args.count
        result_lines = []
        while lines and i > 0:
            ele = random.choice(lines)
            result_lines.append(ele)
            i -= 1
        
        for line in result_lines:
            print(line, end='')
        return

    if args.repeat:
            print(repeat(lines), end='')
            return
    elif args.count != 0:
           print(count_lines(args.count, lines), end='')
           return
    else:
        print(original(lines), end='')
        return
        


if __name__ == "__main__":
    main()
