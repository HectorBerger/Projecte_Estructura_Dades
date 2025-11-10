# -*- coding: utf-8 -*-
import json
import ImageData 
import cfg
import platform
import sys
import os
import os.path
import uuid
from Gallery import Gallery
from ImageData import ImageData
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""

class SearchMetadata (): 
    def __init__ (self, Image_Data: ImageData) :
        self._ImageData = Image_Data

    def prompt (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['prompt'].find(sub) != -1:
                values.append(uuid)
        return values
    
    def model (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['model'].find(sub) != -1:
                values.append(uuid)
        return values
    
    def seed (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['seed'].find(sub) != -1:
                values.append(uuid)

        return values
    
    def cfg_scale (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['cfg_scale'].find(sub) != -1:
                values.append(uuid)
        return values

    def steps (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['steps'].find(sub) != -1:
                values.append(uuid)
        return values
    
    def sampler (self, sub: str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['sampler'].find(sub) != -1:
                values.append(uuid)
        return values
    
    def date (self, sub:str):
        values  = []
        for uuid, metadata in self._ImageData.get_Image_Data().items():
            if metadata['date'].find(sub) != -1:
                values.append(uuid)
        return values
    
    def and_operator (self, list1: list, list2: list):
        return [x for x in list1 if x in list2]
    
    def or_opperator (self, list1: list, list2: list):
        return list( set(list1) | set(list2))

        
