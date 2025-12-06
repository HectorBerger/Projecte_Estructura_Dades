# test_phase3_local.py

import json
import os

from RecommenderSystem import RecommenderSystem
from ImageData import ImageData
from ImageID import ImageID


DATA_DIR = "data"
VECTORS_PATH = os.path.join(DATA_DIR, "clip_vectors.json")


def pick_uuid_pairs(vectors_path, n_pairs=3, step=50):
    """
    Pick some (start, end) UUID pairs from the vectors just to test transitions.

    step controls how far apart the pairs are in the list so they're not identical.
    """
    with open(vectors_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vectors = data.get("vectors", data)
    all_uuids = list(vectors.keys())

    pairs = []
    for i in range(0, n_pairs * step, step):
        if i + step < len(all_uuids):
            pairs.append((all_uuids[i], all_uuids[i + step]))
        else:
            break
    return pairs


def main():
    image_data = ImageData()
    image_id = ImageID()

    rs = RecommenderSystem(VECTORS_PATH, image_data=image_data, image_id=image_id)
    rs.preprocess()

    pairs = pick_uuid_pairs(VECTORS_PATH, n_pairs=3, step=200)

    print("Testing Phase 3: find_transition_prompts\n")
    for (start_uuid, end_uuid) in pairs:
        print(f"Start UUID: {start_uuid}")
        print(f"End   UUID: {end_uuid}")

        prompts = rs.find_transition_prompts(start_uuid, end_uuid)
        print("\n  Path of prompts:")
        for i, p in enumerate(prompts):
            print(f"    {i+1}. {p!r}")
        print("-" * 60)


if __name__ == "__main__":
    main()
