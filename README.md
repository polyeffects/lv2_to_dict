#python-RDFdict

Python-RDFdict is a small utility class that uses RDFLib to represent RDF as hierarchies. It is 
a subclass of `dict` with a few added methods that help parse and structure RDF turning 
itself into a hierarchy of dicts according to nodes. It also allows you to interpret 
URIRefs and Literals. For an example usage run `python RDFdict.py -h` and read the
bottom of RDFdict.py 

Naturally, `librdf` is required.
