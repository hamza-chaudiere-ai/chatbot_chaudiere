# chat/bot.py
import os
import sys
from colorama import init, Fore, Style
import random
import json
import re

# Ajouter le chemin du projet au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

from data_processing.excel_parser import ExcelParser
from data_processing.amdec_generator import AMDECGenerator
from maintenance.maintenance_planner import MaintenancePlanner

class Chatbot:
    """
    Classe pour le chatbot AMDEC
    """
    
    def __init__(self):
        """
        Initialisation du chatbot
        """
        # Initialiser colorama pour les couleurs dans la console
        init()
        
        # Charger les données de composants
        self.components_data = self._load_components_data()
        
        # Historique des conversations
        self.conversation_history = []
        
        # Modèles de réponses pour différents types de questions
        self.response_templates = {
            'greeting': [
                "Bonjour ! Comment puis-je vous aider avec la maintenance des chaudières aujourd'hui ?",
                "Salut ! Je suis là pour répondre à vos questions sur les AMDEC et la maintenance des chaudières.",
                "Bonjour, que puis-je faire pour vous concernant les chaudières et leur maintenance ?"
            ],
            'farewell': [
                "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions.",
                "À bientôt ! J'espère avoir pu vous aider.",
                "Bonne journée ! Je reste disponible pour toute autre question sur les chaudières."
            ],
            'component_info': [
                "Le {component} est un élément important de la chaudière. {info}",
                "Concernant le {component}, voici ce que je peux vous dire : {info}",
                "Informations sur le {component} : {info}"
            ],
            'failure_mode': [
                "Les modes de défaillance courants pour {component} - {subcomponent} incluent : {modes}",
                "Pour {component} - {subcomponent}, voici les défaillances typiques : {modes}",
                "Le {component} - {subcomponent} peut présenter les défaillances suivantes : {modes}"
            ],
            'maintenance': [
                "Pour la maintenance de {component} - {subcomponent}, je recommande : {maintenance}",
                "Voici les opérations de maintenance recommandées pour {component} - {subcomponent} : {maintenance}",
                "La maintenance de {component} - {subcomponent} nécessite : {maintenance}"
            ],
            'criticality': [
                "La criticité de {component} - {subcomponent} est de {criticality}. {interpretation}",
                "Pour {component} - {subcomponent}, l'indice de criticité est de {criticality}. {interpretation}",
                "Avec une criticité de {criticality}, {component} - {subcomponent} {interpretation}"
            ],
            'not_understood': [
                "Je ne suis pas sûr de comprendre votre question. Pouvez-vous reformuler ?",
                "Désolé, je n'ai pas bien saisi votre demande. Pourriez-vous préciser ?",
                "Je ne comprends pas complètement. Pouvez-vous me donner plus de détails ?"
            ]
        }
    
    def _load_components_data(self):
        """
        Charge les données des composants depuis un fichier JSON
        
        Returns:
            dict: Données des composants
        """
        # Chemin vers le fichier JSON
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                'data', 'chaudiere_data.json')
        
        # Si le fichier existe, le charger
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"{Fore.RED}Erreur lors du chargement des données : {str(e)}{Style.RESET_ALL}")
        
        # Retourner un dictionnaire vide si le fichier n'existe pas ou en cas d'erreur
        return {}
    
    def start_conversation(self):
        """
        Démarre une conversation avec l'utilisateur
        """
        # Message de bienvenue
        print(f"\n{Fore.CYAN}Bonjour ! Je suis votre assistant pour l'analyse AMDEC et la maintenance des chaudières.")
        print(f"Posez-moi des questions sur les composants, les défaillances, ou les procédures de maintenance.")
        print(f"Tapez 'exit' pour quitter la conversation.{Style.RESET_ALL}\n")
        
        # Boucle de conversation
        while True:
            # Récupérer la question de l'utilisateur
            user_input = input(f"{Fore.GREEN}Vous : {Style.RESET_ALL}")
            
            # Vérifier si l'utilisateur souhaite quitter
            if user_input.lower() in ['exit', 'quit', 'q', 'bye', 'au revoir']:
                # Message d'au revoir
                farewell = random.choice(self.response_templates['farewell'])
                print(f"\n{Fore.CYAN}Assistant : {farewell}{Style.RESET_ALL}\n")
                break
            
            # Traiter la question et générer une réponse
            response = self.generate_response(user_input)
            
            # Afficher la réponse
            print(f"\n{Fore.CYAN}Assistant : {response}{Style.RESET_ALL}\n")
            
            # Ajouter la question et la réponse à l'historique
            self.conversation_history.append({
                'user': user_input,
                'assistant': response
            })
    
    def generate_response(self, query):
        """
        Génère une réponse en fonction de la question de l'utilisateur
        
        Args:
            query (str): Question de l'utilisateur
            
        Returns:
            str: Réponse générée
        """
        # Normaliser la requête
        query = query.lower()
        
        # Vérifier si c'est une salutation
        if self._is_greeting(query):
            return random.choice(self.response_templates['greeting'])
        
        # Vérifier si la question concerne un composant spécifique
        component, subcomponent = self._extract_component_info(query)
        
        if component:
            # Si la question concerne un mode de défaillance
            if any(term in query for term in ['défaillance', 'panne', 'problème', 'bris', 'casse']):
                return self._get_failure_mode_response(component, subcomponent)
            
            # Si la question concerne la maintenance
            elif any(term in query for term in ['maintenance', 'entretien', 'réparer', 'inspecter']):
                return self._get_maintenance_response(component, subcomponent)
            
            # Si la question concerne la criticité
            elif any(term in query for term in ['criticité', 'critique', 'risque', 'danger', 'priorité']):
                return self._get_criticality_response(component, subcomponent)
            
            # Par défaut, donner des informations générales sur le composant
            else:
                return self._get_component_info_response(component, subcomponent)
        
        # Si aucun composant n'est identifié, essayer de comprendre le type de question
        elif any(term in query for term in ['défaillance', 'panne', 'problème']):
            return "Pour obtenir des informations sur les modes de défaillance, veuillez préciser le composant concerné. Par exemple : \"Quels sont les modes de défaillance de l'économiseur BT ?\""
        
        elif any(term in query for term in ['maintenance', 'entretien', 'réparer']):
            return "Pour obtenir des informations sur la maintenance, veuillez préciser le composant concerné. Par exemple : \"Comment faire la maintenance du surchauffeur HT ?\""
        
        # Réponse par défaut si la question n'est pas comprise
        return random.choice(self.response_templates['not_understood'])
    
    def _is_greeting(self, query):
        """
        Vérifie si la requête est une salutation
        
        Args:
            query (str): Requête à vérifier
            
        Returns:
            bool: True si c'est une salutation, False sinon
        """
        greetings = [
            'bonjour', 'salut', 'hello', 'hi', 'hey', 'coucou',
            'bonsoir', 'good morning', 'good afternoon', 'good evening'
        ]
        
        return any(greeting in query for greeting in greetings) and len(query.split()) < 5
    
    def _extract_component_info(self, query):
        """
        Extrait les informations de composant et sous-composant de la requête
        
        Args:
            query (str): Requête à analyser
            
        Returns:
            tuple: (composant, sous-composant) ou (None, None) si non trouvés
        """
        # Liste des composants et sous-composants
        components = {
            'economiseur bt': ['collecteur sortie', 'epingle'],
            'economiseur ht': ['collecteur entree', 'tubes suspension'],
            'surchauffeur bt': ['epingle', 'collecteur entree'],
            'surchauffeur ht': ['tube porteur', 'branches entree', 'collecteur sortie'],
            'rechauffeur bt': ['collecteur entree', 'tubes suspension', 'tube porteur'],
            'rechauffeur ht': ['branches sortie', 'collecteur entree', 'collecteur sortie']
        }
        
        # Alias pour les composants
        component_aliases = {
            'eco bt': 'economiseur bt',
            'économiseur bt': 'economiseur bt',
            'eco ht': 'economiseur ht',
            'économiseur ht': 'economiseur ht',
            'sur bt': 'surchauffeur bt',
            'sbt': 'surchauffeur bt',
            'sur ht': 'surchauffeur ht',
            'sht': 'surchauffeur ht',
            'rch bt': 'rechauffeur bt',
            'réchauffeur bt': 'rechauffeur bt',
            'rbt': 'rechauffeur bt',
            'rch ht': 'rechauffeur ht',
            'réchauffeur ht': 'rechauffeur ht',
            'rht': 'rechauffeur ht'
        }
        
        # Alias pour les sous-composants
        subcomponent_aliases = {
            'collecteur d\'entrée': 'collecteur entree',
            'collecteur entrée': 'collecteur entree',
            'collecteur de sortie': 'collecteur sortie',
            'épingle': 'epingle',
            'tube porteur': 'tube porteur',
            'tubes de suspension': 'tubes suspension',
            'branches d\'entrée': 'branches entree',
            'branches entrée': 'branches entree',
            'branches de sortie': 'branches sortie'
        }
        
        # Rechercher des composants dans la requête
        found_component = None
        
        # Vérifier d'abord les alias
        for alias, comp in component_aliases.items():
            if alias in query:
                found_component = comp
                break
        
        # Si aucun alias n'est trouvé, vérifier les noms complets
        if found_component is None:
            for comp in components.keys():
                if comp in query:
                    found_component = comp
                    break
        
        # Si toujours aucun composant n'est trouvé, retourner None, None
        if found_component is None:
            return None, None
        
        # Rechercher des sous-composants dans la requête
        found_subcomponent = None
        
        # Vérifier d'abord les alias
        for alias, subcomp in subcomponent_aliases.items():
            if alias in query and subcomp in components[found_component]:
                found_subcomponent = subcomp
                break
        
        # Si aucun alias n'est trouvé, vérifier les noms complets
        if found_subcomponent is None:
            for subcomp in components[found_component]:
                if subcomp in query:
                    found_subcomponent = subcomp
                    break
        
        # Si aucun sous-composant n'est trouvé, prendre le premier de la liste
        if found_subcomponent is None and components[found_component]:
            found_subcomponent = components[found_component][0]
        
        return found_component, found_subcomponent
    
    def _get_component_info_response(self, component, subcomponent):
        """
        Génère une réponse avec des informations sur un composant
        
        Args:
            component (str): Nom du composant
            subcomponent (str): Nom du sous-composant
            
        Returns:
            str: Réponse générée
        """
        # Formater les noms pour l'affichage
        component_display = component.replace('economiseur', 'Économiseur').replace('surchauffeur', 'Surchauffeur').replace('rechauffeur', 'Réchauffeur')
        subcomponent_display = subcomponent.replace('entree', 'entrée').replace('epingle', 'épingle')
        
        # Vérifier si les données du composant sont disponibles
        if 'chaudiere' in self.components_data and component in self.components_data['chaudiere']:
            comp_data = self.components_data['chaudiere'][component]
            
            # Construire une réponse informative
            info = f"{comp_data.get('description_simple', '')} "
            
            # Ajouter des informations sur les matériaux si disponibles
            if 'matériaux' in comp_data:
                material_info = []
                for mat_type, mat_value in comp_data['matériaux'].items():
                    material_info.append(f"{mat_type}: {mat_value}")
                
                if material_info:
                    info += f"Il est fabriqué avec {', '.join(material_info)}. "
            
            # Ajouter des informations sur la structure si disponibles
            if 'structure' in comp_data:
                structure_info = []
                for struct_type, struct_value in comp_data['structure'].items():
                    if isinstance(struct_value, list):
                        structure_info.append(f"{struct_type}: {', '.join(struct_value)}")
                    else:
                        structure_info.append(f"{struct_type}: {struct_value}")
                
                if structure_info:
                    info += f"Sa structure comprend {', '.join(structure_info)}. "
            
            # Ajouter des informations sur le sous-composant si disponibles
            subcmp_info = ""
            if 'AMDEC' in comp_data:
                subcmp_info = f"Le {subcomponent_display} est susceptible de subir des défaillances comme {comp_data['AMDEC'].get('mode_defaillance', '')}. "
            
            # Utiliser un modèle de réponse
            template = random.choice(self.response_templates['component_info'])
            response = template.format(component=component_display, info=info + subcmp_info)
            
            return response
        
        # Réponse par défaut si les données ne sont pas disponibles
        return f"Le {component_display} est un composant important de la chaudière. Le {subcomponent_display} est un élément critique qui nécessite une attention particulière lors de la maintenance."
    
    def _get_failure_mode_response(self, component, subcomponent):
        """
        Génère une réponse sur les modes de défaillance d'un composant
        
        Args:
            component (str): Nom du composant
            subcomponent (str): Nom du sous-composant
            
        Returns:
            str: Réponse générée
        """
        # Formater les noms pour l'affichage
        component_display = component.replace('economiseur', 'Économiseur').replace('surchauffeur', 'Surchauffeur').replace('rechauffeur', 'Réchauffeur')
        subcomponent_display = subcomponent.replace('entree', 'entrée').replace('epingle', 'épingle')
        
        # Modes de défaillance courants par type de composant et sous-composant
        failure_modes = {
            'economiseur bt': {
                'epingle': ['Corrosion externe', 'Érosion', 'Encrassement', 'Fuites locales'],
                'collecteur sortie': ['Caustic attack', 'Dépôts internes', 'Perte matière', 'Fissuration']
            },
            'economiseur ht': {
                'collecteur entree': ['Érosion par cendres', 'Amincissement accéléré', 'Corrosion interne'],
                'tubes suspension': ['Fatigue mécanique', 'Vibrations', 'Fissures externes']
            },
            'surchauffeur bt': {
                'epingle': ['Graphitization', 'Corrosion côté feu', 'Short-term overheat'],
                'collecteur entree': ['Corrosion interne', 'Érosion', 'Fissuration']
            },
            'surchauffeur ht': {
                'tube porteur': ['Long-term overheat', 'Rupture fluage', 'Déformation permanente'],
                'branches entree': ['Fireside corrosion', 'Perte métal externe', 'Fissuration'],
                'collecteur sortie': ['SCC (Stress Corrosion Cracking)', 'Fissures intergranulaires']
            },
            'rechauffeur bt': {
                'collecteur entree': ['Hydrogen damage', 'Microfissures', 'Corrosion interne'],
                'tubes suspension': ['Fatigue thermique', 'Fissures', 'Déformation'],
                'tube porteur': ['Fatigue thermique', 'Cycles démarrage/arrêt', 'Fissures']
            },
            'rechauffeur ht': {
                'branches sortie': ['Acid attack', 'Surface "fromage suisse"', 'Corrosion'],
                'collecteur entree': ['Waterside corrosion', 'Fissures internes', 'Dépôts'],
                'collecteur sortie': ['Dissimilar metal weld', 'Rupture soudure', 'Contraintes interfaces']
            }
        }
        
        # Vérifier si les données du composant sont disponibles
        modes = []
        if component in failure_modes and subcomponent in failure_modes[component]:
            modes = failure_modes[component][subcomponent]
        
        # Si aucun mode n'est trouvé, utiliser des modes génériques
        if not modes:
            modes = ['Corrosion', 'Érosion', 'Fatigue', 'Fissuration']
        
        # Ajouter des informations supplémentaires
        causes = ""
        effects = ""
        
        # Vérifier si les données AMDEC sont disponibles
        if 'chaudiere' in self.components_data and component in self.components_data['chaudiere']:
            comp_data = self.components_data['chaudiere'][component]
            
            if 'AMDEC' in comp_data:
                amdec_data = comp_data['AMDEC']
                
                if 'causes' in amdec_data:
                    causes = f" Ces défaillances sont souvent causées par {', '.join(amdec_data['causes'])}."
                
                if 'mode_defaillance' in amdec_data:
                    effects = f" Le mode de défaillance principal est {amdec_data['mode_defaillance']}."
        
        # Utiliser un modèle de réponse
        template = random.choice(self.response_templates['failure_mode'])
        response = template.format(
            component=component_display,
            subcomponent=subcomponent_display,
            modes=', '.join(modes)
        )
        
        return response + causes + effects
    
    def _get_maintenance_response(self, component, subcomponent):
        """
        Génère une réponse sur la maintenance d'un composant
        
        Args:
            component (str): Nom du composant
            subcomponent (str): Nom du sous-composant
            
        Returns:
            str: Réponse générée
        """
        # Formater les noms pour l'affichage
        component_display = component.replace('economiseur', 'Économiseur').replace('surchauffeur', 'Surchauffeur').replace('rechauffeur', 'Réchauffeur')
        subcomponent_display = subcomponent.replace('entree', 'entrée').replace('epingle', 'épingle')
        
        # Opérations de maintenance courantes par type de composant et sous-composant
        maintenance_ops = {
            'economiseur bt': {
                'epingle': [
                    'Inspection visuelle des surfaces',
                    'Contrôle d\'épaisseur par ultrasons',
                    'Nettoyage des dépôts',
                    'Application d\'un revêtement protecteur'
                ],
                'collecteur sortie': [
                    'Inspection visuelle des soudures',
                    'Test d\'étanchéité',
                    'Rinçage chimique',
                    'Contrôle du pH'
                ]
            },
            'economiseur ht': {
                'collecteur entree': [
                    'Nettoyage pneumatique',
                    'Inspection visuelle',
                    'Contrôle des raccords',
                    'Traitement anti-corrosion'
                ],
                'tubes suspension': [
                    'Installation de renforts',
                    'Surveillance vibratoire',
                    'Inspection visuelle',
                    'Vérification des fixations'
                ]
            },
            'surchauffeur bt': {
                'epingle': [
                    'Contrôle des soudures',
                    'Inspection thermique',
                    'Nettoyage des dépôts',
                    'Remplacement préventif'
                ],
                'collecteur entree': [
                    'Injection d\'additifs anti-slagging',
                    'Contrôle des raccords',
                    'Inspection des points chauds',
                    'Nettoyage interne'
                ]
            },
            'surchauffeur ht': {
                'tube porteur': [
                    'Installation de capteurs de température',
                    'Surveillance continue',
                    'Inspection de la structure cristalline',
                    'Analyse de contraintes'
                ],
                'branches entree': [
                    'Optimisation de la combustion',
                    'Nettoyage des surfaces',
                    'Contrôle des raccords',
                    'Analyse des dépôts'
                ],
                'collecteur sortie': [
                    'Remplacement des matériaux par des aciers austénitiques',
                    'Contrôle ultrasons',
                    'Analyse des contraintes',
                    'Inspection des soudures'
                ]
            },
            'rechauffeur bt': {
                'collecteur entree': [
                    'Contrôle chimie eau',
                    'Surveillance du pH',
                    'Inspection des dépôts',
                    'Nettoyage interne'
                ],
                'tubes suspension': [
                    'Inspection thermique',
                    'Analyse des vibrations',
                    'Renforcement des supports',
                    'Contrôle des fixations'
                ],
                'tube porteur': [
                    'Inspection thermique',
                    'Analyse des cycles',
                    'Contrôle des fixations',
                    'Renforcement structurel'
                ]
            },
            'rechauffeur ht': {
                'branches sortie': [
                    'Procédures nettoyage contrôlé',
                    'Inspection des surfaces',
                    'Analyse chimique des dépôts',
                    'Remplacement des joints'
                ],
                'collecteur entree': [
                    'Traitement eau déminéralisée',
                    'Contrôle de la corrosion',
                    'Inspection par endoscopie',
                    'Analyse des dépôts'
                ],
                'collecteur sortie': [
                    'Contrôle ultrasons soudure',
                    'Surveillance des interfaces',
                    'Inspection des contraintes',
                    'Traitement thermique'
                ]
            }
        }
        
        # Vérifier si les données du composant sont disponibles
        ops = []
        if component in maintenance_ops and subcomponent in maintenance_ops[component]:
            ops = maintenance_ops[component][subcomponent]
        
        # Si aucune opération n'est trouvée, utiliser des opérations génériques
        if not ops:
            ops = [
                'Inspection visuelle régulière',
                'Contrôle des paramètres opérationnels',
                'Nettoyage préventif',
                'Analyse des tendances'
            ]
        
        # Déterminer la fréquence de maintenance
        frequencies = {
            'economiseur bt': 'trimestrielle',
            'economiseur ht': 'semestrielle',
            'surchauffeur bt': 'trimestrielle',
            'surchauffeur ht': 'trimestrielle',
            'rechauffeur bt': 'semestrielle',
            'rechauffeur ht': 'trimestrielle'
        }
        
        frequency = frequencies.get(component, 'régulière')
        
        # Construire la réponse
        maintenance_text = f"La maintenance {frequency} devrait inclure : {', '.join(ops)}."
        
        # Ajouter des informations supplémentaires si disponibles
        equipment_info = ""
        
        # Vérifier si les données du composant sont disponibles
        if 'chaudiere' in self.components_data and component in self.components_data['chaudiere']:
            comp_data = self.components_data['chaudiere'][component]
            
            if 'maintenance' in comp_data:
                maint_data = comp_data['maintenance']
                
                if 'personnel' in maint_data:
                    equipment_info = f" Cette maintenance devrait être effectuée par {', '.join(maint_data['personnel'])}."
        
        # Utiliser un modèle de réponse
        template = random.choice(self.response_templates['maintenance'])
        response = template.format(
            component=component_display,
            subcomponent=subcomponent_display,
            maintenance=maintenance_text
        )
        
        return response + equipment_info
    
    def _get_criticality_response(self, component, subcomponent):
        """
        Génère une réponse sur la criticité d'un composant
        
        Args:
            component (str): Nom du composant
            subcomponent (str): Nom du sous-composant
            
        Returns:
            str: Réponse générée
        """
        # Formater les noms pour l'affichage
        component_display = component.replace('economiseur', 'Économiseur').replace('surchauffeur', 'Surchauffeur').replace('rechauffeur', 'Réchauffeur')
        subcomponent_display = subcomponent.replace('entree', 'entrée').replace('epingle', 'épingle')
        
        # Valeurs de criticité par défaut
        criticality_values = {
            'economiseur bt': {
                'epingle': 24,
                'collecteur sortie': 45
            },
            'economiseur ht': {
                'collecteur entree': 24,
                'tubes suspension': 16
            },
            'surchauffeur bt': {
                'epingle': 40,
                'collecteur entree': 24
            },
            'surchauffeur ht': {
                'tube porteur': 30,
                'branches entree': 24,
                'collecteur sortie': 30
            },
            'rechauffeur bt': {
                'collecteur entree': 30,
                'tubes suspension': 24,
                'tube porteur': 24
            },
            'rechauffeur ht': {
                'branches sortie': 36,
                'collecteur entree': 24,
                'collecteur sortie': 20
            }
        }
        
        # Récupérer la criticité
        criticality = 0
        if component in criticality_values and subcomponent in criticality_values[component]:
            criticality = criticality_values[component][subcomponent]
        
        # Si aucune criticité n'est trouvée, générer une valeur par défaut
        if criticality == 0:
            criticality = 25
        
        # Interprétation de la criticité
        interpretation = ""
        if criticality <= 12:
            interpretation = "présente une criticité négligeable. Une maintenance corrective est suffisante."
        elif criticality <= 16:
            interpretation = "présente une criticité moyenne. Une maintenance préventive systématique est recommandée."
        elif criticality <= 20:
            interpretation = "présente une criticité élevée. Une maintenance préventive conditionnelle est nécessaire."
        else:
            interpretation = "présente une criticité interdite. Une remise en cause complète de la conception est requise."
        
        # Utiliser un modèle de réponse
        template = random.choice(self.response_templates['criticality'])
        response = template.format(
            component=component_display,
            subcomponent=subcomponent_display,
            criticality=criticality,
            interpretation=interpretation
        )
        
        return response