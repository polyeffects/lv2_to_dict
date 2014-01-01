#python-RDFdict

Python-RDFdict is a small utility class that uses [RDFLib][1] to represent RDF as hierarchies. It is 
a subclass of `dict` with a few added methods that help parse and structure RDF. It turns 
itself into a dict of dicts that represents a hierarchy according to nodes. 

It also allows for interpreting URIRefs and Literals as strings, ints and floats. For an 
example usage run `python RDFdict.py -h` and read the bottom of RDFdict.py 

Some namespaces are included in [namespaces.py](namespaces.py) for convenience.

[1]: http://librdf.org/
