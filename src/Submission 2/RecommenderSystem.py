"""
RecommenderSystem.py - Student Template for Image Recommendation System

This class implements the recommendation system for Phase 2 and Phase 3 of the project.
It uses CLIP embeddings to find similar images and generate transition paths.

IMPORTANT NOTES FOR STUDENTS:
- Fill in the methods below with your own implementation
- Keep the method signatures exactly as shown (parameters and return types)
- You can add helper methods if needed
- The cosine_similarity function is provided for your convenience


Phases:
- Phase 2: find_similar_images() - Find k most similar images
- Phase 3: find_transition_prompts() - Find path connecting two images
"""

import json
import heapq
from typing import Dict, List, Tuple

from Graph_Djikstra import GrafHash

from Gallery import Gallery
from ImageData import ImageData
from ImageID import ImageID
from ImageViewer import ImageViewer
from SearchMetadata import SearchMetadata

STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by',
        'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
        'can', 'that', 'this', 'it', 'as', 'from', 'up', 'about', 'out', 'if', 'so',
        'than', 'no', 'not', 'only', 'own', 'such', 'too', 'very', 'just'
        }

class RecommenderSystem:
    """
    Recommender system for finding similar images and generating transition paths.

    Attributes:
        
        vectors_path: Path to the JSON file containing CLIP vectors
    """
    __slots__ = (
        'vectors',
        'uuids',
        '_image_vectors',
        'image_data',
        'image_id',
        '_viewer',
        '_norms',
        '_uuid_to_idx',
    )
    def __init__(self, vectors_path: str, image_data=None, image_id=None):
        """
        Initialize the recommender system by loading CLIP vectors.

        Args:
            vectors_path: Path to JSON file with CLIP embeddings
                         Format: {"uuid": {"image_embedding": [...], "text_embedding": [...]}, ...}
            image_data: (Optional) ImageData instance from Phase 1 for metadata access
            image_id: (Optional) ImageID instance from Phase 1 for UUID mapping
        """
        with open(vectors_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Llegeix i accepta {"uuid": {...}} i {"vectors": {...}}
        self.vectors: Dict[str, Dict[str, List[float]]] = data.get("vectors", data)

        # Helpers per a accés ràpid
        self.uuids: List[str] = []
        self._image_vectors: List[List[float]] = []
        for uid, entry in self.vectors.items():
            self.uuids.append(uid)
            self._image_vectors.append(entry.get("image_embedding", []))

        # Integració amb fase 1
        self.image_data: ImageData = image_data or ImageData()
        self.image_id: ImageID = image_id or ImageID()
        self._viewer: ImageViewer = ImageViewer(self.image_data)

        # Caches preprocessats (omplerts a preprocess) per agilitat
        self._norms: List[float] = []
        self._uuid_to_idx: Dict[str, int] = {}

    def preprocess(self):
        """
        Preprocess and prepare data structures for efficient queries.

        This method is called once before running Phase 2/3 queries.
        Use it to build indexes or prepare other data structures
        that will speed up similarity computations.

        """
        self._uuid_to_idx = {uid: idx for idx, uid in enumerate(self.uuids)}
        self._norms = [self._vector_norm(vec) for vec in self._image_vectors]


    # CODI REPETIT ENTRE COSINE I NORMES, arreglar
    @staticmethod
    def _vector_norm(vec: List[float]) -> float:
        return sum(x * x for x in vec) ** 0.5


    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        """
        Compute cosine similarity between two vectors.

        Cosine similarity measures the angle between vectors:
        - 1.0 = identical direction (very similar)
        - 0.0 = perpendicular (not related)
        - -1.0 = opposite direction (very different)

        Args:
            vec_a: First vector (list of floats)
            vec_b: Second vector (list of floats)

        Returns:
            float: Cosine similarity score between -1.0 and 1.0

        Formula:
            similarity = (a · b) / (||a|| * ||b||)
            where · is dot product and ||a|| is the magnitude (norm) of vector a

        Implementation tips:
        - Handle edge cases: empty vectors, zero norms
        """
        # Calcula el producte escalar
        dot = sum(a * b for a, b in zip(vec_a, vec_b))

        # Calcula les magnituds (normes)
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5

        # Retorna la similitud (gestiona divisió per zero)
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def find_similar_images(self, query_uuid: str, k: int = 10) -> Gallery:
        """
        Find k most similar images to a query image.

        PHASE 2: This is the main evaluation method for Phase 2.

        Args:
            query_uuid: UUID of the query image
            k: Number of similar images to return (default 10)

        Returns:
            Gallery object with images field containing top-k similar UUIDs
            ordered from most to least similar

        Example:
            system = RecommenderSystem("vectors.json")
            system.preprocess()
            gallery = system.find_similar_images("uuid_123", k=10)
            print(gallery.images)  # ['uuid_45', 'uuid_67', ..., 'uuid_99']

        Evaluation:
        - Metric: Recall@100 (your top-10 vs ground truth top-100)
        - Timing: Tested on 1,000 queries
        - Scoring: 25 pts for precision + 15 pts for speed

        # IMPLEMENTED:
        # 1. Get query vector from self.vectors
        # 2. Calculate similarity to other images (use cosine_similarity)
        # 3. Sort by similarity (descending)
        # 4. Create and return Gallery with top-k images
        """

        # Assegura que les dades estan preprocessades
        if not self._norms or len(self._norms) != len(self._image_vectors):
            self.preprocess()

        gallery = Gallery(self._viewer, self.image_id)
        gallery.images = []

        # Comprovacions bàsiques
        if query_uuid not in self.vectors:
            print("query_uuid not in vectors")
            return gallery

        query_vec = self.vectors[query_uuid].get("image_embedding", [])
        if not query_vec:
            print(" not  query_vec")
            return gallery

        query_norm = self._vector_norm(query_vec)
        if not query_norm:
            print(" not  query_norm")
            return gallery

        uuids = self.uuids
        vectors = self._image_vectors
        norms = self._norms
        scores: List[Tuple[float, str]] = []
        append_score = scores.append

        # Calcula la similitud cosinus per a cada imatge
        for idx, uid in enumerate(uuids):
            if uid == query_uuid:
                continue

            vec = vectors[idx]
            norm_b = norms[idx] if idx < len(norms) else self._vector_norm(vec)
            if not norm_b:
                continue

            dot = sum(a * b for a, b in zip(query_vec, vec))
            sim = dot / (query_norm * norm_b)
            append_score((sim, uid))

        # Obté les k imatges més similars ordenades
        top_k = heapq.nlargest(k, scores, key=lambda x: x[0])
        gallery.images = [uid for _, uid in top_k]
        return gallery

    def find_transition_prompts(self, uuid_1: str, uuid_2: str) -> list:
        """
        Find a transition path of prompts connecting two images.

        PHASE 3: This is the main evaluation method for Phase 3.

        Args:
            uuid_1: Starting image UUID
            uuid_2: Destination image UUID

        Returns:
            List of prompts describing the visual transition from uuid_1 to uuid_2
            First element should be prompt of uuid_1, last should be prompt of uuid_2
            Length of list represents number of transition steps

        Example:
            prompts = system.find_transition_prompts(uuid_start, uuid_end)
            # Returns: [
            #   "a cat in the snow",          # uuid_start
            #   "an animal in the snow",      # intermediate
            #   "a creature in the snow",     # intermediate
            #   "a dragon in the snow",       # intermediate
            #   "a dragon by a mountain",     # uuid_end
            # ]

        Evaluation:
        - Metric: Word overlap (how many words match ground truth)
        - Timing: Tested on ~10 transitions
        - Scoring: 30 pts for quality + 10 pts for speed

        Algorithm overview:
        1. Get prompts for both images (use image_data if available)
        2. Extract meaningful words from prompts (stop word removal)
        3. Build a graph where nodes are images and edges connect similar images
        4. Return prompts along a path

        Key considerations:
        - Path quality: Should gradually transition from uuid_1 to uuid_2
        - Path length: Shorter paths are faster but may skip important intermediates

        TODO: Implement this method
        """
        # TODO:
        # 1. Validate that both UUIDs exist
        if uuid_1 not in self.vectors or uuid_2 not in self.vectors:
            return []

        # 2. Get prompts using self.image_data if available
        prompt1 = self.image_data.get_prompt(uuid_1)
        prompt2 = self.image_data.get_prompt(uuid_2)

        # 3. Build set of images to explore
        # Clean and split prompts
        words1 = prompt1.lower().replace('.', '').replace(',', '').split()
        words2 = prompt2.lower().replace('.', '').replace(',', '').split()
        
        # Create bag of words without stop words
        bag_of_words = set(words1 + words2) - STOP_WORDS
        
        search_metadata = SearchMetadata(self.image_data)

        img_exp = {uuid_1, uuid_2}
        
        for word in bag_of_words:
            # Add images that match the word in their prompt
            found_uuids = search_metadata.prompt(word)
            img_exp.update(found_uuids)

        # Filter out UUIDs that don't have vectors
        img_exp = {uid for uid in img_exp if uid in self.vectors}
        
        # Convert to list for indexing
        candidates = list(img_exp)
        
        # 4. Build similarity graph between candidates
        similarity = []
        similar_vertex = []
        
        # Pre-fetch vectors for performance
        candidate_vectors = {uid: self.vectors[uid]["image_embedding"] for uid in candidates} 
        
        # Compute pairwise similarities
        # We use 1 - similarity as distance because Dijkstra finds minimum path
        for i in range(len(candidates)):
            u = candidates[i]
            vec_u = candidate_vectors[u]
            
            for j in range(i + 1, len(candidates)):
                v = candidates[j]
                vec_v = candidate_vectors[v]
                
                sim = self.cosine_similarity(vec_u, vec_v)
                
                # Ensure distance is non-negative (Habría que comprobar que en algún caso podría ser negativa, lo dudo pporq cos_sim es [-1,1])
                dist = max(0.0, 1.0 - sim)
                
                #Graf Complet de momento
                similar_vertex.append((u, v))
                similarity.append(dist)

        G = GrafHash(candidates, similar_vertex, similarity, digraf=False)

        # 5. Find path 
        path_uuids = G.camiMesCurt(uuid_1, uuid_2)

        # 6. Extract and return prompts from path
        path_prompts = []
        for uid in path_uuids:
            path_prompts.append(self.image_data.get_prompt(uid))

        return path_prompts