# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""

from Gallery import Gallery 
from SearchMetadata import SearchMetadata
from ImageData import ImageData
from ImageViewer import ImageViewer
from ImageFiles import ImageFiles
from ImageID import ImageID
from pathlib import Path
import os
import cfg

from PIL import Image, UnidentifiedImageError

def create_mosaic(image_entries, out_file: Path, thumb_size=(200,200), cols=4, bg_color=(255,255,255)):
    """
    Crea un mosaico (collage) a partir de image_entries (iterable de tuples (uuid, data_dict)).
    Guarda el resultado en out_file i intenta obrir-lo amb el visualitzador per defecte.
    - image_entries: iterable de (uuid, data) on data['file'] és el path a la imatge
    - out_file: Path on s'emmagatzema el mosaic (format JPEG)
    - thumb_size: mida de cada miniatura (width, height)
    - cols: nombre de columnes del mosaic
    """
    entries = list(image_entries)
    if not entries:
        raise ValueError("No hay entradas para crear el mosaico.")

    thumbs = []
    for uid, data in entries:
        file_path = data.get('file')
        if not file_path:
            print(f"Warning: entrada {uid} no tiene 'file', se omite.")
            continue
        try:
            im = Image.open(file_path).convert("RGB")
            im.thumbnail(thumb_size)
            # Centrar la miniatura en un lienzo del tamaño thumb_size
            thumb = Image.new("RGB", thumb_size, bg_color)
            x = (thumb_size[0] - im.width) // 2
            y = (thumb_size[1] - im.height) // 2
            thumb.paste(im, (x, y))
            thumbs.append(thumb)
        except Exception as e:
            print(f"Warning: no se pudo procesar '{file_path}': {e}")

    if not thumbs:
        raise ValueError("No se han podido generar miniaturas para el mosaico.")

    rows = (len(thumbs) + cols - 1) // cols
    mosaic_w = cols * thumb_size[0]
    mosaic_h = rows * thumb_size[1]
    mosaic = Image.new("RGB", (mosaic_w, mosaic_h), bg_color)

    for idx, thumb in enumerate(thumbs):
        r = idx // cols
        c = idx % cols
        mosaic.paste(thumb, (c * thumb_size[0], r * thumb_size[1]))

    out_file.parent.mkdir(parents=True, exist_ok=True)
    mosaic.save(out_file, "JPEG", quality=90)
    try:
        mosaic.show()
    except Exception:
        pass

    return out_file

def main():
    path_file_exemple = cfg.get_one_file(1)
    
    #1) Carregar la col·lecció d'imatges
    img_files = ImageFiles()
    img_files.reload_fs()
    #print(img_files)

    #2) Generar UUID per a totes les imatges
    img_id = ImageID()
    for img_file in img_files.files_added():
        img_id.generate_uuid(img_file)
    #print(img_id)
        

    #3) Llegir metadades d'algunes imatges
    img_data = ImageData()
    for img_file in img_files.files_added():
            uuid = img_id.get_uuid(img_file)
            img_data.add_image(uuid, img_file)
            img_data.load_metadata(uuid)
        
            
        

    #4) Visualitzar imatges
    img_viewer = ImageViewer(img_data)
    img_viewer.show_image(cfg.get_uuid(path_file_exemple), mode=1)

    #5) Carregar i mostrar galeries
    gallery = Gallery(img_viewer, img_id)
    gallery_file = os.path.join(cfg.get_root(), 'galleries', 'example_gallery.json')
    gallery.load_gallery(gallery_file)

    #6) Fer cerques i crear galeries a partir dels resultats
    search = SearchMetadata(img_data)
    results = search.search_by_prompt("dragon", case_sensitive=False)
    print(f"Imatges trobades amb 'dragon' al prompt: {len(results)}")


if __name__ == "__main__":
    main()