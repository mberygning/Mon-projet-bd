import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
#from datetime import datetime
from tkcalendar import DateEntry
from datetime import datetime


def connecter_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="immo"
    )


def recuperer_proprietes():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT id_propriete, nom_propiete FROM propriete")
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des propriétés: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def recuperer_locataires():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT id_locataire, CONCAT(nom, ' ', prenom) AS nom_complet FROM locataire")
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des locataires: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def recuperer_baux():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT b.id_bail, p.nom_propiete, CONCAT(l.nom, ' ', l.prenom) AS nom_locataire,
                   b.date_debut, b.date_fin, b.loyer_mensuel, b.depot_garantie, 
                   b.cond_special, b.prix_vente, b.date_vente
            FROM bail b
            JOIN propriete p ON b.id_propriete = p.id_propriete
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


def afficher_baux(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    bouton_ajouter_bail = tk.Button(frame, text="Ajouter Bail", command=lambda: afficher_formulaire_ajout_bail(frame))
    bouton_ajouter_bail.pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_baux = tk.Frame(canvas, bg='white')

    frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    canvas.create_window((0, 0), window=frame_baux, anchor="nw")
    frame_baux.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    baux = recuperer_baux()

    headers = ["ID", "Nom Propriété", "Nom Locataire", "Date Début", "Date Fin", "Loyer Mensuel", "Dépôt Garantie",
               "Conditions Spéciales", "Prix Vente", "Date Vente", "Modifier", "Supprimer"]
    for idx, header in enumerate(headers):
        tk.Label(frame_baux, text=header, bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=idx, padx=10,
                                                                                       pady=5)

    for i, bail in enumerate(baux):
        for j, value in enumerate(bail):
            tk.Label(frame_baux, text=value, bg='white').grid(row=i + 1, column=j, padx=10, pady=5)

        bouton_modifier = tk.Button(frame_baux, text="Modifier",
                                    command=lambda id_b=bail[0]: modifier_bail(id_b, frame))
        bouton_modifier.grid(row=i + 1, column=len(headers) - 2, padx=5, pady=5)

        bouton_supprimer = tk.Button(frame_baux, text="Supprimer",
                                     command=lambda id_b=bail[0]: supprimer_bail(id_b, frame))
        bouton_supprimer.grid(row=i + 1, column=len(headers) - 1, padx=5, pady=5)




def afficher_formulaire_ajout_bail(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Nom Propriété", "Nom Locataire", "Date Début", "Date Fin", "Loyer Mensuel", "Dépôt Garantie",
              "Conditions Spéciales", "Prix Vente", "Date Vente"]
    entries = {}

    proprietes = recuperer_proprietes()
    proprietes_options = [f"{prop[1]} ({prop[0]})" for prop in proprietes]

    locataires = recuperer_locataires()
    locataire_options = [f"{loc[1]} ({loc[0]})" for loc in locataires]

    for idx, text in enumerate(labels):
        tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if "Propriété" in text:
            entry = tk.StringVar()
            entry.set(proprietes_options[0] if proprietes_options else "")
            option_menu = tk.OptionMenu(form_frame, entry, *proprietes_options)
            option_menu.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        elif "Locataire" in text:
            entry = tk.StringVar()
            entry.set(locataire_options[0] if locataire_options else "")
            option_menu = tk.OptionMenu(form_frame, entry, *locataire_options)
            option_menu.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        elif "Date" in text:
            entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                              date_pattern='mm/dd/yyyy')
            entry.grid(row=idx, column=1, padx=10, pady=5)
        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[text] = entry



    def ajouter_bail():
        values = {key: entry.get() for key, entry in entries.items()}

        if not all(values.values()):
            messagebox.showwarning("Validation", "Tous les champs doivent être remplis.")
            return

        try:
            id_propriete = values["Nom Propriété"].split("(")[1][:-1]
            id_locataire = values["Nom Locataire"].split("(")[1][:-1]

            # Formatage des dates
            date_debut = datetime.strptime(values["Date Début"], "%m/%d/%Y").date() if values["Date Début"] else None
            date_fin = datetime.strptime(values["Date Fin"], "%m/%d/%Y").date() if values["Date Fin"] else None

            connection = connecter_bd()
            cursor = connection.cursor()
            query = """INSERT INTO bail (id_propriete, id_locataire, date_debut, date_fin, loyer_mensuel, depot_garantie, cond_special, prix_vente, date_vente)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                id_propriete,
                id_locataire,
                date_debut,
                date_fin,
                values["Loyer Mensuel"],
                values["Dépôt Garantie"],
                values["Conditions Spéciales"],
                values["Prix Vente"],
                values["Date Vente"]
            ))
            connection.commit()
            messagebox.showinfo("Succès", "Bail ajouté avec succès")
            afficher_baux(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du bail: {e}")
        except ValueError:
            messagebox.showwarning("Erreur de Format", "Le format de la date est incorrect. Utilisez m/j/a.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    bouton_ajouter = tk.Button(form_frame, text="Ajouter", command=ajouter_bail, bg='green', fg='white')
    bouton_ajouter.grid(row=len(labels), column=1, pady=10)


def modifier_bail(id_bail, frame):
    for widget in frame.winfo_children():
        widget.destroy()  # Efface les widgets existants dans le cadre

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Nom Propriété", "Nom Locataire", "Date Début", "Date Fin", "Loyer Mensuel", "Dépôt Garantie",
              "Conditions Spéciales", "Prix Vente", "Date Vente"]
    entries = {}

    # Récupération des informations actuelles du bail
    connection = connecter_bd()
    cursor = connection.cursor()

    try:
        query = """SELECT id_propriete, id_locataire, date_debut, date_fin, loyer_mensuel, depot_garantie, cond_special, prix_vente, date_vente 
                   FROM bail WHERE id_bail = %s"""
        cursor.execute(query, (id_bail,))
        bail_info = cursor.fetchone()

        propriete_options = recuperer_proprietes()
        locataire_options = recuperer_locataires()

        for idx, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
            if "Propriété" in text:
                entry = tk.StringVar()
                entry.set(f"{bail_info[0]} - {next(nom for id_, nom in propriete_options if id_ == bail_info[0])}")
                option_menu = tk.OptionMenu(form_frame, entry, *[f"{id_} - {nom}" for id_, nom in propriete_options])
                option_menu.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry
            elif "Locataire" in text:
                entry = tk.StringVar()
                entry.set(f"{bail_info[1]} - {next(nom for id_, nom in locataire_options if id_ == bail_info[1])}")
                option_menu = tk.OptionMenu(form_frame, entry, *[f"{id_} - {nom}" for id_, nom in locataire_options])
                option_menu.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry
            elif "Date" in text:
                entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                  date_pattern='dd/mm/yyyy')
                entry.set_date(bail_info[2 + idx - 2])  # Correspond à la date dans la base
                entry.grid(row=idx, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(form_frame)
                entry.insert(0, bail_info[4 + idx - 4])  # Ajustez l'index selon le champ
                entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry

        def enregistrer_modifications():
            try:
                id_propriete = entries["Nom Propriété"].get().split(' - ')[0]
                id_locataire = entries["Nom Locataire"].get().split(' - ')[0]
                date_debut = entries["Date Début"].get_date()
                date_fin = entries["Date Fin"].get_date()
                loyer_mensuel = entries["Loyer Mensuel"].get()
                depot_garantie = entries["Dépôt Garantie"].get()
                cond_special = entries["Conditions Spéciales"].get()
                prix_vente = entries["Prix Vente"].get()
                date_vente = entries["Date Vente"].get_date()

                connection = connecter_bd()
                cursor = connection.cursor()
                query = """UPDATE bail 
                           SET id_propriete = %s, id_locataire = %s, date_debut = %s, date_fin = %s, loyer_mensuel = %s, depot_garantie = %s, cond_special = %s, prix_vente = %s, date_vente = %s
                           WHERE id_bail = %s"""
                values = (id_propriete, id_locataire, date_debut, date_fin, loyer_mensuel, depot_garantie, cond_special,
                          prix_vente, date_vente, id_bail)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Bail modifié avec succès")
                afficher_baux(frame)  # Réafficher la liste des baux
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification du bail : {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        bouton_enregistrer = tk.Button(form_frame, text="Enregistrer", command=enregistrer_modifications, bg='green',
                                       fg='white')
        bouton_enregistrer.grid(row=len(labels), column=1, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations du bail : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def supprimer_bail(id_bail, frame):
    if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce bail ?"):
        try:
            connection = connecter_bd()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM bail WHERE id_bail = %s", (id_bail,))
            connection.commit()
            messagebox.showinfo("Succès", "Bail supprimé avec succès")
            afficher_baux(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du bail: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


