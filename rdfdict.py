#!/usr/bin/env python
import rdflib
import sys
import os
import collections


class RDFdict(dict):
    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self.graph = rdflib.ConjunctiveGraph()
        self.parsed_files = set()

        #these two namespaces are required to function
        self.xsd  =  rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")
        self.rdfs =  rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")

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
        graph = rdflib.ConjunctiveGraph()
        graph.parse(path, format=format)
        for s,p,o in graph.triples([None, self.rdfs.seeAlso, None]):
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
                if isinstance(o, rdflib.BNode):
                    tree[s][p].append(self._structure(subject=o))
                else:
                    tree[s][p].append(o)
        return tree
    def interpret(self, *args):
        '''Interprets itself according to the namespaces dictionaries that map strings 
        to rdflib URIRefs. The strings that form the keys of the namespaces replace the 
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
        try:
            if isinstance(obj, rdflib.Literal):
                if(obj.datatype == self.xsd.integer):
                    return int(obj.decode())
                elif(obj.datatype == self.xsd.float):
                    return float(obj.decode())
                else:
                    return obj.decode()
            elif isinstance(obj, rdflib.URIRef):
                for key, namespace in self.namespaces.items():
                    if obj.startswith(namespace):
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
        URI = rdflib.URIRef(args.URI)

    rdf_dict = RDFdict()
    rdf_dict.parse(args.ttl_file)
    rdf_dict.structure(subject=URI)
    rdf_dict.interpret(namespaces.lv2, namespaces.w3, namespaces.usefulinc)
    pprint(rdf_dict)

