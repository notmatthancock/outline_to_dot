## Indented outline => dot

Convert a simple indented (markdown inspired) outline format to dot language.

Example input file:

    # This is a comment; blank lines get eaten.

    main
        # Default indent marker is 4 spaces. This can be changed.
        topic one
            subtopic one
        topic two
            subtopic one
            subtopic two

From the command line, running

    ./outline_to_dot.py input-file.txt

produces the output:

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

    ./outline_to_dot.py --tree=True input-file.txt

Using the same input as above, this produces a slightly different graph:

![](https://raw.githubusercontent.com/notmatthancock/outline_to_dot/master/example-tree-True.png)
