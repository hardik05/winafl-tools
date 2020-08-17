# winafl-tools
Tools for winafl

what it is?
Running winafl is a hell of task in itself. it invloce a large command line and has lot of options. if you want to run winafl, you need to give proper parameter to dynamorio and as well other parameters, if you want to minimise corpus you need to run winafl-cmin with parameter, if you want to generate coverage, you need to run drrun.exe with some parameters and so on. either people write their own batch file or scripts to do it. so i decided to write a single script for all the task. this script internally uses all the scripts like winafl-cmin.py etc to do its job, its just a wrapper for all the commands and scrips. But this makes running winafl very easy.
NOTE: you need to run this script from your winafl\bin32(64) directory.

There are two tools:
1. generate-config.py - this will generate a json config file for you winafl project. if you want to fuzz GDI then you can create one json config file - gdi_config.json and use winafl-tools.py to do most of your work. if you want to fuzz mdb files, you can generate another json file - mdb_confi.json and so on.
These config file contains nothing but simple parameter you would pass to winafl like indir name, outdir,dynamorio path etc..
this is how a simple config file looks like:

{"FUZZ_ITERATIONS": "5000", "COVTYPE": "edge", "TIMEOUT": "5000+", "DYNAMORIO_BIN32_DIR": "E:\\Research\\WinAFL_Work\\DynamoRIO-Windows-7.1.0-1\\bin32", "FUZZ_EXE_NAME": "test_gdiplus.exe", "FUZZ_OFFSET_OR_METHOD": "0x1680", "NARGS": "2", "CALL_CONVENTION": "stdcall", "COVERAGE_MODULES_NAMES": ["gdiplus.dll", "windowscodecs.dll"], "CORPUS_INPUT_DIR": "InGDI", "CORPUS_MIN_DIR": "inMinGDI", "OUTPUT_DIR": "OutGDI", "INPUT_TEST_FILE": "test", "NO_OF_CORES": "8"}


you just need to open generate-config.py and modify the parameters as per you need and it will generate a json file which will be used by winafl-tools.py

2. winafl-tools.py - this script takes care of all the work from corpus minimization, running winafl in test mode, generating code coverage files, running multiple instances of winafl in Master/Slave fashion, restarting a crashes core etc.
  a. A simple use to run gdi fuzzer with 1 master and 7 slave would be following[after you have generated a gdi_config.json from generate_config.py above]:
    winafl-tools.py --run=run --config=gdi_config.json --core=8
    this will start 1 master and 7 slaves.
  b. generating code coverage files: following command will generate code coverage:
      winafl-utils.py --coverage=True --config=gdi_settings.json
  c. restarting a crashes core: following command will restart a core:
     winafl-utils.py --restartcore=2 --config=gdi_settings.json
  d. resuming winafl session[using input dir as "_"]:  following command will change input dir as "-":
     winafl-utils.py --resume=true --config=gdi_settings.json
  e. if you want to minmise corpus: use following command:
      winafl-utils.py --mincorpus=true --config=gdi_settings.json
  f. if you want to generate a debug file to make sure winafl and dynamorio instrumentation is working correctly:
      winafl-utils.py --debuglog=true --debuginput=test.jpeg --config=gdi_settings.json
      
Hope this helps. pull requests and ideas to make it better are always welcome.
      
