# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
from PIL import Image
from ImageData import ImageData

class ImageViewer:

    def __init__(self, Image_Data: ImageData):
        self._image = Image_Data

    """    def print_image(self, uuid: str) -> None:
        dades = self._image._image_data[uuid]
        msg = f"Dimensions: {dades['width']} x {dades['height']}\n \
            - Prompt: {dades['prompt'][:50]}... \n \
            - Model: {dades['model']} \n \
            - Seed: {dades['seed']} \n \
            - CFG Scale: {dades['cfg_scale']} \n \
            - Steps: {dades['steps']} \n \
            - Sampler: {dades['sampler']} \n \
            - Generated: {dades['generated']} \n \
            - Created Date: {dades['created_date']} \n \
            - UUID: {dades['uuid']} \n \
            - Path de l'arxiu: {dades['file']}"
        print(msg)
        """

    def print_image(self, uuid: str) -> None:
        w, h = self._image.get_dimensions(uuid)
        prompt = self._image.get_prompt(uuid)
        model  = self._image.get_model(uuid)
        seed   = self._image.get_seed(uuid)
        cfg_s  = self._image.get_cfg_scale(uuid)
        steps  = self._image.get_steps(uuid)
        samp   = self._image.get_sampler(uuid)
        gen    = self._image.get_generated(uuid)
        date   = self._image.get_created_date(uuid)

        # Necessitem el path del fitxer per el msg
        path = self._image.get_Image_Data()[uuid]['file']

        msg = (
            f"Dimensions: {w} x {h}\n"
            f"- Prompt: {prompt[:50]}...\n"
            f"- Model: {model}\n"
            f"- Seed: {seed}\n"
            f"- CFG Scale: {cfg_s}\n"
            f"- Steps: {steps}\n"
            f"- Sampler: {samp}\n"
            f"- Generated: {gen}\n"
            f"- Created Date: {date}\n"
            f"- UUID: {uuid}\n"
            f"- Path de l'arxiu: {path}"
        )
        print(msg)


    def show_file(self, file: str) -> None:
        try:
            img = Image.open(file)
            img.show()
        except Exception as e:
            print(f"No s'ha pogut mostrar la imatge: {e}")

    def show_image(self, uuid: str, mode: int) -> None:
        if mode == 0:
                self.print_image(uuid)
        elif mode == 1:
                self.print_image(uuid)
                file = self._image._image_data[uuid]["file"]
                self.show_file(file)
                input("Pressiona Enter per continuar...")
        elif mode == 2:
                file = self._image._image_data[uuid]["file"]
                self.show_file(file)
                input("Pressiona Enter per continuar...")
        else:
                raise ValueError("Mode invàlid:", mode)
        
    def __str__(self):
        return 'hola'
    
    def __len__(self):
        return 0
