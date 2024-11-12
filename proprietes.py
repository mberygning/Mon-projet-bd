import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
from datetime import datetime

def connecter_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="immo"
    )

def afficher_proprietes(frame):
    for widget in frame.winfo_children():
        widget.destroy()




    bouton_ajouter_propriete = tk.Button(frame, text="Ajouter Propriété", command=lambda: afficher_formulaire_ajout(frame))
    bouton_ajouter_propriete.pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_proprietes = tk.Frame(canvas, bg='white')

    frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    canvas.create_window((0, 0), window=frame_proprietes, anchor="nw")
    frame_proprietes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT id_propriete, nom_propiete, adresse_propriete, nombres_chambres, nombre_de_cantine, nb_salle_bain, superficie, date_dacquisition, prix_louer, prix_achat, type FROM propriete")
        resultats = cursor.fetchall()

        headers = ["ID", "Nom", "Adresse", "Chambres", "Cantines", "Salles de Bain", "Superficie", "Date d'Acquisition", "Prix de Location", "Prix d'Achat", "Type", "Modifier", "Supprimer"]
        for idx, header in enumerate(headers):
            tk.Label(frame_proprietes, text=header, bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=idx, padx=10, pady=5)

        for i, propriete in enumerate(resultats):
            for j, value in enumerate(propriete):
                tk.Label(frame_proprietes, text=value, bg='white').grid(row=i + 1, column=j, padx=10, pady=5)

            bouton_modifier = tk.Button(frame_proprietes, text="Modifier", command=lambda id_p=propriete[0]: modifier_propriete(id_p, frame))
            bouton_modifier.grid(row=i + 1, column=len(headers) - 2, padx=5, pady=5)

            bouton_supprimer = tk.Button(frame_proprietes, text="Supprimer", command=lambda id_p=propriete[0]: supprimer_propriete(id_p, frame))
            bouton_supprimer.grid(row=i + 1, column=len(headers) - 1, padx=5, pady=5)


    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des propriétés: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
from tkcalendar import DateEntry  # Ajoute cette ligne en haut de ton fichier

def afficher_formulaire_ajout(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    # Charger et afficher l'image de fond
    image_fond = Image.open("hotel2.jpg")
    photo_fond = ImageTk.PhotoImage(image_fond)
    label_fond = tk.Label(frame, image=photo_fond)
    label_fond.image = photo_fond
    label_fond.place(x=0, y=0, relwidth=1, relheight=1)

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Nom", "Adresse", "Nombre de Chambres", "Nombre de Cantine", "Nombre de Salles de Bain", "Superficie", "Date d'Acquisition", "Prix de Location", "Prix d'Achat", "Type"]
    entries = {}

    for idx, text in enumerate(labels):
        tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if text == "Date d'Acquisition":
            entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
            entry.grid(row=idx, column=1, padx=10, pady=5)
        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[text] = entry

    def ajouter():
        values = {key: entry.get() for key, entry in entries.items()}

        # Vérification des champs
        if not all(values.values()):
            messagebox.showwarning("Validation", "Tous les champs doivent être remplis.")
            return

        try:
            # Conversion des valeurs numériques...

            # Récupérer et convertir la date d'acquisition
            date_acquisition = values["Date d'Acquisition"]
            date_acquisition = datetime.strptime(date_acquisition, "%m/%d/%y").date()

            connection = connecter_bd()
            cursor = connection.cursor()
            query = """INSERT INTO propriete (nom_propiete, adresse_propriete, nombres_chambres, nombre_de_cantine, nb_salle_bain, superficie, date_dacquisition, prix_louer, prix_achat, type)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
            values["Nom"], values["Adresse"], values["Nombre de Chambres"], values["Nombre de Cantine"],
            values["Nombre de Salles de Bain"], values["Superficie"], date_acquisition, values["Prix de Location"],
            values["Prix d'Achat"], values["Type"]))
            connection.commit()
            messagebox.showinfo("Succès", "Propriété ajoutée avec succès")
            afficher_proprietes(frame)
        except ValueError as ve:
            messagebox.showwarning("Validation", str(ve))
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de la propriété: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    bouton_ajouter = tk.Button(form_frame, text="Ajouter", command=ajouter, bg='green', fg='white')
    bouton_ajouter.grid(row=len(labels), column=1, pady=10)

    # Ajouter un bouton retour
    bouton_retour = tk.Button(form_frame, text="Retour", command=lambda: afficher_proprietes(frame))
    bouton_retour.grid(row=len(labels) + 1, column=1, pady=10)


def modifier_propriete(id_propriete, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    # Charger et afficher l'image de fond
    image_fond = Image.open("hotel3.jpg")  # Assure-toi que le chemin est correct
    photo_fond = ImageTk.PhotoImage(image_fond)
    label_fond = tk.Label(frame, image=photo_fond)
    label_fond.image = photo_fond  # Garder une référence à l'image
    label_fond.place(x=0, y=0, relwidth=1, relheight=1)

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT nom_propiete, adresse_propriete, nombres_chambres, nombre_de_cantine, nb_salle_bain, superficie, date_dacquisition, prix_louer, prix_achat, type FROM propriete WHERE id_propriete = %s", (id_propriete,))
        propriete_info = cursor.fetchone()

        labels = ["Nom", "Adresse", "Nombre de Chambres", "Nombre de Cantine", "Nombre de Salles de Bain", "Superficie", "Date d'Acquisition", "Prix de Location", "Prix d'Achat", "Type"]
        entries = {}

        for idx, text in enumerate(labels):
            tk.Label(frame, text=text).grid(row=idx, column=0, padx=10, pady=5)
            if text == "Date d'Acquisition":
                entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.set_date(propriete_info[idx])  # Définit la date par défaut
            else:
                entry = tk.Entry(frame)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.insert(0, propriete_info[idx])
            entries[text] = entry

        def enregistrer_modifications():
            values = {key: entry.get() for key, entry in entries.items()}

            try:
                connection = connecter_bd()
                cursor = connection.cursor()

                # Récupérer et convertir la date d'acquisition
                date_acquisition = values["Date d'Acquisition"]
                date_acquisition = datetime.strptime(date_acquisition, "%m/%d/%y").date()

                query = """UPDATE propriete 
                           SET nom_propiete = %s, adresse_propriete = %s, nombres_chambres = %s, nombre_de_cantine = %s, nb_salle_bain = %s, superficie = %s, date_dacquisition = %s, prix_louer = %s, prix_achat = %s, type = %s 
                           WHERE id_propriete = %s"""
                cursor.execute(query, (
                values["Nom"], values["Adresse"], values["Nombre de Chambres"], values["Nombre de Cantine"],
                values["Nombre de Salles de Bain"], values["Superficie"], date_acquisition, values["Prix de Location"],
                values["Prix d'Achat"], values["Type"], id_propriete))
                connection.commit()
                messagebox.showinfo("Succès", "Propriété modifiée avec succès")
                afficher_proprietes(frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        bouton_enregistrer = tk.Button(frame, text="Enregistrer", command=enregistrer_modifications)
        bouton_enregistrer.grid(row=len(labels), column=1, padx=10, pady=10)

        # Ajouter un bouton retour
        bouton_retour = tk.Button(form_frame, text="Retour", command=lambda: afficher_proprietes(frame))
        bouton_retour.grid(row=len(labels) + 1, column=1, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations: {e}")

def supprimer_propriete(id_propriete, frame):
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette propriété ?"):
        return

    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        query = "DELETE FROM propriete WHERE id_propriete = %s"
        cursor.execute(query, (id_propriete,))
        connection.commit()
        messagebox.showinfo("Succès", "Propriété supprimée avec succès")
        afficher_proprietes(frame)
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


