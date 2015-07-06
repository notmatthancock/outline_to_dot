"""
outline_to_graphviz.py
Author: Matt Hancock

Convert markdown-style outlines to graphviz language.
"""

def _get_indent_level(line, tab):
    """
    Get indentation level of string, line, based on string, tab.
    """
    i = 0
    while line.startswith(tab*i):
        i+=1
    return i-1

def outline_to_graphviz(input, tab=' '*4):
    """
    indent_to_dot converts a file where a tree-like hierarchy is specified
    by indentation to dot style language.

    input: str
        string to be converted to .dot language.
    tab: str
        specify the indentation marker used. default is 4 spaces, but
        any string could be used ('\\t' for instance).

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
            "main" -> "topicr two";
            "topic two" -> "subtopic one";
            "topic two" -> "subtopic two";
        }
    """
    lines = input.split('\n')
    # remove comments, blank lines
    lines = [line for line in lines if line.strip() and not line.startswith('#')]
    lt = len(tab)

    output = 'digraph G {\n'
    node   = {}
    ibase  = _get_indent_level(lines[0], tab)
    iprev  = ibase # initialize

    for line in lines:
        i = _get_indent_level(line, tab)
        if i < ibase:
            raise Exception('Indentation level began at %d, but current line is at level %d'%(ibase,i))
        elif i > iprev+1:
            raise Exception('Indentation level skipped. %s has no parent.' % line[lt*i:])
        elif i <= iprev+1:
            for k in range(i+1,iprev): node.pop(k)
            node[i] = line[lt*i:]
            if i is not ibase:
                output += '    \"%s\" -> \"%s\";\n' % (node[i-1], node[i])
        iprev = i
    output += '}'

    return output
