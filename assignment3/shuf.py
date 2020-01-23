#!/usr/bin/env python3

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class randline:
    def __init__(self, input_arr, argument):
        self.lines = input_arr
        self.argu = argument

    def chosenlines(self, rpt, numlines ,input_range):
        #rpt is a bool, T/F
        #numlines contains numlines to display OR a boolean False
        #input_range contains a string OR a boolean False
        #function global variables
        val = self.lines #val is a list with our elements to be shuffled at this point
        output_arr=[]
        if input_range != False:
            input_range = True

        if numlines == "":
            numlines = False

            
        #print("rpt:",rpt)
        #print("input_range:",input_range)
        #print("numlines:",numlines)
        #9 CASES
        #-i = 0, -n = 0, -r = 1
        if input_range == False:
            if numlines != False:
                if rpt == True:
                    #-i = 0, -n = 1, -r - 1: takes n input, choose for n times
                    for i in range(numlines):
                        outLineIndex=random.choice(range(len(self.lines)))
                        output_arr.append(self.lines[outLineIndex])
                elif rpt == False:
                    #-i = 0, -n = 1, -r = 0 takes n input, sample
                    output_arr=random.sample(self.lines,numlines)
            elif numlines == False:
                if rpt == True:
                    #-i = 0, -n= 0, -r = 1 #takes all input, choose forever
                    while True:
                        outLineIndex=random.choice(range(len(self.lines)))
                        sys.stdout.write(self.lines[outLineIndex])
                if rpt == False:
                    #-i = 0, -n = 0, -r = 0
                    #print(self.argu)
                    if self.argu != "":
                        output_arr=random.sample(self.lines,len(self.lines))
                    else:
                        print("shuf: invalid input", file=sys.stderr)
                        exit(2)
                
        elif input_range != False:
            if numlines != False:
                if rpt == True:
                    #-i = 1, -n = 1, -r = 1: takes input, chooses n times
                    for i in range(numlines):
                        outLineIndex=random.choice(range(len(self.lines)))
                        output_arr.append(self.lines[outLineIndex])
                elif rpt == False:
                    #-i = 1, -n = 1, -r = 0: takes input, samples n times
                    output_arr=random.sample(self.lines,numlines)
            elif numlines == False:
                if rpt == True:
                    #-i = 1, -n = 0 , -r = 1: takes input, chooses forever
                    while True:
                        outLineIndex=random.choice(range(len(self.lines)))
                        sys.stdout.write(self.lines[outLineIndex])
                elif rpt == False:
                    #-i = 1, -n = 0, -r = 0: takes input samples all.
                    output_arr=random.sample(self.lines,len(self.lines))               
        return output_arr
    
def main():
    version_msg = "%prog 1.0"
    usage_msg = """shuf [OPTION]... [FILE] shuf -e [OPTION]... [ARG]...shuf -i LO-HI [OPTION]..."""

    parser = OptionParser(version=version_msg,usage=usage_msg)
    #-n option
    parser.add_option("-n", "--head-count", action="store", dest="numlines",default=False, help="output at most COUNT lines", metavar="COUNT" )
    #-i option
    parser.add_option("-i", "--input-range", action="store", type="string", default=False, dest="input_range", help="treat each number LO through HI as an input line")
    #-r option
    parser.add_option("-r", "--repeat", action="store_true", dest="rpt", default=False, help="output lines can be repeated (default false)")
    options, args = parser.parse_args(sys.argv[1:])

    input_to_randline=""
    input_file=""
    #-i input handling
    if options.input_range != False:
        ir=options.input_range
        arr=[]
        if ir == "-":
            print("shuf: invalid input", file=sys.stderr)
            exit(2)
        arr=ir.split('-',1) #splits input_range string into two
        try:
            first = int(arr[0]) #if this fails, first is not a digit
            second = int(arr[1]) #if this fails, second is not a digit
        except:
            print("invalid input {0}".format(arr[1]))
            exit(2)

        #at this point, first and second are valid digits
        if second < 0 or first < 0:
            print("invalid input {0}-{1}".format(arr[0],arr[1]))
            exit(2)
        #at this point, first and second are valid and positive
        if first - second > 1:
            print("invalid input {0}-{1}".format(arr[0],arr[1]))
            exit(2)
        if first - second == 1:
            exit(2)
        if len(arr) <= 1:
            print("invalid input")
            exit(2)
#        try:
#            if len(arr) <= 1:
#                print("invalid input")
#                exit(2)
#            if len(arr) > 2:
#                print("invalid input {0}-{1}".format(arr[-2],arr[-1]))
#                exit(2)
#            for index in range(arr):
#                if type(int(arr[index])) != int:
#                    print("shuf: invalid input", file=sys.stderr)
#                    exit(2)
#            if int(arr[0]) < 0 or int(arr[1]) < 0:
#                print("invalid input {0}-{1}".format(arr[0],arr[1]))
#            if int(arr[0])-int(arr[1]) > 1:
#                print("invalid input {0}-{1}".format(arr[0],arr[1]))
#        except Exception as e:
#            print("shuf: invalid input",e, file=sys.stderr)
#        else:
#            if int(arr[0])-int(arr[1]) == 1:
#                exit(2)
#            input_to_randline=list(range(int(arr[0]),int(arr[1])+1))
        #print(input_to_randline)
        temp_in=list(range(int(arr[0]),int(arr[1])+1))
        for i in range(len(temp_in)):
            temp_in[i] = str(temp_in[i])+"\n"
        input_to_randline=temp_in



    #handling no arguments or one argument -> Stdin
    elif options.input_range == False:
        if len(args) == 1 and args[0] == "-":
            if sys.stdin.isatty() == True:
                print("Error inputting from standard in bc nothing there")
            else:
                input_file = sys.stdin
                input_to_randline = input_file.readlines()
            #something in standard in
        elif len(args) == 0:
            if sys.stdin.isatty() == True:
                print("Error inputting from standard in bc nothing there")
            else:
                input_file = sys.stdin
                input_to_randline=input_file.readlines()
        elif len(args) != 1: #refers to number of arguments passed in for a specific option.
            parser.error("wrong number of operands")

        else:
            input_file = args[0]
            try:
                f = open(input_file, 'r')
                input_to_randline = f.readlines()
                f.close()
            except (IsADirectoryError,FileNotFoundError) as e:
                print("shuf: ",e,file=sys.stderr)
                exit(2)

    #figure out wrong number of operands here?

    #-n input handling
    numlines=""
    temp_numlines = options.numlines
    if temp_numlines != False:
        #numlines has been specified by user
        try:
            numlines = int(options.numlines) #try to convert it to an int. Won't work if a alpha char!            
        except:
            parser.error("invalid NUMLINES: {0}".format(options.numlines)) #-n param passed in isn't a digit
            exit(2)
        else:
            #executes if no exceptions
            #only throw exception when negative numlines is passed in.
            if numlines < 0:
                parser.error("invalid NUMLINES: {0}".format(options.numlines))
            if numlines > len(input_to_randline):
                numlines = len(input_to_randline)
    #At this point, numlines is either False, or a correct input.
    
    
                
    #-r input handling

    
    rpt = bool(options.rpt)
    
    #print(rpt)
    #print(len(args))
    if options.input_range != False and len(args) >= 1:
        parser.error("wrong number of operands")
        
    #--help input handling
    
    #Outputting our random lines
    argument=""
    try:
        #check if something is in our arguments
        if options.input_range == False and args[0] != "":
            argument = args[0]
            input_file = args[0]
            try:
                f = open(input_file, 'r')
                input_to_randline = f.readlines()
                f.close()
            except (IsADirectoryError,FileNotFoundError) as e:
                print("shuf: ",e,file=sys.stderr)
                exit(2)
    except:
        parser.error("Invalid Input: No arguments passed in")
    try:
        generator = randline(input_to_randline, argument)
        outputLines = generator.chosenlines(rpt, numlines,options.input_range)
        for line in outputLines:
            sys.stdout.write(line)

    except IOError as err:
        errno, strerror = err.args
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
