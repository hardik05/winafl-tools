import json

# Enter your twitter keys/secrets as strings in the following fields
winaflconfig = {}
winaflconfig['FUZZ_ITERATIONS'] = "5000"
winaflconfig['COVTYPE'] = "edge"
winaflconfig['TIMEOUT'] = "5000+"
winaflconfig['DYNAMORIO_BIN32_DIR'] = "E:\\Research\\WinAFL_Work\\DynamoRIO-Windows-7.1.0-1\\bin32"
winaflconfig['FUZZ_EXE_NAME'] = "test_gdiplus.exe"
winaflconfig['FUZZ_OFFSET_OR_METHOD'] = "0x1680"
winaflconfig['NARGS'] = "2" #how often script should check for new crashes or hangs, in seconds
winaflconfig['CALL_CONVENTION'] = "stdcall" #how often script should send pingpong DMs to twitter account?
winaflconfig['COVERAGE_MODULES_NAMES'] = ["gdiplus.dll","windowscodecs.dll"]
winaflconfig['CORPUS_INPUT_DIR'] = "InGDI"
winaflconfig['CORPUS_MIN_DIR'] = "inMinGDI"
winaflconfig['OUTPUT_DIR'] = "OutGDI"
winaflconfig['INPUT_TEST_FILE'] = "test"
winaflconfig['NO_OF_CORES'] = "8"
# Save the winaflconfig object to file
with open("gdi_settings.json", "w") as file:
    json.dump(winaflconfig, file)
