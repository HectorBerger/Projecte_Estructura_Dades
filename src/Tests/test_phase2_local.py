# test_phase2_local.py

import json
import os

from RecommenderSystem import RecommenderSystem
from ImageData import ImageData
from ImageID import ImageID


DATA_DIR = "data"  # adjust if needed
VECTORS_PATH = os.path.join(DATA_DIR, "clip_vectors.json")


def pick_some_uuids(vectors_path, n=5):
    """Pick n UUIDs from clip_vectors.json just to use as test queries."""
    with open(vectors_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vectors = data.get("vectors", data)
    all_uuids = list(vectors.keys())
    return all_uuids[:n]


def main():
    # Init helpers
    image_data = ImageData()
    image_id = ImageID()

    # Init recommender
    rs = RecommenderSystem(VECTORS_PATH, image_data=image_data, image_id=image_id)
    rs.preprocess()

    # Pick a few UUIDs to test
    test_uuids = pick_some_uuids(VECTORS_PATH, n=5)

    print("Testing Phase 2: find_similar_images\n")
    for uuid in test_uuids:
        print(f"Query UUID: {uuid}")
        gallery = rs.find_similar_images(uuid, k=5)
        print("  Top-5 similar UUIDs:")
        for i, uid in enumerate(gallery.images):
            prompt = rs._safe_prompt(uid)
            print(f"    {i+1}. {uid}  |  prompt={prompt!r}")
        print("-" * 60)


if __name__ == "__main__":
    main()
