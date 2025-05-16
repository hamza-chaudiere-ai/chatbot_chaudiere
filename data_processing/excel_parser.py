# data_processing/excel_parser.py
import pandas as pd
import os
import re
from datetime import datetime

class ExcelParser:
    """
    Classe pour analyser les fichiers Excel contenant l'historique des arrêts
    """
    
    def __init__(self, file_path):
        """
        Initialisation avec le chemin du fichier Excel
        
        Args:
            file_path (str): Chemin vers le fichier Excel à analyser
        """
        self.file_path = file_path
        self.data = None
        
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
            
        # Vérifier si le fichier est au format Excel
        if not (file_path.endswith('.xlsx') or file_path.endswith('.xls')):
            raise ValueError("Le fichier doit être au format Excel (.xlsx ou .xls).")
    
    def parse(self):
        """
        Analyse le fichier Excel et normalise les données
        
        Returns:
            pandas.DataFrame: DataFrame contenant les données normalisées
        """
        try:
            # Lecture du fichier Excel
            df = pd.read_excel(self.file_path)
            
            # Normalisation des noms de colonnes
            df.columns = [self._normalize_column_name(col) for col in df.columns]
            
            # Identifier les colonnes requises
            required_columns = ['composant', 'sous_composant', 'cause', 'duree']
            
            # Vérifier si toutes les colonnes requises sont présentes
            missing_columns = []
            column_mapping = {}
            
            for req_col in required_columns:
                found = False
                for col in df.columns:
                    if req_col in col.lower() or self._is_similar_column(req_col, col):
                        column_mapping[col] = req_col
                        found = True
                        break
                
                if not found:
                    missing_columns.append(req_col)
            
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans le fichier Excel: {', '.join(missing_columns)}. "
                                 f"Colonnes trouvées: {', '.join(df.columns)}")
            
            # Renommer les colonnes
            df = df.rename(columns=column_mapping)
            
            # Sélectionner uniquement les colonnes requises
            df = df[[column_mapping.get(col, col) for col in column_mapping.keys()]]
            
            # Normalisation des noms de composants et sous-composants
            df['composant'] = df['composant'].apply(self._normalize_component_name)
            df['sous_composant'] = df['sous_composant'].apply(self._normalize_subcomponent_name)
            
            # Convertir les durées en nombres (heures)
            df['duree'] = df['duree'].apply(self._convert_to_hours)
            
            # Normaliser les causes
            df['cause'] = df['cause'].apply(self._normalize_cause)
            
            # Stocker les données
            self.data = df
            
            return df
        
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse du fichier Excel: {str(e)}")
    
    def _normalize_column_name(self, name):
        """
        Normalise le nom d'une colonne
        
        Args:
            name (str): Nom de la colonne à normaliser
            
        Returns:
            str: Nom normalisé
        """
        name = str(name).lower()
        name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')
        return name
    
    def _is_similar_column(self, required, actual):
        """
        Vérifie si le nom d'une colonne est similaire à un nom requis
        
        Args:
            required (str): Nom de colonne requis
            actual (str): Nom de colonne actuel
            
        Returns:
            bool: True si les noms sont similaires, False sinon
        """
        actual = actual.lower()
        
        # Mappings pour les colonnes
        column_mappings = {
            'composant': ['composant', 'composants', 'component', 'equipement', 'équipement', 'materiel', 'matériel'],
            'sous_composant': ['sous_composant', 'sous-composant', 'subcomponent', 'sous_composants', 'sous-composants'],
            'cause': ['cause', 'causes', 'raison', 'motif', 'origine', 'reason'],
            'duree': ['duree', 'durée', 'heures', 'temps', 'time', 'duration', 'arret', 'arrêt']
        }
        
        if required in column_mappings:
            return any(term in actual for term in column_mappings[required])
        
        return False
    
    def _normalize_component_name(self, name):
        """
        Normalise le nom d'un composant
        
        Args:
            name (str): Nom du composant à normaliser
            
        Returns:
            str: Nom normalisé
        """
        if pd.isna(name):
            return "Inconnu"
        
        name = str(name).strip().lower()
        
        # Mappings pour les composants
        component_mappings = {
            'economiseur bt': ['eco bt', 'économiseur bt', 'economiseur basse température', 'économiseur basse température'],
            'economiseur ht': ['eco ht', 'économiseur ht', 'economiseur haute température', 'économiseur haute température'],
            'surchauffeur bt': ['sur bt', 'sbt', 'surchauf bt', 'surchauffeur basse température'],
            'surchauffeur ht': ['sur ht', 'sht', 'surchauf ht', 'surchauffeur haute température'],
            'rechauffeur bt': ['rch bt', 'rbt', 'rechauff bt', 'réchauffeur bt', 'rechauffeur basse température', 'réchauffeur basse température'],
            'rechauffeur ht': ['rch ht', 'rht', 'rechauff ht', 'réchauffeur ht', 'rechauffeur haute température', 'réchauffeur haute température']
        }
        
        for standard_name, variations in component_mappings.items():
            if name in variations or any(variation in name for variation in variations):
                return standard_name
        
        return name
    
    def _normalize_subcomponent_name(self, name):
        """
        Normalise le nom d'un sous-composant
        
        Args:
            name (str): Nom du sous-composant à normaliser
            
        Returns:
            str: Nom normalisé
        """
        if pd.isna(name):
            return "Inconnu"
        
        name = str(name).strip().lower()
        
        # Mappings pour les sous-composants
        subcomponent_mappings = {
            'epingle': ['épingle', 'epingles', 'épingles', 'tube epingle', 'tube épingle'],
            'collecteur entree': ['collecteur entrée', 'collecteur d\'entrée', 'collecteur d entree', 'coll. entrée', 'collecteur e'],
            'collecteur sortie': ['collecteur de sortie', 'collecteur sortie', 'coll. sortie', 'collecteur s'],
            'tube porteur': ['tubes porteurs', 'porteur', 'tube support', 'tubes supports'],
            'branches entree': ['branches entrée', 'branche entrée', 'branch. entrée'],
            'branches sortie': ['branches sortie', 'branche sortie', 'branch. sortie'],
            'tubes suspension': ['tube suspension', 'tubes de suspension', 'suspension']
        }
        
        for standard_name, variations in subcomponent_mappings.items():
            if name in variations or any(variation in name for variation in variations):
                return standard_name
        
        return name
    
    def _convert_to_hours(self, duration):
        """
        Convertit une durée en heures
        
        Args:
            duration: La durée à convertir
            
        Returns:
            float: Durée en heures
        """
        if pd.isna(duration):
            return 0.0
        
        try:
            # Si c'est déjà un nombre, le retourner directement
            return float(duration)
        except (ValueError, TypeError):
            # Si c'est une chaîne, essayer de la parser
            duration_str = str(duration).lower()
            
            # Format "HH:MM:SS" ou "HH:MM"
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 3:  # HH:MM:SS
                    return float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
                elif len(parts) == 2:  # HH:MM
                    return float(parts[0]) + float(parts[1])/60
            
            # Format "Xh Ymin"
            match = re.search(r'(\d+)h\s*(?:(\d+)m(?:in)?)?', duration_str)
            if match:
                hours = float(match.group(1))
                minutes = float(match.group(2)) if match.group(2) else 0
                return hours + minutes/60
            
            # Format "X heures Y minutes"
            match = re.search(r'(\d+)\s*heure[s]?\s*(?:(\d+)\s*minute[s]?)?', duration_str)
            if match:
                hours = float(match.group(1))
                minutes = float(match.group(2)) if match.group(2) else 0
                return hours + minutes/60
            
            # Autres formats non reconnus, retourner 0
            return 0.0
    
    def _normalize_cause(self, cause):
        """
        Normalise la cause d'une défaillance
        
        Args:
            cause (str): Cause à normaliser
            
        Returns:
            str: Cause normalisée
        """
        if pd.isna(cause):
            return "Inconnue"
        
        cause = str(cause).strip().lower()
        
        # Mappings pour les causes
        cause_mappings = {
            'corrosion': ['corrosion', 'rouille', 'oxydation', 'attaque chimique', 'piqure'],
            'fissure': ['fissure', 'fissuration', 'craquelure', 'fente'],
            'erosion': ['erosion', 'érosion', 'usure', 'abrasion'],
            'fatigue': ['fatigue', 'stress', 'tension'],
            'percement': ['percement', 'perforation', 'trou', 'perce'],
            'surchauffe': ['surchauffe', 'température élevée', 'chaleur excessive'],
            'encrassement': ['encrassement', 'dépôt', 'accumulation', 'obstruction', 'bouchage'],
            'vibration': ['vibration', 'oscillation'],
            'mauvais montage': ['mauvais montage', 'montage incorrect', 'défaut d\'assemblage'],
            'fuite': ['fuite', 'écoulement', 'perte', 'suintement']
        }
        
        for standard_cause, variations in cause_mappings.items():
            if cause in variations or any(variation in cause for variation in variations):
                return standard_cause
        
        return cause
    
    def save_normalized_data(self, output_path=None):
        """
        Sauvegarde les données normalisées dans un fichier Excel
        
        Args:
            output_path (str, optional): Chemin de sortie pour le fichier Excel.
                Si non fourni, un chemin par défaut sera utilisé.
        
        Returns:
            str: Chemin du fichier sauvegardé
        """
        if self.data is None:
            raise ValueError("Aucune donnée à sauvegarder. Appelez d'abord la méthode parse().")
        
        if output_path is None:
            # Créer un nom de fichier basé sur le nom du fichier d'origine
            base_name = os.path.basename(self.file_path)
            name_without_ext = os.path.splitext(base_name)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(os.path.dirname(self.file_path), f"{name_without_ext}_normalized_{timestamp}.xlsx")
        
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Sauvegarder le fichier
        self.data.to_excel(output_path, index=False)
        
        return output_path