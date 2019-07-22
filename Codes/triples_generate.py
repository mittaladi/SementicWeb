# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:48:45 2019

@author: Legen
"""
import csv
import rdflib
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF,FOAF
from rdflib import Namespace

attributes = []
values = []

with open("SpotifyFeatures.csv",'r',encoding = 'UTF8') as csvfile:
   
    csvreader = csv.reader(csvfile)  
    attributes = next(csvreader) 
    for row in csvreader: 
        values.append(row) 
attributes[0] = 'genre'        
dic = {}
for i in range(len(attributes)):
    dic[attributes[i]] = i

#########################################################################
mappingname = []       
title1 = []
with open("MappingFile_1.csv","r") as cs1:
    csvreader = csv.reader(cs1)
    title1 = next(csvreader)
    for row in csvreader:
        mappingname.append(row)

dictname = {}

for names in mappingname:
    dictname[names[0]] = names[1]
    
#########################################################################
     
mappingrelation = []
title2 = []
with open("MappingFile_2.csv","r") as cs1:
    csvreader = csv.reader(cs1)
    title2 = next(csvreader)
    for row in csvreader:
        mappingrelation.append(row)
        
##########################################################################

relations = []
for relation in mappingrelation:
    relation[0] = dictname[relation[0]]
    relation[2] = dictname[relation[2]]
    relations.append(relation)
########################################################################

for rel in relations:
    rel[0] = dic[rel[0]]
    rel[2] = dic[rel[2]]

########################################################################
L = []
M = []
T =[]
for z in range(len(relations)):  
    A = relations[z]
    FOAF.name = rdflib.term.URIRef(u'http://xmlns.com/foaf/0.1/'+A[1])
    T.append(FOAF.name)
    n = Namespace("http://example.org/TrackID/")
    n1 = Namespace("http://example.org/Duration/")
    a = [row[A[0]] for row in values]
    b = [row[A[2]] for row in values]
     
    for i in range(len(a)):
        temp1 = a[i]
        temp2 = b[i]
        n.temp1 = rdflib.term.URIRef(u'http://example.org/TrackID/'+a[i])
        n1.temp2 = rdflib.term.URIRef(u'http://example.org/Duration/'+b[i])
        t1 = n.temp1
        t2 = n1.temp2
        L.append(t1)
        M.append(t2)
    

g = Graph()

count = -1
for i in range(len(L)):
    if i%228159 == 0:
        count = count+1
    typ = T[count]
    g.add( (L[i], typ, M[i]) )
   
print (g.serialize(format='turtle'))


with open('Turtlefinal.ttl', 'ab') as file:
    file.write(g.serialize(format='turtle'))
    








from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
g = Graph()

for row in values:
   TrackID = BNode()


   g.add( (TrackID, RDF.type, FOAF.TrackID) )
   g.add((TrackID, FOAF.hasID, Literal(row[3])))
   g.add((TrackID, FOAF.hasDuration, Literal(row[7])))
   g.add( (TrackID, FOAF.hasName, Literal(row[0])) )
   g.add( (TrackID, FOAF.hasGenre,Literal(row[16]) ) )

for row in values:
   TrackName = BNode()


   g.add( (TrackName, RDF.type, FOAF.TrackName) )
   g.add( (TrackName, FOAF.hasID, Literal((row[3])) ))
   g.add( (TrackName, FOAF.hasAcousticness, Literal((row[5])) ))
   g.add( (TrackName, FOAF.hasInstrumentalness, Literal((row[9])) ))
   g.add( (TrackName, FOAF.hasLoudness,Literal((row[12]) ) ))
   g.add( (TrackName, FOAF.hasKeys,Literal((row[10]) ) ))
   g.add( (TrackName, FOAF.hasSpeechiness,Literal((row[14]) ) ))
   g.add( (TrackName, FOAF.hasTempo,Literal((row[15]) ) ))









