## Indented Outline => Graphviz

Convert a simple indented (markdown inspired) outline format to graphviz. Essentially, this is a small function which takes a string formatted in a indented outline format and outputs the corresponding hierarchy in graphviz format. See below or `example.py`.

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
        "main" -> topic-one;
        "topic one" -> subtopic one;
        "main" -> "topic-two";
        "topic two" -> "subtopic one";
        "topic two" -> "subtopic two";
    }
