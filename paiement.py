import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry  # Importer DateEntry
from datetime import datetime


def connecter_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="immo"
    )


def recuperer_paiements():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.id_paiement, b.id_bail, b.cond_special, b.date_debut, b.date_fin, 
                   CONCAT(l.nom, ' ', l.prenom) AS nom_locataire,
                   p.montant, p.date_paiement, p.mode, p.commentaire
            FROM paiement p
            JOIN bail b ON p.id_bail = b.id_bail
            JOIN locataire l ON b.id_locataire = l.id_locataire
        """)
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des paiements: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def recuperer_bail_details(id_bail):
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT cond_special, date_debut, date_fin 
            FROM bail 
            WHERE id_bail = %s
        """, (id_bail,))
        return cursor.fetchone()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des détails du bail: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def recuperer_baux():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT b.id_bail, CONCAT(l.nom, ' ', l.prenom) AS nom_locataire
            FROM bail b
            JOIN locataire l ON b.id_locataire = l.id_locataire
        """)
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des baux: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def afficher_paiements(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    bouton_ajouter_paiement = tk.Button(frame, text="Ajouter Paiement", command=lambda: afficher_formulaire_ajout_paiement(frame))
    bouton_ajouter_paiement.pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_paiements = tk.Frame(canvas, bg='white')

    frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    canvas.create_window((0, 0), window=frame_paiements, anchor="nw")
    frame_paiements.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    paiements = recuperer_paiements()

    headers = ["ID", "Bail", "Nom Locataire", "Montant", "Date Paiement", "Mode", "Commentaire", "Modifier", "Supprimer"]
    for idx, header in enumerate(headers):
        tk.Label(frame_paiements, text=header, bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=idx, padx=10, pady=5)

    for i, paiement in enumerate(paiements):
        # Combinez les informations du bail
        bail_info = f"Bail ID: {paiement[1]}\nConditions: {paiement[2]}\nDébut: {paiement[3]}\nFin: {paiement[4]}"
        tk.Label(frame_paiements, text=bail_info, bg='white', justify='left').grid(row=i + 1, column=1, padx=10, pady=5)

        # Affichage des autres colonnes
        tk.Label(frame_paiements, text=paiement[0], bg='white').grid(row=i + 1, column=0, padx=10, pady=5)  # ID
        tk.Label(frame_paiements, text=paiement[5], bg='white').grid(row=i + 1, column=2, padx=10, pady=5)  # Nom Locataire
        tk.Label(frame_paiements, text=paiement[6], bg='white').grid(row=i + 1, column=3, padx=10, pady=5)  # Montant
        tk.Label(frame_paiements, text=paiement[7], bg='white').grid(row=i + 1, column=4, padx=10, pady=5)  # Date Paiement
        tk.Label(frame_paiements, text=paiement[8], bg='white').grid(row=i + 1, column=5, padx=10, pady=5)  # Mode
        tk.Label(frame_paiements, text=paiement[9], bg='white').grid(row=i + 1, column=6, padx=10, pady=5)  # Commentaire

        bouton_modifier = tk.Button(frame_paiements, text="Modifier",
                                    command=lambda id_p=paiement[0]: modifier_paiement(id_p, frame))
        bouton_modifier.grid(row=i + 1, column=len(headers) - 2, padx=5, pady=5)

        bouton_supprimer = tk.Button(frame_paiements, text="Supprimer",
                                     command=lambda id_p=paiement[0]: supprimer_paiement(id_p, frame))
        bouton_supprimer.grid(row=i + 1, column=len(headers) - 1, padx=5, pady=5)



def afficher_details_bail(selected_id, lbl_cond_special, lbl_date_debut, lbl_date_fin):
    details = recuperer_bail_details(selected_id)
    if details:
        lbl_cond_special.config(text=details[0])  # Conditions spéciales
        lbl_date_debut.config(text=details[1])     # Date de début
        lbl_date_fin.config(text=details[2])       # Date de fin

def afficher_formulaire_ajout_paiement(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Bail", "Montant", "Date Paiement", "Mode", "Commentaire"]
    entries = {}

    # Récupération des baux pour le menu déroulant
    baux = recuperer_baux()

    for idx, text in enumerate(labels):
        tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if "Bail" in text:
            entry = tk.StringVar()
            option_menu = tk.OptionMenu(form_frame, entry, *(f"{bail[1]} (ID: {bail[0]})" for bail in baux),
                command=lambda selected: afficher_details_bail(selected.split(" (ID: ")[-1][:-1], lbl_cond_special, lbl_date_debut, lbl_date_fin))

            option_menu.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        elif "Date Paiement" in text:
            # Utiliser DateEntry pour la sélection de la date
            date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            date_entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = date_entry
        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry

    # Labels pour afficher les détails du bail
    tk.Label(form_frame, text="Conditions Spéciales:", bg='white').grid(row=len(labels), column=0, padx=10, pady=5)
    lbl_cond_special = tk.Label(form_frame, text="", bg='white')
    lbl_cond_special.grid(row=len(labels), column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Date Début:", bg='white').grid(row=len(labels)+1, column=0, padx=10, pady=5)
    lbl_date_debut = tk.Label(form_frame, text="", bg='white')
    lbl_date_debut.grid(row=len(labels)+1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Date Fin:", bg='white').grid(row=len(labels)+2, column=0, padx=10, pady=5)
    lbl_date_fin = tk.Label(form_frame, text="", bg='white')
    lbl_date_fin.grid(row=len(labels)+2, column=1, padx=10, pady=5)

    def ajouter_paiement():
        values = {key: entry.get() for key, entry in entries.items()}

        if not all(values.values()):
            messagebox.showwarning("Validation", "Tous les champs doivent être remplis.")
            return

        try:
            connection = connecter_bd()
            cursor = connection.cursor()
            query = """INSERT INTO paiement (id_bail, montant, date_paiement, mode, commentaire)
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                values["Bail"].split(" (ID: ")[-1][:-1],  # Récupérer l'ID à partir de la sélection
                values["Montant"],
                values["Date Paiement"],  # Utiliser la date sélectionnée du DateEntry
                values["Mode"],
                values["Commentaire"]
            ))
            connection.commit()
            messagebox.showinfo("Succès", "Paiement ajouté avec succès")
            afficher_paiements(frame)  # Réafficher la liste des paiements
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du paiement: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    bouton_ajouter = tk.Button(form_frame, text="Ajouter", command=ajouter_paiement, bg='green', fg='white')
    bouton_ajouter.grid(row=len(labels)+3, column=1, pady=10)

def modifier_paiement(id_paiement, frame):
    for widget in frame.winfo_children():
        widget.destroy()  # Efface les widgets existants dans le cadre

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Bail", "Montant", "Date Paiement", "Mode", "Commentaire"]
    entries = {}

    # Récupération des informations actuelles du paiement
    connection = connecter_bd()
    cursor = connection.cursor()

    try:
        query = """SELECT id_bail, montant, date_paiement, mode, commentaire FROM paiement WHERE id_paiement = %s"""
        cursor.execute(query, (id_paiement,))
        paiement_info = cursor.fetchone()

        for idx, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
            if "Bail" in text:
                bail_var = tk.StringVar()
                # Récupérer les baux pour le menu déroulant
                baux = recuperer_baux()
                option_menu = tk.OptionMenu(form_frame, bail_var, *(f"{bail[1]} (ID: {bail[0]})" for bail in baux))
                option_menu.grid(row=idx, column=1, padx=10, pady=5)
                bail_var.set(f"{paiement_info[0]} (ID: {paiement_info[0]})")  # Définir la valeur par défaut
                entries[text] = bail_var

                # Lier l'affichage des détails au changement de sélection
                bail_var.trace("w", lambda *args: afficher_details_bail(bail_var.get().split(" (ID: ")[-1][:-1]))

            elif "Date Paiement" in text:
                date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                date_entry.grid(row=idx, column=1, padx=10, pady=5)
                date_entry.set_date(paiement_info[2])  # Définir la date par défaut
                entries[text] = date_entry
            else:
                entry = tk.Entry(form_frame)
                entry.insert(0, paiement_info[idx])
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry

        # Labels pour afficher les détails du bail
        tk.Label(form_frame, text="Conditions Spéciales:", bg='white').grid(row=len(labels), column=0, padx=10, pady=5)
        lbl_cond_special = tk.Label(form_frame, text="", bg='white')
        lbl_cond_special.grid(row=len(labels), column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Date Début:", bg='white').grid(row=len(labels)+1, column=0, padx=10, pady=5)
        lbl_date_debut = tk.Label(form_frame, text="", bg='white')
        lbl_date_debut.grid(row=len(labels)+1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Date Fin:", bg='white').grid(row=len(labels)+2, column=0, padx=10, pady=5)
        lbl_date_fin = tk.Label(form_frame, text="", bg='white')
        lbl_date_fin.grid(row=len(labels)+2, column=1, padx=10, pady=5)

        # Fonction pour afficher les détails du bail
        def afficher_details_bail(selected_id):
            details = recuperer_bail_details(selected_id)
            if details:
                lbl_cond_special.config(text=details[0])  # Conditions spéciales
                lbl_date_debut.config(text=details[1])     # Date de début
                lbl_date_fin.config(text=details[2])       # Date de fin

        def enregistrer_modifications():
            try:
                connection = connecter_bd()
                cursor = connection.cursor()
                query = """UPDATE paiement 
                           SET id_bail = %s, montant = %s, date_paiement = %s, mode = %s, commentaire = %s
                           WHERE id_paiement = %s"""
                values = (entries["Bail"].get().split(" (ID: ")[-1][:-1], entries["Montant"].get(),
                          entries["Date Paiement"].get(),  # Utiliser la date sélectionnée du DateEntry
                          entries["Mode"].get(), entries["Commentaire"].get(), id_paiement)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Paiement modifié avec succès")
                afficher_paiements(frame)  # Réafficher la liste des paiements
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification du paiement : {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        bouton_enregistrer = tk.Button(form_frame, text="Enregistrer", command=enregistrer_modifications, bg='green', fg='white')
        bouton_enregistrer.grid(row=len(labels)+4, column=1, pady=10)  # Ajustez la ligne pour éviter le chevauchement

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations du paiement : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def supprimer_paiement(id_paiement, frame):
    if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce paiement ?"):
        try:
            connection = connecter_bd()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM paiement WHERE id_paiement = %s", (id_paiement,))
            connection.commit()
            messagebox.showinfo("Succès", "Paiement supprimé avec succès")
            afficher_paiements(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du paiement: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
