# rag/vectordb.py
import os
import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class VectorDB:
    """
    Base de données vectorielle simple pour la recherche de documents
    """
    
    def __init__(self, data_dir=None):
        """
        Initialisation de la base de données vectorielle
        
        Args:
            data_dir (str, optional): Répertoire contenant les données.
                Si non fourni, un répertoire par défaut sera utilisé.
        """
        # Définir le répertoire de données
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        else:
            self.data_dir = data_dir
        
        # Initialiser les attributs
        self.documents = []
        self.embeddings = None
        self.vectorizer = None
        self.db_path = os.path.join(self.data_dir, 'vectordb.pkl')
        
        # Charger la base de données si elle existe
        self._load_db()
    
    def _load_db(self):
        """
        Charge la base de données vectorielle depuis un fichier
        """
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'rb') as f:
                    db_data = pickle.load(f)
                
                self.documents = db_data.get('documents', [])
                self.embeddings = db_data.get('embeddings')
                self.vectorizer = db_data.get('vectorizer')
                
                print(f"Base de données vectorielle chargée avec {len(self.documents)} documents.")
            except Exception as e:
                print(f"Erreur lors du chargement de la base de données vectorielle : {str(e)}")
                # Initialiser une nouvelle base de données
                self._init_db()
        else:
            # Initialiser une nouvelle base de données
            self._init_db()
    
    def _init_db(self):
        """
        Initialise une nouvelle base de données vectorielle
        """
        # Créer les répertoires nécessaires
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Chemin des documents à indexer
        documents_dirs = [
            os.path.join(self.data_dir, 'models'),
            os.path.join(self.data_dir, 'maintenance')
        ]
        
        # Indexer les documents
        self._index_documents(documents_dirs)
    
    def _index_documents(self, directories):
        """
        Indexe les documents contenus dans les répertoires spécifiés
        
        Args:
            directories (list): Liste des répertoires à indexer
        """
        documents = []
        
        # Parcourir les répertoires
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                continue
            
            # Parcourir les fichiers
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                # Ignorer les répertoires
                if os.path.isdir(filepath):
                    continue
                
                # Traiter les différents types de fichiers
                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                    # Fichiers Excel
                    try:
                        df = pd.read_excel(filepath)
                        text = self._dataframe_to_text(df)
                        documents.append({
                            'id': filename,
                            'path': filepath,
                            'text': text,
                            'type': 'excel'
                        })
                    except Exception as e:
                        print(f"Erreur lors de l'indexation de {filename} : {str(e)}")
                
                elif filename.endswith('.docx'):
                    # Fichiers Word
                    try:
                        from docx import Document
                        doc = Document(filepath)
                        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                        documents.append({
                            'id': filename,
                            'path': filepath,
                            'text': text,
                            'type': 'docx'
                        })
                    except Exception as e:
                        print(f"Erreur lors de l'indexation de {filename} : {str(e)}")
                
                elif filename.endswith('.json'):
                    # Fichiers JSON
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        text = json.dumps(data, ensure_ascii=False)
                        documents.append({
                            'id': filename,
                            'path': filepath,
                            'text': text,
                            'type': 'json'
                        })
                    except Exception as e:
                        print(f"Erreur lors de l'indexation de {filename} : {str(e)}")
                
                elif filename.endswith('.txt'):
                    # Fichiers texte
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            text = f.read()
                        documents.append({
                            'id': filename,
                            'path': filepath,
                            'text': text,
                            'type': 'txt'
                        })
                    except Exception as e:
                        print(f"Erreur lors de l'indexation de {filename} : {str(e)}")
        
        # Mettre à jour les documents
        self.documents = documents
        
        # Créer les embeddings
        if documents:
            texts = [doc['text'] for doc in documents]
            self.vectorizer = TfidfVectorizer(max_features=1000)
            self.embeddings = self.vectorizer.fit_transform(texts)
        
        # Sauvegarder la base de données
        self._save_db()
    
    def _dataframe_to_text(self, df):
        """
        Convertit un DataFrame en texte
        
        Args:
            df (pandas.DataFrame): DataFrame à convertir
            
        Returns:
            str: Texte généré
        """
        text = ""
        
        # Ajouter les noms de colonnes
        text += "Colonnes: " + ", ".join(df.columns) + "\n\n"
        
        # Ajouter les données
        for i, row in df.iterrows():
            text += f"Ligne {i+1}: "
            for col in df.columns:
                text += f"{col}: {row[col]}, "
            text = text[:-2] + "\n"
        
        return text
    
    def _save_db(self):
        """
        Sauvegarde la base de données vectorielle dans un fichier
        """
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Sauvegarder les données
        db_data = {
            'documents': self.documents,
            'embeddings': self.embeddings,
            'vectorizer': self.vectorizer
        }
        
        with open(self.db_path, 'wb') as f:
            pickle.dump(db_data, f)
        
        print(f"Base de données vectorielle sauvegardée avec {len(self.documents)} documents.")
    
    def add_document(self, document):
        """
        Ajoute un document à la base de données
        
        Args:
            document (dict): Document à ajouter avec les clés 'id', 'path', 'text' et 'type'
        """
        # Vérifier si le document est valide
        if not all(key in document for key in ['id', 'path', 'text', 'type']):
            raise ValueError("Le document doit contenir les clés 'id', 'path', 'text' et 'type'.")
        
        # Ajouter le document
        self.documents.append(document)
        
        # Mettre à jour les embeddings
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(max_features=1000)
            self.embeddings = self.vectorizer.fit_transform([doc['text'] for doc in self.documents])
        else:
            # Calculer les embeddings pour le nouveau document
            new_embedding = self.vectorizer.transform([document['text']])
            
            # Concaténer avec les embeddings existants
            if self.embeddings is not None:
                self.embeddings = np.vstack([self.embeddings.toarray(), new_embedding.toarray()])
            else:
                self.embeddings = new_embedding
        
        # Sauvegarder la base de données
        self._save_db()
    
    def search(self, query, top_k=5):
        """
        Recherche les documents les plus similaires à une requête
        
        Args:
            query (str): Requête de recherche
            top_k (int, optional): Nombre de résultats à retourner
            
        Returns:
            list: Liste des documents les plus similaires
        """
        # Vérifier si la base de données est vide
        if not self.documents or self.embeddings is None or self.vectorizer is None:
            return []
        
        # Calculer l'embedding de la requête
        query_embedding = self.vectorizer.transform([query])
        
        # Calculer les similarités
        similarities = cosine_similarity(query_embedding, self.embeddings).flatten()
        
        # Trier les indices par similarité décroissante
        indices = np.argsort(similarities)[::-1][:top_k]
        
        # Récupérer les documents correspondants
        results = []
        for idx in indices:
            if similarities[idx] > 0.1:  # Seuil de similarité minimal
                results.append({
                    'document': self.documents[idx],
                    'similarity': float(similarities[idx])
                })
        
        return results
    
    def get_document_by_id(self, doc_id):
        """
        Récupère un document par son identifiant
        
        Args:
            doc_id (str): Identifiant du document
            
        Returns:
            dict: Document trouvé ou None si non trouvé
        """
        for doc in self.documents:
            if doc['id'] == doc_id:
                return doc
        
        return None
    
    def update_db(self):
        """
        Met à jour la base de données en ré-indexant tous les documents
        """
        # Chemin des documents à indexer
        documents_dirs = [
            os.path.join(self.data_dir, 'models'),
            os.path.join(self.data_dir, 'maintenance')
        ]
        
        # Indexer les documents
        self._index_documents(documents_dirs)