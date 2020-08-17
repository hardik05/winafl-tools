#-------------------------------------------------------------------------------
# Name:       winafl-tools.py
# Purpose:    running winafl and managing it is a really pain.this script helps
#             to overcome this by automating most of the stuff.
#             check readme.txt for complete usage and documentation.
#
# Author:     hardik shah
# Email:      Hardik05@gmail.com
# Created:    03/06/2019
# Copyright:  (c) hardik shah 2019-2020
# twitter:    @hardik05
# Licence:    GNU GPLV3
#-------------------------------------------------------------------------------
import os,sys
import argparse
import json
'''
default options - no need to change unless you really want to try some different values
'''
AFL_FUZZ_EXE = "afl-fuzz.exe"

'''
DO NOT CHANGE ANYTHING BELOW
'''

WINAFL_OPTIONS = ""

# convert unicode chars to byte
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

#get dynamorio path
def getDROptions():
    DRPATH = DYNAMORIO_BIN32_DIR + "\\drrun.exe" + " -c winafl.dll -debug -target_module " + FUZZ_EXE_NAME
    if "0x" in FUZZ_OFFSET_OR_METHOD:
        DRPATH = DRPATH + " -target_offset " + FUZZ_OFFSET_OR_METHOD
    else:
        DRPATH = DRPATH + " -target_method " + FUZZ_OFFSET_OR_METHOD
    DRPATH = DRPATH + " -fuzz_iterations 10" + " -nargs " + NARGS  + " -- " + FUZZ_EXE_NAME + " "
    print (DRPATH)
    return DRPATH

#geerate debug log
def generateDebuglog(filename):
    DRCmd = getDROptions() + filename
    print ("Generating debug log..")
    print (DRCmd)
    os.system("cmd.exe /c start " + DRCmd)


def generateCodeCoverage():
    testcases = []
    for root, dirs, files in os.walk(CORPUS_INPUT_DIR, topdown=False):
        for name in files:
            testcase =  os.path.abspath(os.path.join(root, name))
            testcases.append(testcase)

    for testcase in testcases:
        print ("[*] Running DynamoRIO for testcase: ", testcase)
        cmd = DYNAMORIO_BIN32_DIR + "\\drrun.exe -t drcov -- "+ FUZZ_EXE_NAME + " %s" % testcase
        print (cmd)
        os.system(cmd)


def getAFLFuzzOptions():
    AFL_FUZZ_OPTIONS = "-i " + CORPUS_INPUT_DIR + " -o " + OUTPUT_DIR + " -t " + TIMEOUT + " -D " + DYNAMORIO_BIN32_DIR
    return AFL_FUZZ_OPTIONS

def getWinAFLOptions():
    COVERAGE_MODULE =""
    for name in COVERAGE_MODULES_NAMES:
        COVERAGE_MODULE = COVERAGE_MODULE + "-coverage_module " + name + " "

    WINAFL_OPTIONS = COVERAGE_MODULE + "-target_module " + FUZZ_EXE_NAME
    if "0x" in FUZZ_OFFSET_OR_METHOD:
        WINAFL_OPTIONS = WINAFL_OPTIONS + " -target_offset " + FUZZ_OFFSET_OR_METHOD
    else:
        WINAFL_OPTIONS = WINAFL_OPTIONS + " -target_method " + FUZZ_OFFSET_OR_METHOD
    WINAFL_OPTIONS = WINAFL_OPTIONS +" -fuzz_iterations " + FUZZ_ITERATIONS + " -call_convention " + CALL_CONVENTION + " -nargs " + NARGS + " -covtype " + COVTYPE
    return WINAFL_OPTIONS

def runCore(core):
    #get the options
    WINAFL_OPTIONS = getWinAFLOptions()
    AFL_FUZZ_OPTIONS = getAFLFuzzOptions()

    if(core ==0):
        FINAL_COMMAND_LINE = AFL_FUZZ_EXE + " " + "-M Master " +  AFL_FUZZ_OPTIONS + " -- " + WINAFL_OPTIONS + " -- " + FUZZ_EXE_NAME + " @@"
    else:
        FINAL_COMMAND_LINE = AFL_FUZZ_EXE + " " + "-S Slave" + str(core)+ " " +  AFL_FUZZ_OPTIONS + " -- " + WINAFL_OPTIONS + " -- " + FUZZ_EXE_NAME + " @@"
    print (FINAL_COMMAND_LINE)
    os.system("cmd.exe /c start " + FINAL_COMMAND_LINE)

def runFuzzers():
    print ("Don't forget to enable PaegeHeap on :" + FUZZ_EXE_NAME)
    print ("running cores:", NO_OF_CORES)
    WINAFL_OPTIONS = getWinAFLOptions()
    AFL_FUZZ_OPTIONS = getAFLFuzzOptions()
    i = 0
    if NO_OF_CORES > 1:
        while i< int(NO_OF_CORES) :
            if i == 0:
                i = i + 1
                FINAL_COMMAND_LINE = AFL_FUZZ_EXE + " " + "-M Master "+  AFL_FUZZ_OPTIONS + " -- " + WINAFL_OPTIONS + " -- " + FUZZ_EXE_NAME + " @@"
                print (FINAL_COMMAND_LINE)
                os.system("cmd.exe /c start " + FINAL_COMMAND_LINE)
            else:
                i = i + 1
                FINAL_COMMAND_LINE = AFL_FUZZ_EXE + " " + "-S Slave" + str(i-1)+ " " +  AFL_FUZZ_OPTIONS + " -- " + WINAFL_OPTIONS + " -- " + FUZZ_EXE_NAME + " @@"
                print (FINAL_COMMAND_LINE)
                os.system("cmd.exe /c start " + FINAL_COMMAND_LINE)
    else:
        FINAL_COMMAND_LINE = AFL_FUZZ_EXE + " " + AFL_FUZZ_OPTIONS + " -- " + WINAFL_OPTIONS + " -- " + FUZZ_EXE_NAME + " @@"
        print (FINAL_COMMAND_LINE)
        os.system("cmd.exe /c start " + FINAL_COMMAND_LINE)

def readConfigfile(filename):
    global FUZZ_ITERATIONS
    global COVTYPE
    global TIMEOUT
    global DYNAMORIO_BIN32_DIR
    global FUZZ_EXE_NAME
    global FUZZ_OFFSET_OR_METHOD
    global NARGS
    global CALL_CONVENTION
    global COVERAGE_MODULES_NAMES
    global CORPUS_INPUT_DIR
    global CORPUS_MIN_DIR
    global OUTPUT_DIR
    global INPUT_TEST_FILE
    global NO_OF_CORES

    # Load credentials from json file
    with open(filename, "r") as file:

        winaflconfig = json.load(file)

        FUZZ_ITERATIONS = byteify(winaflconfig['FUZZ_ITERATIONS'])
        COVTYPE = byteify(winaflconfig['COVTYPE'])
        TIMEOUT = byteify(winaflconfig['TIMEOUT'])
        DYNAMORIO_BIN32_DIR = byteify(winaflconfig['DYNAMORIO_BIN32_DIR'])
        FUZZ_EXE_NAME = byteify(winaflconfig['FUZZ_EXE_NAME'])
        FUZZ_OFFSET_OR_METHOD = byteify(winaflconfig['FUZZ_OFFSET_OR_METHOD'])
        NARGS = byteify(winaflconfig['NARGS'])
        CALL_CONVENTION = byteify(winaflconfig['CALL_CONVENTION'])
        COVERAGE_MODULES_NAMES = byteify(winaflconfig['COVERAGE_MODULES_NAMES'])
        CORPUS_INPUT_DIR = byteify(winaflconfig['CORPUS_INPUT_DIR'])
        CORPUS_MIN_DIR = byteify(winaflconfig['CORPUS_MIN_DIR'])
        OUTPUT_DIR = byteify(winaflconfig['OUTPUT_DIR'])
        INPUT_TEST_FILE = byteify(winaflconfig['INPUT_TEST_FILE'])
        NO_OF_CORES = int(byteify(winaflconfig['NO_OF_CORES']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debuglog", help="Runs AFL in debug mode and check if everything is working as expected.")
    parser.add_argument("--debuginput", help="input file for which you want to generate debug log.")
    parser.add_argument("--core", help="number of cores")
    parser.add_argument("--mincorpus", help="minimize corpus", default=False)
    parser.add_argument("--restartcore", help="restart core if it crashed")
    parser.add_argument("--resume", help="resume session instead of starting from scratch, input dir will be - ",default=False)
    parser.add_argument("--coverage", help="generate code coverage files from input dir",default=False)
    parser.add_argument("--run", help="run the fuzzer")
    parser.add_argument("--config", help="config file",default="config.json")

    args = parser.parse_args()

    if(args.config):
        configfile = args.config
        if(os.path.isfile(configfile)):
            readConfigfile(configfile)
        else:
            print ("config file not specified or not found.. exiting.")
            parser.print_help(sys.stderr)
            exit(0)


    if(args.coverage):
        print ("generating code coverage files...")
        generateCodeCoverage()
        exit(0)

    if(args.resume):
        global CORPUS_INPUT_DIR
        CORPUS_INPUT_DIR = "-" #this will set input dir to "-" to resume the session instead of restarting it again..

    #print(args.AFLDebug)
    if(args.mincorpus):
        print ("Min corpus Mode..")
        MIN_COMMAND = "..\winafl-cmin.py -i " + CORPUS_INPUT_DIR + " -o " + CORPUS_MIN_DIR + " -D " + DYNAMORIO_BIN32_DIR + " -covtype " + COVTYPE +  " -call_convention " + CALL_CONVENTION
        COVERAGE_MODULE =""
        for name in COVERAGE_MODULES_NAMES:
            COVERAGE_MODULE = COVERAGE_MODULE + " -coverage_module " + name
        MIN_COMMAND = MIN_COMMAND + COVERAGE_MODULE + " -target_module " + FUZZ_EXE_NAME
        if "0x" in FUZZ_OFFSET_OR_METHOD:
            MIN_COMMAND = MIN_COMMAND + " -target_offset " + FUZZ_OFFSET_OR_METHOD
        else:
            MIN_COMMAND = MIN_COMMAND + " -target_method " + FUZZ_OFFSET_OR_METHOD

        MIN_COMMAND = MIN_COMMAND + " --skip-dry-run -nargs " + NARGS + " -- " + FUZZ_EXE_NAME + " @@"
        print (MIN_COMMAND)
        os.system("cmd.exe /c start " + MIN_COMMAND)
        exit(0)

    if(args.restartcore):
        core = int(args.restartcore)
        runCore(core)
        exit(0)

    global NO_OF_CORES
    if(args.core): #this will override default configuration
        NO_OF_CORES = int(args.core)

    if(args.debuglog):
        generateDebuglog(args.debuginput)
        exit(0)

    #this will run the fuzzers based on the configurations
    if(args.run):
        runFuzzers()
        exit(0)


if __name__ == '__main__':
    main()
