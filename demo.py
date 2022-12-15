from rdfdict import RDFdict
import namespaces as ns
import rdflib
from pprint import pprint

ttl_file ="/usr/lib/lv2/avw.lv2/lfo_tempo.ttl"
#amp = rdflib.URIRef("http://avwlv2.sourceforge.net/plugins/avw/lfo_temp")

rdf_dict = RDFdict()

#we parse the file into the rdf_dict.graph which is a rdflib.ConjunctiveGraph
#the subject is optional but saves time parsing only what we care about
print("Fetching and parsing file, the fetching may take a while as it's an online resource.")
rdf_dict.parse(ttl_file) #, subject=amp)

#we populate rdf_dict with a structure
rdf_dict.structure()

#we replace the Literals with ints, floats and strings and the URIRefs according to the 
#namespaces we know about
rdf_dict.interpret(ns.lv2, ns.w3, ns.usefulinc, ns.kxstudio)
print(rdf_dict)

# pprint(rdf_dict) # [amp]["lv2:port"])
