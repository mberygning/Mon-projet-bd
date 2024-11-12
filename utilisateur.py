import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt
import re


def connecter_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="immo"
    )


def afficher_utilisateurs(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    bouton_ajouter_utilisateur = tk.Button(frame, text="Ajouter Utilisateur", command=lambda: afficher_formulaire_ajout(frame))
    bouton_ajouter_utilisateur.pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_utilisateurs = tk.Frame(canvas, bg='white')

    frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    canvas.create_window((0, 0), window=frame_utilisateurs, anchor="nw")
    frame_utilisateurs.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT id_utilisateur, nom_utilisateur, prenom_utilisateur, email, role FROM utilisateur")
        resultats = cursor.fetchall()

        tk.Label(frame_utilisateurs, text="ID", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Nom", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Prénom", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Email", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=3, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Role", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=4, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Modifier", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=5, padx=10, pady=5)
        tk.Label(frame_utilisateurs, text="Supprimer", bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=6, padx=10, pady=5)

        for i, utilisateur in enumerate(resultats):
            id_utilisateur = utilisateur[0]
            tk.Label(frame_utilisateurs, text=id_utilisateur, bg='white').grid(row=i + 1, column=0, padx=10, pady=5)
            tk.Label(frame_utilisateurs, text=utilisateur[1], bg='white').grid(row=i + 1, column=1, padx=10, pady=5)
            tk.Label(frame_utilisateurs, text=utilisateur[2], bg='white').grid(row=i + 1, column=2, padx=10, pady=5)
            tk.Label(frame_utilisateurs, text=utilisateur[3], bg='white').grid(row=i + 1, column=3, padx=10, pady=5)
            tk.Label(frame_utilisateurs, text=utilisateur[4], bg='white').grid(row=i + 1, column=4, padx=10, pady=5)

            bouton_modifier = tk.Button(frame_utilisateurs, text="Modifier", command=lambda id_u=id_utilisateur: modifier_utilisateur(id_u, frame))
            bouton_modifier.grid(row=i + 1, column=5, padx=5, pady=5)

            bouton_supprimer = tk.Button(frame_utilisateurs, text="Supprimer", command=lambda id_u=id_utilisateur: supprimer_utilisateur(id_u, frame))
            bouton_supprimer.grid(row=i + 1, column=6, padx=5, pady=5)


    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des utilisateurs: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def afficher_formulaire_ajout(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # Créer le formulaire d'ajout d'utilisateur
    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels_texts = ["Nom", "Prénom", "Email", "Mot de passe", "Role"]
    entries = {}

    for idx, text in enumerate(labels_texts):
        tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if text == "Role":
            role_var = tk.StringVar()
            role_var.set("Administrateur")
            role_menu = tk.OptionMenu(form_frame, role_var,
                                      "Administrateur",
                                      "Gestionnaire de Propriétés",
                                      "Comptable",
                                      "Agent Immobilier",
                                      "Technicien d'Entretien")
            role_menu.grid(row=idx, column=1, padx=10, pady=5)
            entries["Role"] = role_var
        elif text == "Mot de passe":
            entry = tk.Entry(form_frame, show="*")
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry

    def ajouter():
        mot_de_passe = entries["Mot de passe"].get()
        nom_utilisateur = entries["Nom"].get()
        prenom_utilisateur = entries["Prénom"].get()
        email = entries["Email"].get()
        role = entries["Role"].get()

        if not nom_utilisateur or not prenom_utilisateur or not email or not mot_de_passe:
            messagebox.showwarning("Validation", "Tous les champs doivent être remplis.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validation", "L'adresse email est invalide.")
            return

        if len(mot_de_passe) < 8:
            messagebox.showwarning("Validation", "Le mot de passe doit comporter au moins 8 caractères.")
            return

        mot_de_passe_hache = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        ajouter_utilisateur(nom_utilisateur, prenom_utilisateur, email, mot_de_passe_hache, role, form_frame)

    bouton_ajouter = tk.Button(form_frame, text="Ajouter", command=ajouter, bg='green', fg='white')
    bouton_ajouter.grid(row=len(labels_texts), column=1, pady=10)


def ajouter_utilisateur(nom_utilisateur, prenom_utilisateur, email, mot_de_passe, role, fenetre):
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        query_check_email = "SELECT COUNT(*) FROM utilisateur WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        email_exists = cursor.fetchone()[0] > 0

        if email_exists:
            messagebox.showwarning("Validation", "L'adresse email est déjà utilisée.")
            return

        query = """INSERT INTO utilisateur (nom_utilisateur, prenom_utilisateur, email, mot_de_passe, role) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (nom_utilisateur, prenom_utilisateur, email, mot_de_passe, role)
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Succès", "Utilisateur ajouté avec succès")
        afficher_utilisateurs(fenetre)
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'utilisateur: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def modifier_utilisateur(id_utilisateur, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT nom_utilisateur, prenom_utilisateur, email, role FROM utilisateur WHERE id_utilisateur = %s", (id_utilisateur,))
        utilisateur_info = cursor.fetchone()

        tk.Label(frame, text="Nom").grid(row=0, column=0, padx=10, pady=5)
        entry_nom = tk.Entry(frame)
        entry_nom.grid(row=0, column=1, padx=10, pady=5)
        entry_nom.insert(0, utilisateur_info[0])

        tk.Label(frame, text="Prénom").grid(row=1, column=0, padx=10, pady=5)
        entry_prenom = tk.Entry(frame)
        entry_prenom.grid(row=1, column=1, padx=10, pady=5)
        entry_prenom.insert(0, utilisateur_info[1])

        tk.Label(frame, text="Email").grid(row=2, column=0, padx=10, pady=5)
        entry_email = tk.Entry(frame)
        entry_email.grid(row=2, column=1, padx=10, pady=5)
        entry_email.insert(0, utilisateur_info[2])

        tk.Label(frame, text="Role").grid(row=3, column=0, padx=10, pady=5)
        var_role = tk.StringVar(value=utilisateur_info[3])
        role_menu = tk.OptionMenu(frame, var_role,
                                  "Administrateur",
                                  "Gestionnaire de Propriétés",
                                  "Comptable",
                                  "Agent Immobilier",
                                  "Technicien d'Entretien")
        role_menu.grid(row=3, column=1, padx=10, pady=5)

        def enregistrer_modifications():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            email = entry_email.get()
            role = var_role.get()
            try:
                connection = connecter_bd()
                cursor = connection.cursor()
                query = """UPDATE utilisateur 
                           SET nom_utilisateur = %s, prenom_utilisateur = %s, email = %s, role = %s 
                           WHERE id_utilisateur = %s"""
                values = (nom, prenom, email, role, id_utilisateur)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Utilisateur modifié avec succès")
                afficher_utilisateurs(frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        bouton_enregistrer = tk.Button(frame, text="Enregistrer", command=enregistrer_modifications)
        bouton_enregistrer.grid(row=4, column=1, padx=10, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations: {e}")


def supprimer_utilisateur(id_utilisateur, frame):
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet utilisateur ?"):
        return

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        query = "DELETE FROM utilisateur WHERE id_utilisateur = %s"
        cursor.execute(query, (id_utilisateur,))
        connection.commit()
        messagebox.showinfo("Succès", "Utilisateur supprimé avec succès")
        afficher_utilisateurs(frame)
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


