import getopt
import sys

# read commandline arguments
arg_list = sys.argv[1:]

# prepare valid parameters
short_options = 'f:t:w:'
long_options = ['from=', 'to=', 'wait=']

# parse argument list
try:
    args, values = getopt.getopt(
        arg_list, short_options, long_options)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

# initialize parameters
codes_from = ''
code_to = ''
wait_seconds = ''

# evaluate given options
for arg, value in args:
    if arg in ('-f', '--from'):
        codes_from = value.split(',')
    elif arg in ('-t', '--to'):
        code_to = value
    elif arg in ('-w', '--wait'):
        wait_seconds = value
