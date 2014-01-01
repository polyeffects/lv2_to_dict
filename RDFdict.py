#!/usr/bin/env python
# Copyright 2014 Kaspar Emanuel <kaspar.emanuel@gmail.com> 
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys, os
import rdflib

rdflib_version = [int(i) for i in rdflib.__version__.split('.')]

if rdflib_version <= [2,4,99]:
    from rdflib.BNode import BNode
    from rdflib.Graph import ConjunctiveGraph
    from rdflib.URIRef import URIRef
    from rdflib.Literal import Literal
    from rdflib.Namespace import Namespace
    from rdflib.RDFS import RDFSNS as RDFS
    XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
else:
    from rdflib.graph import ConjunctiveGraph
    from rdflib.term import BNode
    from rdflib.term import Literal
    from rdflib.term import URIRef
    from rdflib.namespace import Namespace
    from rdflib.namespace import RDFS, XSD

class RDFdict(dict):
    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))
        self.graph = ConjunctiveGraph()
        self.parsed_files = set()
    def parse(self, path, format="n3"):
        '''Parse a file into the RDFdict.graph even with no namespaces given. The rdf 
        schema #seeAlso is supported and the files will be parsed recursively. '''
        if not path.startswith('file://'):
            path = os.path.realpath(path)
            assert os.path.exists(path)
            path = 'file://%s' % path
        if path in self.parsed_files:
            return
        self.parsed_files.add(path)
        graph = ConjunctiveGraph()
        graph.parse(path, format=format)
        for s,p,o in graph.triples([None, RDFS.seeAlso, None]):
            self.parse(o)
        self.graph += graph
    def structure(self, subject=None):
        '''Fills itself as a dictionary that represents the structure of the graph.
        Copies of dictionaries with nodes as subjects replace nodes that are objects. 
        ''' 
        self.update(self._structure(subject=subject))
    def _structure(self, subject=None):
        tree = {}
        for s,p,o in self.graph.triples((subject, None, None)):
                if s not in tree:
                    tree[s] = {} 
                if p not in tree[s]:
                    tree[s][p] = []
                if isinstance(o, BNode):
                    tree[s][p].append(self._structure(subject=o))
                else:
                    tree[s][p].append(o)
        return tree
    def interpret(self, *args):
        '''Interprets itself according to the namespaces dictionaries that map strings 
        to rdflib Namespaces. The strings that form the keys of the namespaces replace the 
        rdflib URIRefs. Rdflib Literals are interpreted as ints, floats or unicode 
        according to their data_type even with no namespaces given'''
        self.namespaces = {}
        for d in args:
            self.namespaces.update(d)
        self.update(self._interpret(self))
    def _interpret(self, tree):
        if isinstance(tree, dict):
            interp_tree = {}
            for key, item in tree.items():
                interp_key = self._interpret(key)
                if isinstance(item, dict):
                    interp_tree[interp_key] = self._interpret(item)
                elif isinstance(item, list):
                    interp_tree[interp_key] = [self._interpret(i) for i in item]
            return interp_tree
        else:
            return self._interpret_rdfobj(tree)
    def _interpret_rdfobj(self, obj):
            if isinstance(obj, Literal):
                if(obj.datatype == XSD.integer):
                    return int(obj)
                elif(obj.datatype == XSD.float):
                    return float(obj)
                else:
                    return str(obj)
            elif isinstance(obj, URIRef):
                for key, namespace in self.namespaces.items():
                    if obj.startswith(namespace):
                        return key + ":" + obj.split("#")[1]
                else:
                    return obj
            else:
                return obj

if __name__ == "__main__":
    from pprint import pprint
    import argparse
    import namespaces
    parser = argparse.ArgumentParser()
    parser.add_argument("ttl_file", help='''File in turtle format that contains the info
                                          for the RDF graph.''')
    parser.add_argument("URI", help='''URI that forms the base node for the dictionary. 
                                       If not given all nodes are parsed and printed.''',
                                       nargs="?", default=None)
    args = parser.parse_args()
    if args.URI is None:
        URI = None
    else:
        URI = URIRef(args.URI)

    rdf_dict = RDFdict()
    rdf_dict.parse(args.ttl_file)
    rdf_dict.structure(subject=URI)
    rdf_dict.interpret(namespaces.lv2, namespaces.w3, namespaces.usefulinc, namespaces.kxstudio)
    pprint(rdf_dict)

