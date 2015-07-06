from outline_to_graphviz import outline_to_graphviz

s = \
"""
# This is a comment; blank lines get eaten.

main
    topic one
        subtopic one
    topic two
        subtopic one
        subtopic two
"""

print outline_to_graphviz(s)
