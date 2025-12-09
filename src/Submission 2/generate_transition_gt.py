
import json
import os
import sys
import random
from pathlib import Path
import networkx as nx
import re

# Add Submission 1 to path for imports
sys.path.append(str(Path(__file__).parent.parent / "Submission 1"))

from RecommenderSystem import RecommenderSystem
from ImageData import ImageData
from ImageID import ImageID
from SearchMetadata import SearchMetadata


def find_optimal_path_networkx(rs, uuid_1, uuid_2):
    """
    Find optimal path using NetworkX and ground truth logic (dense graph + Dijkstra).
    """
    if uuid_1 not in rs.vectors or uuid_2 not in rs.vectors:
        return []
        
    image_data = rs.image_data
    # Initialize SearchMetadata with populated imageData
    sm = SearchMetadata(image_data)
    
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by',
        'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
        'can', 'that', 'this', 'it', 'as', 'from', 'up', 'about', 'out', 'if', 'so',
        'than', 'no', 'not', 'only', 'own', 'such', 'too', 'very', 'just'
    }
    
    p1 = image_data.get_prompt(uuid_1)
    p2 = image_data.get_prompt(uuid_2)
    
    def get_words(text):
        if not text: return set()
        return set(re.findall(r'\b[a-z]+\b', text.lower())) - STOP_WORDS
        
    words = get_words(p1) | get_words(p2)
    
    candidates = {uuid_1, uuid_2}
    for w in words:
        # SearchMetadata returns list of UUIDs
        candidates.update(sm.prompt(w))
        
    # Validation: must be in vectors
    candidates = [u for u in candidates if u in rs.vectors]
    
    # Build Graph
    G = nx.Graph()
    candidate_vectors = {u: rs.vectors[u]['image_embedding'] for u in candidates}
    
    nodes = list(candidates)
    n = len(nodes)
    
    for i in range(n):
        u = nodes[i]
        vec_u = candidate_vectors[u]
        G.add_node(u) # Ensure node exists
        for j in range(i + 1, n):
            v = nodes[j]
            vec_v = candidate_vectors[v]
            
            sim = rs.cosine_similarity(vec_u, vec_v)
            # Distance: 1 - sim
            dist = 1.0 - sim
            if dist < 0: dist = 0.0
            
            G.add_edge(u, v, weight=dist)
            
    try:
        path = nx.shortest_path(G, source=uuid_1, target=uuid_2, weight='weight')
        return [image_data.get_prompt(u) for u in path]
    except nx.NetworkXNoPath:
        return []

def generate_ground_truth():
    # Paths
    current_dir = Path(__file__).parent
    # data dir is ../../data
    data_dir = current_dir.parent.parent / "data"
    vectors_path = data_dir / "clip_vectors.json"
    output_path = current_dir / "transition_ground_truth.json"
    image_dir = data_dir / "images"
    
    if not vectors_path.exists():
        print(f"Error: Vectors file not found at {vectors_path}")
        return

    print(f"Loading vectors from {vectors_path}...")
    
    # Initialize system
    # We need to initialize ImageData and ImageID properly if we want real prompts
    # But RecommenderSystem initializes them if not provided.
    # However, RecommenderSystem needs to know where images are to load metadata?
    # ImageData loads metadata from... where?
    # Usually ImageData needs to be populated.
    # Let's check how autograder does it.
    # autograder_alumne.py Phase 1 tests populate ImageData by scanning files.
    # Phase 2/3 tests pass image_data=None, so RecommenderSystem creates new ImageData().
    # But if ImageData is empty, get_prompt(uuid) will return empty string?
    # RecommenderSystem.py:
    # self.image_data: ImageData = image_data or ImageData()
    # prompt1 = self.image_data.get_prompt(uuid_1)
    # If ImageData is empty, prompt is empty.
    # We need to populate ImageData!
    
    # Let's try to populate ImageData like autograder does.
    print(f"Scanning images in {image_dir}...")
    
    image_files = []
    if image_dir.exists():
        for f in image_dir.glob("*.png"):
            image_files.append(str(f))
    
    print(f"Found {len(image_files)} images.")
    
    import cfg
    # We need to make sure cfg works.
    
    image_data = ImageData()
    image_id = ImageID()
    
    count = 0
    for img_path in image_files:
        try:
            # We need relative path for ImageID?
            # cfg.get_canonical_pathfile might be needed
            # But let's just try using the path we have
            uuid = image_id.generate_uuid(img_path)
            if uuid:
                image_data.add_image(uuid, img_path)
                image_data.load_metadata(uuid)
                count += 1
        except Exception as e:
            pass
            
    print(f"Loaded metadata for {count} images.")
    
    rs = RecommenderSystem(str(vectors_path), image_data=image_data, image_id=image_id)
    print("Preprocessing...")
    rs.preprocess()
    
    # Select random pairs
    uuids = rs.uuids
    if len(uuids) < 2:
        print("Not enough UUIDs to generate transitions.")
        return

    transitions = []
    num_transitions = 5
    
    print(f"Generating {num_transitions} transitions...")
    
    # We want some successful transitions.
    # Let's try to pick pairs that are somewhat similar?
    # Or just random? Random might result in no path if graph is disconnected.
    # But we want to test the path finding.
    
    for _ in range(num_transitions):
        u1 = random.choice(uuids)
        u2 = random.choice(uuids)
        while u1 == u2:
            u2 = random.choice(uuids)
            
        print(f"Finding path from {u1} to {u2}...")
        try:
            prompts = find_optimal_path_networkx(rs, u1, u2)
            
            if prompts:
                # Create word dict for evaluation
                word_dict = {}
                STOP_WORDS = {
                    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by',
                    'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
                    'can', 'that', 'this', 'it', 'as', 'from', 'up', 'about', 'out', 'if', 'so',
                    'than', 'no', 'not', 'only', 'own', 'such', 'too', 'very', 'just'
                }
                
                import re
                for p in prompts:
                    words = re.findall(r'\b[a-z]+\b', p.lower())
                    for w in words:
                        if w not in STOP_WORDS:
                            word_dict[w] = word_dict.get(w, 0) + 1
                            
                transitions.append({
                    "uuid_1": u1,
                    "uuid_2": u2,
                    "word_dict": word_dict,
                    "path_length": len(prompts)
                })
                print(f"  Found path of length {len(prompts)}")
            else:
                print("  No path found.")
                
        except Exception as e:
            print(f"  Error: {e}")

    output_data = {"transitions": transitions}
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Saved {len(transitions)} transitions to {output_path}")

if __name__ == "__main__":
    generate_ground_truth()
    