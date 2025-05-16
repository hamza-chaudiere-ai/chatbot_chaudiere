# chat/ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import sys
import threading
import time

# Ajouter le chemin du projet au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

from chat.bot import Chatbot

class ChatbotUI:
    """
    Interface utilisateur pour le chatbot AMDEC
    """
    
    def __init__(self, root):
        """
        Initialisation de l'interface
        
        Args:
            root (tk.Tk): Fenêtre racine Tkinter
        """
        self.root = root
        self.root.title("Chatbot AMDEC")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Initialiser le chatbot
        self.chatbot = Chatbot()
        
        # Créer l'interface
        self._create_widgets()
        
        # Afficher un message de bienvenue
        self._add_bot_message("Bonjour ! Je suis votre assistant pour l'analyse AMDEC et la maintenance des chaudières. Comment puis-je vous aider aujourd'hui ?")
    
    def _create_widgets(self):
        """
        Crée les widgets de l'interface
        """
        # Cadre principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone de chat
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Zone de texte pour afficher les messages
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Arial", 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Cadre pour l'entrée utilisateur
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Zone de texte pour saisir les messages
        self.input_field = ttk.Entry(input_frame, font=("Arial", 10))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self._send_message)
        
        # Bouton d'envoi
        send_button = ttk.Button(input_frame, text="Envoyer", command=self._send_message)
        send_button.pack(side=tk.RIGHT)
        
        # Placer le focus sur la zone de saisie
        self.input_field.focus_set()
    
    def _send_message(self, event=None):
        """
        Envoie le message de l'utilisateur au chatbot
        
        Args:
            event: Événement Tkinter (non utilisé)
        """
        # Récupérer le message
        message = self.input_field.get().strip()
        
        # Vérifier si le message est vide
        if not message:
            return
        
        # Afficher le message de l'utilisateur
        self._add_user_message(message)
        
        # Effacer la zone de saisie
        self.input_field.delete(0, tk.END)
        
        # Traiter le message dans un thread séparé pour ne pas bloquer l'interface
        threading.Thread(target=self._process_message, args=(message,), daemon=True).start()
    
    def _process_message(self, message):
        """
        Traite le message de l'utilisateur et génère une réponse
        
        Args:
            message (str): Message de l'utilisateur
        """
        # Vérifier si l'utilisateur souhaite quitter
        if message.lower() in ['exit', 'quit', 'q', 'bye', 'au revoir']:
            # Afficher un message d'au revoir
            self._add_bot_message("Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions.")
            
            # Attendre un peu avant de fermer l'application
            time.sleep(1.5)
            self.root.quit()
            return
        
        # Générer une réponse
        response = self.chatbot.generate_response(message)
        
        # Afficher la réponse
        self._add_bot_message(response)
    
    def _add_user_message(self, message):
        """
        Ajoute un message de l'utilisateur à l'affichage
        
        Args:
            message (str): Message à afficher
        """
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Vous : ", "user_tag")
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.tag_configure("user_tag", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _add_bot_message(self, message):
        """
        Ajoute un message du chatbot à l'affichage
        
        Args:
            message (str): Message à afficher
        """
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Assistant : ", "bot_tag")
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.tag_configure("bot_tag", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

def start_ui():
    """
    Démarre l'interface utilisateur
    """
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_ui()