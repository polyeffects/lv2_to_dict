#!/usr/bin/env python
import rdflib
import sys
import os

class Model(object):
    namespaces = {
            "xsd"     : rdflib.Namespace("http://www.w3.org/2001/XMLSchema#"),
            "rdfs"    : rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "rdf"     : rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
            "bufsize" : rdflib.Namespace("http://lv2plug.in/ns/ext/buf-size#"),
            "atom"    : rdflib.Namespace("http://lv2plug.in/ns/ext/atom#"),
            "lv2"     : rdflib.Namespace("http://lv2plug.in/ns/lv2core#"),
            "midi"    : rdflib.Namespace("http://lv2plug.in/ns/ext/midi#"),
            "owl"     : rdflib.Namespace("http://www.w3.org/2002/07/owl#"), 
            "doap"    : rdflib.Namespace("http://usefulinc.com/ns/doap#"),
            "slim"    : rdflib.Namespace("https://github.com/kasbah/slim_looper.lv2#"),
            }
    def __init__(self, format='n3'):
        self.graph = rdflib.ConjunctiveGraph()
        self.format = format
        self.parsed_files = set()
    def parse(self, path):
        if not path.startswith('file://'):
            path = os.path.realpath(path)
            assert os.path.exists(path)
            path = 'file://%s' % path
        if path in self.parsed_files:
            return
        self.parsed_files.add(path)
        graph = rdflib.ConjunctiveGraph()
        graph.parse(path, format=self.format)
        for s,p,o in graph.triples([None, self.namespaces["rdfs"].seeAlso, None]):
            self.parse(o)
        self.graph += graph
    def interpret(self, obj):
        try:
            if isinstance(obj, rdflib.Literal):
                if(obj.datatype == self.namespaces["xsd"].integer):
                    return int(obj.decode())
                elif(obj.datatype == self.namespaces["xsd"].float):
                    return float(obj.decode())
                else:
                    return unicode(obj.decode())
            elif isinstance(obj, rdflib.URIRef):
                for key, namespace in self.namespaces.items():
                    if namespace in obj:
                        return key + ":" + obj.split("#")[1]
                else:
                    return obj
            else:
                return obj
        except:
            return obj
    def structure(self, subject=None):
        tree = {}
        for s,p,o in self.graph.triples((subject, None, None)):
                s = self.interpret(s)
                p = self.interpret(p)
                if s not in tree:
                    tree[s] = {} 
                if p not in tree[s]:
                    tree[s][p] = []
                if isinstance(o, rdflib.BNode):
                    tree[s][p].append(self.structure(subject=o))
                else:
                    tree[s][p].append(self.interpret(o))
        return tree

if __name__ == "__main__":
    from pprint import pprint
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ttl_file", help='''File in turtle format that contains the info
                                          for the RDF graph.''')
    parser.add_argument("URI", help='''URI that forms the base node for the dictionary. 
                                       If not given all nodes are parsed and printed.''',
                                       nargs="?", default=None)
    args = parser.parse_args()
    model = Model()
    model.parse(args.ttl_file)
    if args.URI is None:
        URI = None
    else:
        URI = rdflib.URIRef(args.URI)
    tree = model.structure(subject=URI)
    pprint(tree)

