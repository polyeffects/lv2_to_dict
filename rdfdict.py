#!/usr/bin/env python
import rdflib
import sys
import os
import collections

import lv2_ns
import w3_ns
import usefulinc_ns


class RDFdict(collections.MutableMapping):
    namespaces = {
            "xsd"     : rdflib.Namespace("http://www.w3.org/2001/XMLSchema#"),
            "rdfs"    : rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            }
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self.graph = rdflib.ConjunctiveGraph()
        self.parsed_files = set()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return self.store.__repr__()

    def parse(self, path, format="n3"):
        if not path.startswith('file://'):
            path = os.path.realpath(path)
            assert os.path.exists(path)
            path = 'file://%s' % path
        if path in self.parsed_files:
            return
        self.parsed_files.add(path)
        graph = rdflib.ConjunctiveGraph()
        graph.parse(path, format=format)
        for s,p,o in graph.triples([None, self.namespaces["rdfs"].seeAlso, None]):
            self.parse(o)
        self.graph += graph
    def structure(self, subject=None):
        self.store = self._structure(subject=subject)
    def _structure(self, subject=None):
        tree = {}
        for s,p,o in self.graph.triples((subject, None, None)):
                if s not in tree:
                    tree[s] = {} 
                if p not in tree[s]:
                    tree[s][p] = []
                if isinstance(o, rdflib.BNode):
                    tree[s][p].append(self._structure(subject=o))
                else:
                    tree[s][p].append(o)
        return tree
    def interpret(self):
        self.store = self._interpret(self.store)
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
        try:
            if isinstance(obj, rdflib.Literal):
                if(obj.datatype == self.namespaces["xsd"].integer):
                    return int(obj.decode())
                elif(obj.datatype == self.namespaces["xsd"].float):
                    return float(obj.decode())
                else:
                    return obj.decode()
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
    rdf_dict = RDFdict()
    rdf_dict.parse(args.ttl_file)

    if args.URI is None:
        URI = None
    else:
        URI = rdflib.URIRef(args.URI)

    rdf_dict.structure(subject=URI)

    rdf_dict.namespaces.update(lv2_ns.namespaces)
    rdf_dict.namespaces.update(w3_ns.namespaces)
    rdf_dict.namespaces.update(usefulinc_ns.namespaces)
    rdf_dict.interpret()

    pprint(rdf_dict.store)

