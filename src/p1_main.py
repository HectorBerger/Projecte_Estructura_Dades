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
    #gallery.show()
    

    #6) Fer cerques i crear galeries a partir dels resultats
    search = SearchMetadata(img_data)
    results = search.prompt("painted closeup") #george washington, dog, painted closeup
    print(f"Imatges trobades amb 'painted closeup' al prompt: {len(results)}")
    results_steps =search.steps("50")
    print(f"Imatges trobades amb '50' als steps: {len(results_steps)}")
    result_gallery = Gallery(img_viewer, img_id)
    for uid in results:
        result_gallery.add_image_at_end(uid)
    #result_gallery.show()
    create_mosaic_page(result_gallery, img_data, Path("output/mosaic.html"), thumb_size=(150,150), cols=5)

    
def create_mosaic_page(gallery: Gallery, image_data: ImageData, out_file: Path,
                       thumb_size=(200,200), cols=4, title="Mosaic Gallery"):
    
    entries = []

    for uid in gallery:
        try:
            fp = Path(image_data.get_file(uid))
        except Exception as e:
            print(f"  No se pudo obtener el path para UUID: {uid} ({e})")
            continue

        dir_base_original, nombre_archivo = os.path.split(cfg.get_canonical_pathfile(fp))
        # dir_base_original será '..\DiffusionDB_subset'

        # Obtener solo el nombre del subdirectorio: 'DiffusionDB_subset'
        subdirectorio = os.path.basename(dir_base_original) 

        # Construcción de la nueva ruta
        nueva_raiz = '.\\generated_images'
        ruta_modificada = os.path.join(nueva_raiz, subdirectorio, nombre_archivo)
        entries.append((uid,ruta_modificada))

    if not entries:
        raise ValueError("La galería no contiene imágenes.")

    figures = []
    for uid, path in entries:
        path = Path(path) if not isinstance(path, Path) else path
        if not path.exists():
            print(f"  File not found for UUID: {uid} -> {path}")
            continue
        try:
            # Abrir la imagen de forma segura y manejar transparencia
            with Image.open(path) as im:
                # Si tiene canal alpha, aplanar sobre fondo blanco para que sea visible en HTML
                if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                    im_rgba = im.convert("RGBA")
                    alpha = im_rgba.split()[-1]
                    bg = Image.new("RGBA", im_rgba.size, (255, 255, 255, 255))
                    bg.paste(im_rgba, mask=alpha)
                    im_rgb = bg.convert("RGB")
                else:
                    im_rgb = im.convert("RGB")

                # Crear thumbnail con buen filtro de remuestreo
                im_rgb.thumbnail(thumb_size, Image.LANCZOS)

                # Guardar como JPEG para reducir tamaño y compatibilidad
                buf = BytesIO()
                im_rgb.save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode("ascii")
                data_uri = f"data:image/jpeg;base64,{b64}"

            # prompt si existe en ImageData
            try:
                prompt = image_data.get_prompt(uid)
                if prompt is None or str(prompt).lower() == "none":
                    prompt = ""
            except Exception:
                prompt = ""
            full_uri = path.resolve().as_uri()
            caption = f"{uid}"
            if prompt:
                caption += f" — {prompt}"
            figures.append((data_uri, full_uri, caption))
        except UnidentifiedImageError as e:
            print(f"  No se pudo abrir imagen {path}: {e}")
            continue
        except Exception as e:
            print(f"  Error procesando imagen {path}: {e}")
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

if __name__ == "__main__":
    main()