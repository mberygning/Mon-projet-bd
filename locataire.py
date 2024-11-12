import tkinter as tk
from tkinter import messagebox, Frame, Label, Entry, Button
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import bcrypt

def connecter_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="immo"
    )

def afficher_locataires(frame):
    for widget in frame.winfo_children():
        widget.destroy()


    Button(frame, text="Ajouter Locataire", command=lambda: afficher_formulaire_ajout(frame)).pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_utilisateurs = Frame(canvas, bg='white')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.create_window((0, 0), window=frame_utilisateurs, anchor="nw")

    frame_utilisateurs.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set)

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT id_locataire, nom, prenom, adresse, email, date_naissance, telephone, profession FROM locataire")
        resultats = cursor.fetchall()

        entetes = ["ID", "Nom", "Prénom", "Adresse", "Email", "Date de Naissance", "Téléphone", "Profession", "Modifier", "Supprimer"]
        for i, titre in enumerate(entetes):
            Label(frame_utilisateurs, text=titre, bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=i, padx=10, pady=5)

        for i, locataire in enumerate(resultats):
            for j in range(len(locataire)):
                Label(frame_utilisateurs, text=locataire[j], bg='white').grid(row=i + 1, column=j, padx=10, pady=5)

            Button(frame_utilisateurs, text="Modifier", command=lambda id_l=locataire[0]: modifier_locataire(id_l, frame)).grid(row=i + 1, column=len(locataire), padx=5, pady=5)
            Button(frame_utilisateurs, text="Supprimer", command=lambda id_l=locataire[0]: supprimer_locataire(id_l, frame)).grid(row=i + 1, column=len(locataire) + 1, padx=5, pady=5)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des locataires: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def afficher_formulaire_ajout(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    form_frame = Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels_texts = ["Nom", "Prénom", "Adresse", "Email", "Date de Naissance", "Téléphone", "Profession", "Mot de Passe"]
    entries = {}

    for idx, text in enumerate(labels_texts):
        Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if text == "Date de Naissance":
            date_entry = DateEntry(form_frame, date_pattern='yyyy/mm/dd', width=12, background='darkblue', foreground='white', borderwidth=2)
            date_entry.grid(row=idx, column=1, padx=10, pady=5)
            entries["Date de Naissance"] = date_entry
        elif text == "Mot de Passe":
            entry = Entry(form_frame, show="*")
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        else:
            entry = Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry

    Button(form_frame, text="Ajouter", command=lambda: ajouter_locataire(
        entries["Nom"].get(),
        entries["Prénom"].get(),
        entries["Adresse"].get(),
        entries["Email"].get(),
        entries["Date de Naissance"].get(),
        entries["Téléphone"].get(),
        entries["Profession"].get(),
        entries["Mot de Passe"].get(),
        frame
    ), bg='green', fg='white').grid(row=len(labels_texts), column=1, pady=10)

def ajouter_locataire(nom, prenom, adresse, email, date_naissance, telephone, profession, mot_de_passe_loc, frame):
    try:
        datetime.strptime(date_naissance, '%Y/%m/%d')
        connection = connecter_bd()
        cursor = connection.cursor()
        mot_de_passe_hache = bcrypt.hashpw(mot_de_passe_loc.encode('utf-8'), bcrypt.gensalt())

        query = """INSERT INTO locataire (nom, prenom, adresse, email, date_naissance, telephone, profession, mot_de_passe_loc) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (nom, prenom, adresse, email, date_naissance, telephone, profession, mot_de_passe_hache)

        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Succès", "Locataire ajouté avec succès")
        afficher_locataires(frame)
    except ValueError:
        messagebox.showwarning("Validation", "La date de naissance doit être au format a/m/j (YYYY/MM/DD).")
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def modifier_locataire(id_locataire, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM locataire WHERE id_locataire = %s", (id_locataire,))
        locataire_info = cursor.fetchone()

        labels_texts = ["Nom", "Prénom", "Adresse", "Email", "Date de Naissance", "Téléphone", "Profession", "Mot de Passe"]
        entries = {}

        for idx, text in enumerate(labels_texts):
            Label(frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
            if text == "Date de Naissance":
                date_entry = DateEntry(frame, date_pattern='yyyy/mm/dd', width=12, background='darkblue', foreground='white', borderwidth=2)
                date_entry.grid(row=idx, column=1, padx=10, pady=5)
                date_entry.set_date(locataire_info[5])  # Assurez-vous que c'est la bonne colonne pour la date
                entries["Date de Naissance"] = date_entry
            elif text == "Mot de Passe":
                entry = Entry(frame, show="*")
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry
            else:
                entry = Entry(frame)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.insert(0, locataire_info[idx + 1])
                entries[text] = entry

        Button(frame, text="Enregistrer", command=lambda: enregistrer_modifications(
            id_locataire,
            entries["Nom"].get(),
            entries["Prénom"].get(),
            entries["Adresse"].get(),
            entries["Email"].get(),
            entries["Date de Naissance"].get(),
            entries["Téléphone"].get(),
            entries["Profession"].get(),
            entries["Mot de Passe"].get(),
            frame
        )).grid(row=len(labels_texts), column=1, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations: {e}")

def enregistrer_modifications(id_locataire, nom, prenom, adresse, email, date_naissance, telephone, profession, mot_de_passe_loc, frame):
    try:
        datetime.strptime(date_naissance, '%Y/%m/%d')
        connection = connecter_bd()
        cursor = connection.cursor()

        if mot_de_passe_loc:
            mot_de_passe_hache = bcrypt.hashpw(mot_de_passe_loc.encode('utf-8'), bcrypt.gensalt())
            query = """UPDATE locataire 
                       SET nom = %s, prenom = %s, adresse = %s, email = %s, date_naissance = %s, telephone = %s, profession = %s, mot_de_passe_loc = %s 
                       WHERE id_locataire = %s"""
            values = (nom, prenom, adresse, email, date_naissance, telephone, profession, mot_de_passe_hache, id_locataire)
        else:
            query = """UPDATE locataire 
                       SET nom = %s, prenom = %s, adresse = %s, email = %s, date_naissance = %s, telephone = %s, profession = %s 
                       WHERE id_locataire = %s"""
            values = (nom, prenom, adresse, email, date_naissance, telephone, profession, id_locataire)

        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Succès", "Locataire modifié avec succès")
        afficher_locataires(frame)
    except ValueError:
        messagebox.showwarning("Validation", "La date de naissance doit être au format a/m/j (YYYY/MM/DD).")
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def supprimer_locataire(id_locataire, frame):
    if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce locataire?"):
        try:
            connection = connecter_bd()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM locataire WHERE id_locataire = %s", (id_locataire,))
            connection.commit()
            messagebox.showinfo("Succès", "Locataire supprimé avec succès")
            afficher_locataires(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
