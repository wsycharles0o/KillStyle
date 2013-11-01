import killstyle
import ConfigParser
import sys
from defaults import DEFAULT_AUTHOR_NAME

HEADER = 'conf'


def __main__(args):
    cf = ConfigParser.ConfigParser()
    cf.read('killstyle.ini')
    try:
        author = cf.get(HEADER, 'author')
    except ConfigParser.NoOptionError:
        author = ''
    killstyle.AUTHOR_NAME = author if author is not '' else DEFAULT_AUTHOR_NAME

__main__(sys.argv[1:])
print(sys.argv[1:])
#killstyle.AUTHOR_NAME = "NICE AND SLOW"
#killstyle.run(['Sample/damn.java'])
