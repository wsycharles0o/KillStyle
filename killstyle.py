import subprocess
import sys
import os
 
from defaults import DEFAULT_JAVADOC, DEFAULT_PARAMDOC, DEFAULT_RETURNDOC, DEFAULT_AUTHOR_NAME

author = DEFAULT_AUTHOR_NAME
args = lambda s: s.strip().split(":")
arg1 = lambda err: int(args(err)[1])
arg2 = lambda err: int(args(err)[2])
get_line = lambda s, n: s.split("\n")[n - 1]
get_line_num = lambda s,: len(s.split("\n"))
write_line = lambda s, n, l: "".join(map(lambda l: l + "\n", s.split("\n")[:n - 1] + [l] + s.split("\n")[n:]))[:-1]
add_new_line = lambda s, n, l: "".join(map(lambda l: l + "\n", s.split("\n")[:n - 1] + [l] + s.split("\n")[n - 1:]))[:-1]
change_line = lambda s, n, f: write_line(s, n, f(get_line(s, n)))
delete_char_at = lambda s, ln, cn: change_line(s, ln, lambda l: l[:cn - 1] + l[cn:])
find_comment_end_up = lambda s, ln: find_comment_end(s, ln - 1) if get_line(s, ln) is "" else (ln, get_line(s, ln).find("*/"))
find_comment_end_down = lambda s, ln: find_comment_end(s, ln + 1) if ln <= get_line_num(s) and get_line(s, ln).find("*/") is -1 else (ln, get_line(s, ln).find("*/"))
line_is_in_comment = lambda s, ln: False if ln <= 0 or get_line(s, ln).find("*/") is not -1 else (True if get_line(s, ln).find("/**") is not -1 else line_is_in_comment(s, ln -1))
find_comment_end = lambda s, ln: find_comment_end_down(s, ln) if line_is_in_comment(s, ln) else find_comment_end_up(s, ln)

add_new_line_at_end = lambda src: src + "\n"
add_author_tag = lambda src, err: add_new_line(src, arg1(err), "/** @author " + AUTHOR_NAME + " */")
add_javadoc = lambda src, err: add_new_line(src, arg1(err), "/** " + DEFAULT_JAVADOC + "*/")
add_paramdoc = lambda src, err: change_line(src, find_comment_end(src, arg1(err) - 1)[0], lambda l: l.rstrip().rstrip("*/").rstrip() + "\n * @param " + args(err)[3][26:-2] + " " + DEFAULT_PARAMDOC + " */") if find_comment_end(src, arg1(err) - 1)[1] is not -1 else add_new_line(src, arg1(err), "/** @param " + args(err)[3][26:-2] + " " + DEFAULT_PARAMDOC + " */")
add_returndoc = lambda src, err: change_line(src, find_comment_end(src, arg1(err) - 1)[0], lambda l: l.rstrip().rstrip("*/").rstrip() + "\n * @return " + DEFAULT_RETURNDOC + " */") if find_comment_end(src, arg1(err) - 1)[1] is not -1 else add_new_line(src, arg1(err), "/** @return " + DEFAULT_RETURNDOC + " */")
add_space = lambda src, err: change_line(src, arg1(err), lambda l: l[:arg2(err) - 1] + " " + l[arg2(err) - 1:])
delete_unknown_tag = lambda src, err: delete_char_at(src, arg1(err), arg2(err))
delete_trailing_spaces = lambda src, err: change_line(src, arg1(err), lambda l: l.rstrip())
improve_comment_style = lambda src, err: change_line(src, arg1(err), lambda l: l[:arg2(err) - 1] + "/*" + l[arg2(err) + 1:] + "*/")
improve_indent = lambda src, err: change_line(src, arg1(err), lambda l: " " * int(err.split(",")[1]) + l.lstrip())
break_line = lambda src, err: change_line(src, arg1(err), lambda l: l[:len(l) - l[::-1].find(" ") - 1] + "\n" + l[len(l) - l[::-1].find(" ") - 1:])


def fix(err, src):
    if err.find("File does not end with a newline.") is not -1:
        src = add_new_line_at_end(src)
    if err.find("Unknown tag") is not -1:
        src = delete_unknown_tag(src, err)
    if err.find("Type Javadoc comment is missing an @author tag.") is not -1:
        src = add_author_tag(src, err)
    if err.find("Line has trailing spaces.") is not -1:
        src = delete_trailing_spaces(src, err)
    if err.find("'//'-style comments are not allowed.") is not -1:
        src = improve_comment_style(src, err)
    if err.find("Missing a Javadoc comment.") is not -1:
        src = add_javadoc(src, err)
    if err.find("Expected @param tag for") is not -1:
        src = add_paramdoc(src, err)
    if err.find("Expected an @return tag.") is not -1:
        src = add_returndoc(src, err)
    if err.find("is not followed by whitespace.") is not -1:
        src = add_space(src, err)
    if err.find("is not preceded with whitespace.") is not -1:
        src = add_space(src, err)
    if err.find("Line is longer than 80 characters") is not -1:
        src = break_line(src, err)
    if err.find("should be on a new line.") is not -1:
        src = break_line(src, err)
    if err.find("not at correct indentation") is not -1:
        src = improve_indent(src, err)
    return src

def help_page():
    print("Please use import first argument as java file name.")
    sys.exit();

def fixfile(javafile):
    #javafile = args[0]
    assert isinstance(javafile,str),    "Java file name invalid!"
    #try:
    #    os.remove("./run.bat")
    #except Exception:
    #    #FIX ME
    #try:
    #    os.remove("./res.tmp")
    #except Exception:
        #FIX ME
    subprocess.call("@echo off\n@del /f /s run.bat", shell = True)
    subprocess.call("@echo off\n@del /f /s *.tmp", shell = True)
    subprocess.call("@echo off > run.bat", shell = True)
    f_run = open("run.bat", "w")
    f_run.write("@echo off\n@java -cp ucb-checkstyle.jar ucb.checkstyle.Main ")
    f_run.write(javafile)
    f_run.write(" > res.tmp")
    f_run.close()
    subprocess.call("@run.bat", shell=True)
    f_res = open("res.tmp", "r")
    res = f_res.read()
    f_res.close()
    lines = res.split("\n")
    subprocess.call("cls", shell=True)
    f_source = open(javafile, "r")
    source = f_source.read()
    f_source.close()
    for i in range(len(lines)):
        source = fix(lines[len(lines) - i - 1], source)
    f_source = open(javafile, "w")
    f_source.write(source)
    f_source.close()

# run(sys.argv[1:] if len(sys.argv) >= 2 else help_page())
