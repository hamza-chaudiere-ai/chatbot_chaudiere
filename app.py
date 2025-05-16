# app.py
import os
import sys
from colorama import init, Fore, Style
import pandas as pd

# Initialisation de colorama pour les couleurs dans la console
init()

# Ajout des chemins au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'data_processing'))
sys.path.append(os.path.join(current_dir, 'maintenance'))
sys.path.append(os.path.join(current_dir, 'rag'))
sys.path.append(os.path.join(current_dir, 'chat'))

# Import des modules
from data_processing.excel_parser import ExcelParser
from data_processing.amdec_generator import AMDECGenerator
from maintenance.maintenance_planner import MaintenancePlanner
from chat.bot import Chatbot

def print_header():
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗")
    print(f"║ {Fore.YELLOW}SYSTÈME D'ANALYSE AMDEC ET MAINTENANCE DE CHAUDIÈRE{Fore.CYAN}       ║")
    print(f"╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def main_menu():
    print_header()
    print(f"\n{Fore.GREEN}Options disponibles:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Générer une nouvelle AMDEC à partir d'un historique")
    print(f"2. Créer une gamme de maintenance")
    print(f"3. Exécuter le chatbot AMDEC")
    print(f"4. Quitter{Style.RESET_ALL}")

    while True:
        try:
            choice = input(f"\nVotre choix (1-4): ")
            if choice == '1':
                generate_amdec()
                break
            elif choice == '2':
                create_maintenance()
                break
            elif choice == '3':
                launch_chatbot()
                break
            elif choice == '4':
                print(f"{Fore.YELLOW}Au revoir!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Option invalide, veuillez réessayer.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erreur: {str(e)}{Style.RESET_ALL}")

def generate_amdec():
    print_header()
    print(f"\n{Fore.GREEN}GÉNÉRATION D'UNE NOUVELLE AMDEC{Style.RESET_ALL}")
    
    # Sélection du fichier Excel
    excel_files = []
    historique_dir = os.path.join(current_dir, 'data', 'historique')
    
    if not os.path.exists(historique_dir):
        os.makedirs(historique_dir)
        
    for file in os.listdir(historique_dir):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            excel_files.append(file)
    
    if not excel_files:
        print(f"{Fore.RED}Aucun fichier Excel trouvé dans le dossier data/historique.{Style.RESET_ALL}")
        input("Appuyez sur Entrée pour revenir au menu principal...")
        main_menu()
        return
    
    print(f"\n{Fore.YELLOW}Fichiers Excel disponibles:{Style.RESET_ALL}")
    for i, file in enumerate(excel_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input(f"\nSélectionnez un fichier (1-{len(excel_files)}): "))
            if 1 <= choice <= len(excel_files):
                selected_file = excel_files[choice-1]
                excel_path = os.path.join(historique_dir, selected_file)
                break
            else:
                print(f"{Fore.RED}Choix invalide, veuillez réessayer.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
    
    # Traitement du fichier Excel
    print(f"\n{Fore.CYAN}Traitement du fichier {selected_file}...{Style.RESET_ALL}")
    try:
        parser = ExcelParser(excel_path)
        df = parser.parse()
        print(f"{Fore.GREEN}Fichier chargé avec succès!{Style.RESET_ALL}")
        
        # Génération de l'AMDEC
        print(f"\n{Fore.CYAN}Génération de l'AMDEC en cours...{Style.RESET_ALL}")
        amdec_generator = AMDECGenerator(df)
        amdec_generator.generate()
        amdec_generator.save_to_file()
        
        print(f"\n{Fore.GREEN}AMDEC générée avec succès! Fichier sauvegardé dans data/models/{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la génération de l'AMDEC: {str(e)}{Style.RESET_ALL}")
    
    input("\nAppuyez sur Entrée pour revenir au menu principal...")
    main_menu()

def create_maintenance():
    print_header()
    print(f"\n{Fore.GREEN}CRÉATION D'UNE GAMME DE MAINTENANCE{Style.RESET_ALL}")
    
    # Sélection du composant
    components = [
        "Économiseur BT", "Économiseur HT", "Surchauffeur BT", 
        "Surchauffeur HT", "Réchauffeur BT", "Réchauffeur HT"
    ]
    
    print(f"\n{Fore.YELLOW}Composants disponibles:{Style.RESET_ALL}")
    for i, comp in enumerate(components, 1):
        print(f"{i}. {comp}")
    
    while True:
        try:
            choice = int(input(f"\nSélectionnez un composant (1-{len(components)}): "))
            if 1 <= choice <= len(components):
                selected_component = components[choice-1]
                break
            else:
                print(f"{Fore.RED}Choix invalide, veuillez réessayer.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
    
    # Sous-composants disponibles selon le composant choisi
    subcomponents = {
        "Économiseur BT": ["Collecteur sortie", "Épingle"],
        "Économiseur HT": ["Collecteur entrée", "Tubes de suspension"],
        "Surchauffeur BT": ["Épingle", "Collecteur entrée"],
        "Surchauffeur HT": ["Tube porteur", "Branches entrée", "Collecteur sortie"],
        "Réchauffeur BT": ["Collecteur entrée", "Tubes suspension", "Tube porteur"],
        "Réchauffeur HT": ["Branches sortie", "Collecteur entrée", "Collecteur sortie"]
    }
    
    print(f"\n{Fore.YELLOW}Sous-composants disponibles pour {selected_component}:{Style.RESET_ALL}")
    subs = subcomponents[selected_component]
    for i, sub in enumerate(subs, 1):
        print(f"{i}. {sub}")
    
    while True:
        try:
            choice = int(input(f"\nSélectionnez un sous-composant (1-{len(subs)}): "))
            if 1 <= choice <= len(subs):
                selected_subcomponent = subs[choice-1]
                break
            else:
                print(f"{Fore.RED}Choix invalide, veuillez réessayer.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
    
    # Génération de la gamme de maintenance
    print(f"\n{Fore.CYAN}Génération de la gamme de maintenance pour {selected_component} - {selected_subcomponent}...{Style.RESET_ALL}")
    
    try:
        # Chargement des données AMDEC pour le calcul de criticité
        amdec_file = os.path.join(current_dir, 'data', 'models', 'amdec_generated.xlsx')
        if not os.path.exists(amdec_file):
            amdec_file = os.path.join(current_dir, 'data', 'models', 'amdec_template.xlsx')
        
        amdec_df = pd.read_excel(amdec_file)
        
        # Création de la gamme de maintenance
        planner = MaintenancePlanner(amdec_df)
        criticality = planner.get_criticality(selected_component, selected_subcomponent)
        
        print(f"\n{Fore.YELLOW}Criticité calculée: {criticality}{Style.RESET_ALL}")
        
        planner.generate_maintenance_plan(selected_component, selected_subcomponent, criticality)
        planner.save_to_file()
        
        print(f"\n{Fore.GREEN}Gamme de maintenance générée avec succès! Fichier sauvegardé dans data/maintenance/{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la génération de la gamme de maintenance: {str(e)}{Style.RESET_ALL}")
    
    input("\nAppuyez sur Entrée pour revenir au menu principal...")
    main_menu()

def launch_chatbot():
    print_header()
    print(f"\n{Fore.GREEN}CHATBOT AMDEC{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Posez des questions sur les composants, défaillances, et procédures de maintenance.")
    print(f"Tapez 'exit' pour quitter.{Style.RESET_ALL}\n")
    
    try:
        chatbot = Chatbot()
        chatbot.start_conversation()
    except Exception as e:
        print(f"{Fore.RED}Erreur lors du lancement du chatbot: {str(e)}{Style.RESET_ALL}")
    
    main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Programme interrompu par l'utilisateur.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Une erreur inattendue s'est produite: {str(e)}{Style.RESET_ALL}")