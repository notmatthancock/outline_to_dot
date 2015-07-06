Convert a simple markdown-style outline format to graphviz. Run `example.py` to see an example. Basically, this takes a string formatted in a indentation outline format and outputs the corresponding hierarchy in graphviz format. See below or `example.py`.

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
