import killstyle
import configparser
import sys

"""
To create a new switch: 
    (assuming the name of the switch is "sw")
    1. Create a new SW_ARG and NO_SW_ARG (Optional) under
            "command-line arguments (without --)"
       and add it to read_args.args under
            "accepted command-line arguments as full name. (without --)"
    2. (Optional) Create a short hand in read_args.arg_alternatives
       The above two will let the program recognizes and reads the argument, the
       first place where the switch is looked up.
    3. Create a new SW_CONF under
            "configure file options"
       and add it to read_conf_file.confs with the default value, '0' or '1'
       (in case it is not found in the configuration file)
       This will let the program to read configurations of the switch, and, if the 
       option is not found, what is the default value of the switch.
    4. Under function apply_settings, add these code
            def apply_sw(boolean): killstyle.SW = boolean
            apply_switch(SW_ARG, NO_SW_ARG, SW_CONF, apply_sw)
       Or, if NO_SW_ARG is not defined in Step 1, replace it with None.
       Here, killstyle.SW is the boolean value in killstyle that you want to
       control.
       This will really notify killstyle.py to do the switch.
    5. (Optional) Update the help message.
    6. (Optional) Update verbose message. (Search killstyle.VERBOSE throughout
       the file)
    See fix-javadoc and verbose as examples.
To create a string definition: (Like author name): //FIXME
"""

def __main__(args):
    conf_settings = read_conf_file()
    arg_settings = read_args(args)
    apply_settings(conf_settings, arg_settings)
    file_names = arg_settings[FILE_ARG]
    if type(file_names) is not list:
        file_names = [file_names]
    for file_name in file_names:
        if killstyle.VERBOSE:
            print("Fixing: "+file_name)
        killstyle.fix_file(file_name)

def read_conf_file():
    """ Read configuration file from cf. If no option found, its default
    value applys. Return a dictionary. """
    cf = configparser.ConfigParser()
    cf.read(CONF_FILE_NAME)
    def get_conf(cf, name, default):
        try:
            attr = cf.get(read_conf_file.HEADER, name)
        except configparser.NoOptionError:
            attr = ''
        if attr is '':
            attr = default
        return attr
    result = {}
    for name, default in read_conf_file.confs.items():
        result[name] = get_conf(cf, name, default)
    return result
    
def read_args(args):
    def parse_arg_list(lst):
        if not lst: return None # if lst is empty
        nonlocal result
        if lst[0] in read_args.arg_alternatives:
            lst[0] = read_args.arg_alternatives[lst[0]]
        if lst[0] not in read_args.args:
            help_page(None, lst[0])
        result[lst[0]] = None if len(lst) == 1 else lst[1] if len(lst) == 2 else lst[1:]
    result = {}
    l = list()
    flag = False
    for arg in args:
        if arg[:2] == '--':
            parse_arg_list(l)
            l = [arg[2:]] # [1:] to eleiminate '--'
            flag = True
        elif arg[0] == '-':
            parse_arg_list(l)
            l = [arg[1:]] # [1:] to eleiminate '-'
            flag = True
        else:
            if flag: l.append(arg)
            else: help_page(None, arg)
    parse_arg_list(l)
    return result

def apply_settings(conf_settings, arg_settings):
    """
    Apply settings to the module killstyle.py
    conf_settings, arg_settings: dictionaries. Values are either None (does not need additional
    stuff), a string (require one extra stuff), or a list of string (require
    many extra stuff)
    """
    def apply_switch(true_arg, false_arg, conf, apply_fn):
        if true_arg in arg_settings:
            if false_arg in arg_settings: # contradiction
                help_page(None, true_arg+" & "+false_arg)
            apply_fn(True)
        elif false_arg in arg_settings:
            apply_fn(False)
        else:
            apply_fn(bool(eval(conf_settings[conf])))
            
    if HELP_ARG in arg_settings:
        help_page()
    if FILE_ARG not in arg_settings or arg_settings[FILE_ARG] is None:
        help_page(FILE_ARG)
    if AUTHOR_ARG in arg_settings:
        if arg_settings[AUTHOR_ARG] is not None:
            killstyle.AUTHOR_NAME = arg_settings[AUTHOR_ARG]
        else:
            help_page(AUTHOR_ARG)
    else:
        killstyle.AUTHOR_NAME = conf_settings[AUTHOR_CONF]
        
    def apply_javadoc(boolean): killstyle.FIX_JAVADOC = boolean
    apply_switch(FIX_JAVADOC_ARG, NO_FIX_JAVADOC_ARG, FIX_JAVADOC_CONF, apply_javadoc)
    
    def apply_fix_return(boolean): killstyle.FIX_RETURN = boolean
    apply_switch(FIX_RETURN_ARG, NO_FIX_RETURN_ARG, FIX_RETURN_CONF, apply_fix_return)
    
    def apply_fix_param(boolean): killstyle.FIX_PARAM = boolean
    apply_switch(FIX_PARAM_ARG, NO_FIX_PARAM_ARG, FIX_PARAM_CONF, apply_fix_param)
    
    def apply_verbose(boolean): killstyle.VERBOSE = boolean
    apply_switch(VERBOSE_ARG, None, VERBOSE_CONF, apply_verbose)
    
    if killstyle.VERBOSE:
        print('Read configurations: {0}'.format(conf_settings))
        print('Read arguments: {0}'.format(arg_settings))
        print('Author name: {0}'.format(killstyle.AUTHOR_NAME))
        print('Enable javadoc fix: {0}'.format(killstyle.JAVADOC))
        print('Enable @return fix: {0}'.format(killstyle.FIX_RETURN))
        print('Enable @param fix: {0}'.format(killstyle.FIX_PARAM))
        print('===================================================')

def help_page(missing = None, unexpected = None):
    """ Print help message and exits the program immediately. """
    if missing is not None:
        print('Error: Missing argument for --' + missing + '\n')
    elif unexpected is not None:
        print('Error: Unexpected command: ' + unexpected + '\n')
    print(help_page.help_message)
    sys.exit();

#Please nicely put the following at the end of the file, just before __main__().

# configuration file name
CONF_FILE_NAME = 'killstyle.ini'
# configure file section header
read_conf_file.HEADER = 'conf'
# configure file options
AUTHOR_CONF = 'author'
VERBOSE_CONF = 'verbose'
FIX_JAVADOC_CONF = 'fixjavadoc'
FIX_RETURN_CONF = 'fixreturntag'
FIX_PARAM_CONF = 'fixparamtag'

# things to read from the configure file and program default settings.
#key: option name in ini file; value: default value if option is not found
read_conf_file.confs = {
    AUTHOR_CONF: 'cs61b',
    FIX_JAVADOC_CONF: '1',
    FIX_RETURN_CONF: '1',
    FIX_PARAM_CONF: '1',
    VERBOSE_CONF: '0'
    } 

# command-line arguments (without --)
FILE_ARG = 'file'
HELP_ARG = 'help'
AUTHOR_ARG = 'author'
FIX_JAVADOC_ARG = 'fix-javadoc'
NO_FIX_JAVADOC_ARG = 'no-fix-javadoc'
FIX_RETURN_ARG = 'fix-return-tag'
NO_FIX_RETURN_ARG = 'no-fix-return-tag'
FIX_PARAM_ARG = 'fix-param-tag'
NO_FIX_PARAM_ARG = 'no-fix-param-tag'
VERBOSE_ARG = 'verbose'
# accepted command-line arguments as full name. (without --)
read_args.args = {FILE_ARG,HELP_ARG,AUTHOR_ARG, VERBOSE_ARG, 
    FIX_JAVADOC_ARG, NO_FIX_JAVADOC_ARG, 
    FIX_RETURN_ARG, NO_FIX_RETURN_ARG,
    FIX_PARAM_ARG, NO_FIX_PARAM_ARG
    }
# accepted short hands for command-line arguments
read_args.arg_alternatives = {
    'a':AUTHOR_ARG, 'f':FILE_ARG, 'h':HELP_ARG, 'v':VERBOSE_ARG,
    'jd': FIX_JAVADOC_ARG, 'njd': NO_FIX_JAVADOC_ARG, 
    'r': FIX_RETURN_ARG, 'nr': NO_FIX_RETURN_ARG,
    'p': FIX_PARAM_ARG, 'np': NO_FIX_PARAM_ARG
    }

# help message    
help_page.help_message = \
    """Usage: 
    python3 run.py [-h]
    python3 run.py -f file1.java [file2.java [...]]
                   [-v]
                   [-a author_name]
                   [-jd | -njd]
                   [-r  | -nr ]
                   [-p  | -np ]
    -h, --help:         Ignores all aguments and print this message
    [no arguments]:     Ignores all aguments and print this message
    -v, --verbose:      Print verbose info
    -f, --file:         Try to fix specified files
    -a, --author:       overrides the .ini settings and set the author tag to
                        be author_name
    -jd,
    --fix-javadoc:      Apply missing javadoc fix
    -njd,
    --no-fix-javadoc:   Do not apply missing javadoc fix
    -r,
    --fix-return-tag:   Apply missing @return tag fix
    -nr,
    --no-fix-return-tag:Do not apply missing @return tag fix
    -p,
    --fix-param-tag:    Apply missing @return tag fix
    -np,
    --no-fix-param-tag: Do not apply missing @param tag fix

    Order of precedence of settings:
        program default settings < """ + CONF_FILE_NAME + """ < command-line arguments
    """


# program starts here.
__main__(sys.argv[1:])





#killstyle.AUTHOR_NAME = "NICE AND SLOW"
#killstyle.run(['Sample/damn.java'])
