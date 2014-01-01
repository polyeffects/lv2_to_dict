import rdflib
lv2 = {
        "bufsize" : rdflib.Namespace("http://lv2plug.in/ns/ext/buf-size#"),
        "atom"    : rdflib.Namespace("http://lv2plug.in/ns/ext/atom#"),
        "lv2"     : rdflib.Namespace("http://lv2plug.in/ns/lv2core#"),
        "midi"    : rdflib.Namespace("http://lv2plug.in/ns/ext/midi#"),
}

w3 = {
        "xsd"     : rdflib.Namespace("http://www.w3.org/2001/XMLSchema#"),
        "rdfs"    : rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
        "rdf"     : rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        "owl"     : rdflib.Namespace("http://www.w3.org/2002/07/owl#"), 
}

usefulinc = {
        "doap"    : rdflib.Namespace("http://usefulinc.com/ns/doap#"),
}
