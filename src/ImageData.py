# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""
import json
from typing import Dict
import cfg

class ImageData:

    def __init__(self):
        self._image_data: Dict[str, Dict] = {} # {UUID : {Data}} 

    def add_image(self, uuid: str, file: str) -> None:
        if uuid not in self._image_data:
            self._image_data[uuid] = {
                'file': file,
                'prompt': 'None',
                'model': 'None',
                'seed': 'None',
                'cfg_scale': 'None',
                'steps': 'None',
                'sampler': 'None',
                'generated': 'None',
                'created_date': 'None',
                'dimensions': ('None', 'None') # O 'None', 'None' ???
            }

        else:
            raise KeyError("COLISIÓ") #Evitar colisions

    def remove_image(self, uuid: str) -> None:
        if uuid not in self._image_data:
            raise KeyError("No image found to remove with UUID:", uuid)

        del self._image_data[uuid]

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._image_data:
            raise KeyError(f"Image with UUID {uuid} not found in collection.")
        
        dades = self._image_data[uuid]
        filepath = dades['file']
        
        try:
            metadata = cfg.read_png_metadata(filepath)
            dimensions = cfg.get_png_dimensions(filepath)
        except AttributeError as e:
            raise AttributeError(f"Error reading metadata/dimensions for {filepath}: {e}")
            
        if metadata:
            prompt = metadata.get('Prompt', 'None')
            model = metadata.get('Model', 'None')
            seed = metadata.get('Seed', 'None')
            cfg_scale = metadata.get('CFG_Scale', 'None')
            steps = metadata.get('Steps', 'None')
            sampler = metadata.get('Sampler', 'None')
            generated = metadata.get('Generated', 'None')
            created_date = metadata.get('Created_Date', 'None')
    
        dimensions = cfg.get_png_dimensions(dades['file'])

        self._image_data[uuid] = {
            'prompt': prompt,
            'model': model,
            'seed': seed,
            'cfg_scale': cfg_scale,
            'steps': steps,
            'sampler': sampler,
            'generated': generated,
            'created_date': created_date,
            'dimensions': dimensions

        }
        
    def _get_metadata_field(self, uuid: str, field: str) -> str:
        if uuid not in self._image_data:
            raise KeyError(f"Image with UUID {uuid} not found.")
        return str(self._image_data[uuid][field])

    def get_prompt(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'prompt')

    def get_model(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'model')

    def get_seed(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'seed')

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'cfg_scale')

    def get_steps(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'steps')

    def get_sampler(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'sampler')

    def get_generated(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'generated')

    def get_created_date(self, uuid: str) -> str:
        return self._get_metadata_field(uuid, 'created_date')
    
    def get_dimensions(self, uuid: str) -> tuple:
        if uuid not in self._image_data:
            raise KeyError("No image found with UUID:", uuid)
        return self._image_data[uuid]['dimensions']
    
    def get_Image_Data(self):
        return self._image_data
    

    def __str__(self):
        return 'hola'
    
    def __len__(self):
        return 0
