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
import requests
import math
import base64
from io import BytesIO

def create_mosaic_page(gallery: Gallery, image_data: ImageData, out_file: Path,
                       thumb_size=(200,200), cols=4, title="Mosaic Gallery"):
    
    entries = []
    print(gallery)

    for uid in gallery:
        try:
            fp = Path(image_data.get_file(uid))
        except Exception:
            # fallback directo al dict si get_file no está disponible
            fp = Path(image_data._image_data[uid]['file'])
        entries.append((uid, fp.resolve()))

    if not entries:
        raise ValueError("La galería no contiene imágenes.")

    figures = []
    for uid, path in entries:
        if not path.exists():
            continue
        try:
            im = Image.open(path).convert("RGBA")
            im.thumbnail(thumb_size)
            buf = BytesIO()
            im.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            data_uri = f"data:image/png;base64,{b64}"
            # prompt si existe en ImageData
            try:
                prompt = image_data.get_prompt(uid)
                if prompt == "None":
                    prompt = ""
            except Exception:
                prompt = ""
            full_uri = path.as_uri()
            caption = f"{uid}"
            if prompt:
                caption += f" — {prompt}"
            figures.append((data_uri, full_uri, caption))
        except Exception:
            continue

    # construir HTML
    css = f"""
    body {{ font-family: Arial, Helvetica, sans-serif; background:#f8f8f8; padding:20px; }}
    .grid {{ display:grid; grid-template-columns: repeat({cols}, 1fr); gap:12px; }}
    figure {{ background: #fff; padding:8px; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.08); margin:0; text-align:center; }}
    img {{ max-width:100%; height:auto; display:block; margin:0 auto 6px; }}
    figcaption {{ font-size:0.8rem; color:#333; word-break:break-word; }}
    """

    html_parts = [f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>",
                  f"<style>{css}</style></head><body>",
                  f"<h1>{title}</h1>",
                  "<div class='grid'>"]

    for data_uri, full_uri, caption in figures:
        html_parts.append(
            f"<figure><a href='{full_uri}' target='_blank' rel='noopener'>"
            f"<img src='{data_uri}' alt='thumb'></a><figcaption>{caption}</figcaption></figure>"
        )

    html_parts.append("</div></body></html>")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(html_parts), encoding="utf-8")
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
    uuid_exemple = img_id.get_uuid(path_file_exemple)
    #img_viewer.show_image(uuid_exemple, mode=1)


    #5) Carregar i mostrar galeries
    gallery = Gallery(img_viewer, img_id)
    gallery_file = os.path.join(cfg.get_root(), 'galleries', 'example_gallery.json')
    gallery.load_file(gallery_file)
    create_mosaic_page(gallery, img_data, Path("output/mosaic.html"), thumb_size=(150,150), cols=5)
    

    #6) Fer cerques i crear galeries a partir dels resultats
    search = SearchMetadata(img_data)
    results = search.search_by_prompt("dragon", case_sensitive=False)
    print(f"Imatges trobades amb 'dragon' al prompt: {len(results)}")
    

if __name__ == "__main__":
    main()