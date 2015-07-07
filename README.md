## Indented outline => dot

Convert a simple indented (markdown inspired) outline format to graphviz. Essentially, this is a small function which takes a string formatted in a indented outline format and outputs the corresponding hierarchy in graphviz format. See below or `example.py`.

Example input file:

    # This is a comment; blank lines get eaten.

    main
        topic one
            subtopic one
        topic two
            subtopic one
            subtopic two

From the command line, running

    ./outline_to_dot.py input-file.txt

produces the output string:

    digraph G {
        "main" -> "topic one";
        "topic one" -> "subtopic one";
        "main" -> "topic two";
        "topic two" -> "subtopic one";
        "topic two" -> "subtopic two";
    }

The default output is to standard out, but one can specify an output file with 

    ./outline_to_dot.py -o output-file.dot input-filt.txt

So then
    
    dot -Tpng -o output-graph.png output-file.dot

produces the following graph:

![](https://raw.githubusercontent.com/notmatthancock/outline_to_dot/master/example.png)

Another useful option is to maintain a strict tree structure in the output. This is specified as follows:

    ./outline_to_dot.py -o output-file.dot --tree=True input-file.txt

Using the same input as above, this produces a slightly different graph:

![](https://raw.githubusercontent.com/notmatthancock/outline_to_dot/master/example-tree-True.png)
