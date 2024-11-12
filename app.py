import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt
import utilisateur  # Module pour gérer les utilisateurs
import proprietes
import bail
import paiement
import locataire
import entretien
class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentification")
        self.root.geometry("800x600")

        # Créer un Canvas pour l'image de fond
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Charger et afficher l'image de fond
        self.image_bg = Image.open("hotel.jpg")
        self.image_bg = self.image_bg.resize((800, 600), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.image_bg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Créer un frame pour le formulaire
        self.form_frame = tk.Frame(root, bg='white', padx=20, pady=20)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Labels et Champs
        tk.Label(self.form_frame, text="Email", bg='white').grid(row=0, column=0)
        tk.Label(self.form_frame, text="Mot de passe", bg='white').grid(row=1, column=0)

        self.email_entry = tk.Entry(self.form_frame)
        self.email_entry.grid(row=0, column=1)

        self.password_entry = tk.Entry(self.form_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        bouton_connexion = tk.Button(self.form_frame, text="Se connecter", command=self.verifier_identifiants)
        bouton_connexion.grid(row=2, columnspan=2, pady=10)

        self.statistiques = self.recuperer_statistiques()

    def connecter_bd(self):
        """ Fonction pour se connecter à la base de données """
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="immo"
        )

    def recuperer_statistiques(self):
        """ Fonction pour récupérer les statistiques de la base de données """
        nb_propriete = 0
        nb_utilisateurs = 0
        try:
            connection = self.connecter_bd()
            cursor = connection.cursor()

            # Compter les propriétés
            cursor.execute("SELECT COUNT(*) FROM propriete")
            nb_propriete = cursor.fetchone()[0]

            # Compter les utilisateurs
            cursor.execute("SELECT COUNT(*) FROM utilisateur")
            nb_utilisateurs = cursor.fetchone()[0]

        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des statistiques: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return nb_propriete, nb_utilisateurs

    def verifier_identifiants(self):
        """ Fonction pour vérifier les identifiants de l'utilisateur ou locataire """
        email = self.email_entry.get()
        mot_de_passe = self.password_entry.get()

        try:
            connection = self.connecter_bd()
            cursor = connection.cursor()

            # Vérification dans la table utilisateur
            query = "SELECT mot_de_passe FROM utilisateur WHERE email = %s"
            cursor.execute(query, (email,))
            resultat = cursor.fetchone()

            if resultat and bcrypt.checkpw(mot_de_passe.encode('utf-8'), resultat[0].encode('utf-8')):
                messagebox.showinfo("Succès", "Connexion réussie en tant qu'utilisateur !")
                self.root.destroy()
                self.creer_fenetre_principale("utilisateur")
                return

            # Vérification dans la table locataire
            query = "SELECT mot_de_passe_loc FROM locataire WHERE email = %s"
            cursor.execute(query, (email,))
            resultat = cursor.fetchone()

            if resultat and bcrypt.checkpw(mot_de_passe.encode('utf-8'), resultat[0].encode('utf-8')):
                messagebox.showinfo("Succès", "Connexion réussie en tant que locataire !")
                self.root.destroy()
                self.creer_fenetre_principale("locataire")
                return

            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")

        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de la connexion à la base de données: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def creer_fenetre_principale(self, role):
        """ Crée la fenêtre principale après connexion """
        self.main_window = tk.Tk()
        self.main_window.title("Gestion Immobilière")
        self.main_window.geometry("800x600")

        # Créer un cadre principal
        self.cadre_principal = tk.Frame(self.main_window, bg='white')
        self.cadre_principal.pack(fill='both', expand=True)

        # Afficher les statistiques
        tk.Label(self.cadre_principal, text=f"Propriétés: {self.statistiques[0]}", bg='white').pack(pady=10)
        tk.Label(self.cadre_principal, text=f"Utilisateurs: {self.statistiques[1]}", bg='white').pack(pady=10)

        # Créer des boutons dans le cadre principal
        self.create_main_buttons()

        self.main_window.mainloop()

    def create_main_buttons(self):
        frame_boutons = tk.Frame(self.cadre_principal, bg='white', padx=20, pady=20)
        frame_boutons.place(x=20, y=100, anchor='nw')

        tk.Button(frame_boutons, text="Gérer Propriété", command=self.afficher_proprietes).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Gérer Personnel", command=self.afficher_utilisateurs).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Les Locataires", command=self.afficher_locataires).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Propriétés en maintenance", command=self.afficher_entretien).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Gestion des baux", command=self.afficher_baux).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Suivi des Paiements", command=self.afficher_paiements).pack(pady=5, fill='x')
        tk.Button(frame_boutons, text="Déconnexion", command=self.main_window.destroy).pack(pady=5, fill='x')

    #def afficher_proprietes(self):
        #self.cadre_principal.pack_forget()  # Masquer le cadre principal
        #self.proprietes_frame = tk.Frame(self.main_window, bg='white')
        #self.proprietes_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des propriétés
        #proprietes.afficher_proprietes(self.proprietes_frame)

        # Bouton retour
        #tk.Button(self.proprietes_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_proprietes(self):
        self.cadre_principal.pack_forget()  # Masquer le cadre principal
        self.proprietes_frame = tk.Frame(self.main_window, bg='white')
        self.proprietes_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des propriétés
        proprietes.afficher_proprietes(self.proprietes_frame)

        # Bouton pour ajouter une propriété
        #tk.Button(self.proprietes_frame, text="Ajouter Propriété", command=self.ajouter_propriete).pack(pady=10)


        # Bouton retour
        tk.Button(self.proprietes_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def ajouter_propriete(self):
        # Appelle la fonction d'ajout de propriété dans le module proprietes
        proprietes.afficher_formulaire_ajout(self.proprietes_frame)
    def modifier_propriete(self):
        self.cadre_principal.pack_forget()  # Masquer le cadre principal
        self.modification_frame = tk.Frame(self.main_window, bg='white')
        self.modification_frame.pack(fill='both', expand=True)

        # Appel de la fonction de modification des propriétés depuis le module proprietes
        proprietes.afficher_formulaire_modification(self.modification_frame)  # Assure-toi que cette fonction existe

        # Bouton retour
        tk.Button(self.modification_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_utilisateurs(self):
        self.cadre_principal.pack_forget()
        self.utilisateurs_frame = tk.Frame(self.main_window, bg='white')
        self.utilisateurs_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des utilisateurs
        utilisateur.afficher_utilisateurs(self.utilisateurs_frame)

        # Bouton retour
        tk.Button(self.utilisateurs_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_entretien(self):
        self.cadre_principal.pack_forget()
        self.entretien_frame = tk.Frame(self.main_window, bg='white')
        self.entretien_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des utilisateurs
        entretien.afficher_entretien(self.entretien_frame)

        # Bouton retour
        tk.Button(self.entretien_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_locataires(self):
        self.cadre_principal.pack_forget()
        self.locataires_frame = tk.Frame(self.main_window, bg='white')
        self.locataires_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des locataires
        locataire.afficher_locataires(self.locataires_frame)

        # Bouton retour
        tk.Button(self.locataires_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_baux(self):
        self.cadre_principal.pack_forget()
        self.bail_frame = tk.Frame(self.main_window, bg='white')
        self.bail_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des baux
        bail.afficher_baux(self.bail_frame)

        # Bouton retour
        tk.Button(self.bail_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_paiements(self):
        self.cadre_principal.pack_forget()
        self.paiement_frame = tk.Frame(self.main_window, bg='white')
        self.paiement_frame.pack(fill='both', expand=True)

        # Appel de la fonction d'affichage des paiements
        paiement.afficher_paiements(self.paiement_frame)

        # Bouton retour
        tk.Button(self.paiement_frame, text="Retour", command=self.afficher_cadre_principal).pack(pady=10)

    def afficher_cadre_principal(self):
        # Masquer tous les autres cadres
        for frame in (getattr(self, 'proprietes_frame', None),
                      getattr(self, 'utilisateurs_frame', None),
                      getattr(self, 'locataires_frame', None),
                      getattr(self, 'entretien_frame', None),

                      getattr(self, 'bail_frame', None),
                      getattr(self, 'paiement_frame', None)):
            if frame is not None:
                frame.pack_forget()

        # Montrer le cadre principal
        self.cadre_principal.pack(fill='both', expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()
