#!/usr/bin/env python
"""
outline_to_dot.py
Author: Matt Hancock

Convert markdown-style outlines to dot language.
"""

def _get_indent_level(line, indent):
    """
    Get indentation level of string, line, based on string, indent.
    """
    i = 0
    while line.startswith(indent*i):
        i+=1
    return i-1

def outline_to_dot(input, indent=' '*4, tree=False):
    """
    outline_to_dot converts a file where a tree-like hierarchy is specified
    by indentation to dot language.

    input: str
        string to be converted to .dot language.
    indent: str
        specify the indentation marker used. default is 4 spaces, but
        any string could be used ('\\t' for instance).
    tree: bool
        Default False. If True, a strict tree-like hierarchy is kept.
        This means duplicate node names are allowed. See examples below.

    Example input:
        # This is a comment; blank lines get eaten.

        main
            topic one
                subtopic one
            topic two
                subtopic one
                subtopic two
    Example output:
        digraph G {
            "main" -> "topic one";
            "topic one" -> "subtopic one";
            "main" -> "topic two";
            "topic two" -> "subtopic one";
            "topic two" -> "subtopic two";
        }
    """
    # So quotes are interpreted are part of the name:
    input = input.replace('\'','\\\'').replace('\"','\\\"')
    lines = input.split('\n')

    # remove comments, blank lines
    lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    lt = len(tab)

    output = 'digraph G {\n'
    parent_stack = []
    ilbase = _get_indent_level(lines[0], tab)
    ilprev = ilbase # initialize
    count = 0

    for line in lines:
        il = _get_indent_level(line, tab)
        if il < ilbase:
            raise Exception('Indentation level began at %d, but current line is at level %d'%(ilbase,il))
        elif il > ilprev+1:
            raise Exception('Indentation level skipped. %s has no parent.' % line[lt*il:])
        else:
            stack_element = line[lt*il:] if not tree else (count, line[lt*il:])
            count += 1

            if il == ilprev+1:
                parent_stack.append(stack_element)
            elif il == ilprev:
                if parent_stack: parent_stack.pop()
                parent_stack.append(stack_element)
            else: # il < ilprev
                for _ in range(ilprev - il): parent_stack.pop()
                if parent_stack: parent_stack.pop()
                parent_stack.append(stack_element)

            if not tree:
                output += '    \"%s\";\n' % parent_stack[-1]
            else:
                output += '    %d[label=\"%s\"];\n' % (parent_stack[-1][0], parent_stack[-1][1])
            if il is not ilbase:
                if not tree:
                    output += '    \"%s\" -> \"%s\";\n' % (parent_stack[-2], parent_stack[-1])
                else:
                    output += '    %d -> %d;\n' % (parent_stack[-2][0], parent_stack[-1][0])


        ilprev = il
    output += '}'

    return output

def usage():
    return \
    """
    outline_to_dot.py:

        Convert a simple indented outline markup to the dot language.

    Usage:

        outline_to_dot.py [options] file

    Options:
    
        -h, --help
            Print this usage summary.
        -i STRING, --indent=STRING
            Specify indentation marker. The usual markers, spaces or 
            tab characters, must be wrapped in quotes, i.e. --indent='    ',
            or --indent='\\t'. Default is 4 spaces.
        -t {True, False}, --tree={True, False}
            Specify if a tree-like structure should be kept. Default is False.
        -o STRING, --output=STRING
            Output file name. Output is piped to stdout be default.
    """

if __name__ == '__main__':
    import os,sys, getopt

    if not os.path.exists(sys.argv[-1]):
        print "Invalid input file specified."
        print usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:t:o:', ['help', 'indent=', 'tree=','output='])
    except getopt.GetoptError:
        print usage()
        sys.exit(2)

    # Defaults
    tab = ' '*4
    write_output = False
    tree = False

    # Parse and set options.
    for o, a in opts:
        if o in ('-h', '--help'):
            print usage()
            sys.exit(0)
        if o in ('-i', '--indent'):
            tab = a.replace('\\t', '\t')
        if o in ('-t', '--tree'):
            tree = (a == 'True')
        if o in ('-o', '--output'):
            write_output = True
            output_name  = a

    with open(sys.argv[-1], 'r') as f:
        output = outline_to_dot(f.read(), tab, tree)
    if write_output:
        with open(output_name, 'w') as f:
            f.write(output)
    else:
        print output
