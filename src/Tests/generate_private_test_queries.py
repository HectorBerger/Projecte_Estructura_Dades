import json
import random
from pathlib import Path


def generate_private_test_queries():
    """
    Generate a simple private_test_queries.json:

    {
      "queries": ["uuid_1", "uuid_2", ...]
    }

    We just sample some UUIDs from clip_vectors.json.
    """

    current_dir = Path(__file__).resolve().parent
    data_dir = current_dir.parent.parent / "data"
    vectors_path = data_dir / "clip_vectors.json"
    output_path = data_dir / "private_test_queries.json"

    if not vectors_path.exists():
        print(f"Error: Vectors file not found at {vectors_path}")
        return

    with open(vectors_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vectors = data.get("vectors", data)
    uuids = list(vectors.keys())

    if not uuids:
        print("No UUIDs found in clip_vectors.json")
        return

    # How many queries do we want?  e.g. 100 or all of them
    num_queries = min(100, len(uuids))
    queries = random.sample(uuids, num_queries)

    output = {"queries": queries}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(queries)} queries to {output_path}")


if __name__ == "__main__":
    generate_private_test_queries()
