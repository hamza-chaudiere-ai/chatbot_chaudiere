# rag/retriever.py
import os
import sys

# Ajouter le chemin du projet au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

from rag.vectordb import VectorDB

class Retriever:
    """
    Classe pour récupérer des informations pertinentes à partir d'une requête
    """
    
    def __init__(self, db=None):
        """
        Initialisation du récupérateur
        
        Args:
            db (VectorDB, optional): Base de données vectorielle.
                Si non fournie, une nouvelle instance sera créée.
        """
        self.db = db if db is not None else VectorDB()
    
    def retrieve(self, query, top_k=3):
        """
        Récupère les informations pertinentes pour une requête
        
        Args:
            query (str): Requête de recherche
            top_k (int, optional): Nombre de résultats à retourner
            
        Returns:
            list: Liste des informations récupérées
        """
        # Rechercher les documents pertinents
        search_results = self.db.search(query, top_k=top_k)
        
        # Extraire les informations pertinentes
        retrieved_info = []
        
        for result in search_results:
            document = result['document']
            similarity = result['similarity']
            
            # Extraire des segments pertinents du document
            segments = self._extract_segments(document['text'], query)
            
            # Ajouter les informations récupérées
            retrieved_info.append({
                'id': document['id'],
                'type': document['type'],
                'similarity': similarity,
                'segments': segments
            })
        
        return retrieved_info
    
    def _extract_segments(self, text, query, max_segments=3, segment_length=200):
        """
        Extrait des segments pertinents d'un texte
        
        Args:
            text (str): Texte à analyser
            query (str): Requête de recherche
            max_segments (int, optional): Nombre maximal de segments à extraire
            segment_length (int, optional): Longueur approximative des segments
            
        Returns:
            list: Liste des segments extraits
        """
        # Normaliser la requête
        query_words = set(query.lower().split())
        
        # Diviser le texte en paragraphes
        paragraphs = text.split('\n')
        
        # Calculer le score de pertinence pour chaque paragraphe
        scored_paragraphs = []
        
        for paragraph in paragraphs:
            # Ignorer les paragraphes vides
            if not paragraph.strip():
                continue
            
            # Calculer le score (nombre de mots de la requête présents dans le paragraphe)
            paragraph_words = paragraph.lower()
            score = sum(1 for word in query_words if word in paragraph_words)
            
            # Ajouter le paragraphe et son score
            scored_paragraphs.append((paragraph, score))
        
        # Trier les paragraphes par score décroissant
        scored_paragraphs.sort(key=lambda x: x[1], reverse=True)
        
        # Extraire les segments les plus pertinents
        segments = []
        
        for paragraph, score in scored_paragraphs[:max_segments]:
            # Ignorer les paragraphes non pertinents
            if score == 0:
                continue
            
            # Ajuster la longueur du segment
            if len(paragraph) > segment_length:
                # Rechercher la position approximative de la requête dans le paragraphe
                best_position = 0
                best_score = 0
                
                for i in range(0, len(paragraph) - segment_length, segment_length // 2):
                    window = paragraph[i:i + segment_length].lower()
                    window_score = sum(1 for word in query_words if word in window)
                    
                    if window_score > best_score:
                        best_score = window_score
                        best_position = i
                
                # Extraire le segment
                segment = paragraph[best_position:best_position + segment_length]
                
                # Ajouter des points de suspension si nécessaire
                if best_position > 0:
                    segment = "..." + segment
                
                if best_position + segment_length < len(paragraph):
                    segment = segment + "..."
            else:
                segment = paragraph
            
            segments.append(segment)
        
        return segments
    
    def update_db(self):
        """
        Met à jour la base de données
        """
        self.db.update_db()