import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
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
        resultats = cursor.fetchall()
        if not resultats:
            messagebox.showinfo("Info", "Aucune propriété trouvée.")
        return resultats
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des propriétés : {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def recuperer_entretien():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT e.id_entretien, p.nom_propiete, e.nom_entretieneur, e.date_entretien, e.type_entretien, e.cout, e.commentaire_entretien FROM entretien e JOIN propriete p ON e.id_propriete = p.id_propriete")
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des entretiens : {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def recuperer_techniciens():
    try:
        connection = connecter_bd()
        cursor = connection.cursor()
        cursor.execute("SELECT CONCAT(nom_utilisateur, ' ', prenom_utilisateur) AS nom_complet FROM utilisateur WHERE role = 'Technicien d''Entretien'")
        techniciens = cursor.fetchall()
        return [t[0] for t in techniciens]  # Liste des noms complets
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des techniciens : {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def afficher_entretien(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    bouton_ajouter_entretien = tk.Button(frame, text="Ajouter Entretien", command=lambda: afficher_formulaire_ajout_entretien(frame))
    bouton_ajouter_entretien.pack(pady=10)

    canvas = tk.Canvas(frame, bg='white')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)

    frame_entretien = tk.Frame(canvas, bg='white')
    frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    canvas.create_window((0, 0), window=frame_entretien, anchor="nw")
    frame_entretien.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    entretiens = recuperer_entretien()

    headers = ["ID", "Nom Propriété", "Nom Technicien", "Date Entretien", "Type Entretien", "Coût", "Commentaire", "Modifier", "Supprimer"]
    for idx, header in enumerate(headers):
        tk.Label(frame_entretien, text=header, bg='white', font=('Arial', 12, 'bold')).grid(row=0, column=idx, padx=10, pady=5)

    for i, entretien in enumerate(entretiens):
        for j, value in enumerate(entretien):
            tk.Label(frame_entretien, text=value, bg='white').grid(row=i + 1, column=j, padx=10, pady=5)

        bouton_modifier = tk.Button(frame_entretien, text="Modifier", command=lambda id_e=entretien[0]: modifier_entretien(id_e, frame))
        bouton_modifier.grid(row=i + 1, column=len(headers) - 2, padx=5, pady=5)

        bouton_supprimer = tk.Button(frame_entretien, text="Supprimer", command=lambda id_e=entretien[0]: supprimer_entretien(id_e, frame))
        bouton_supprimer.grid(row=i + 1, column=len(headers) - 1, padx=5, pady=5)

def afficher_formulaire_ajout_entretien(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Nom Propriété", "Nom Technicien", "Date Entretien", "Type Entretien", "Coût", "Commentaire"]
    entries = {}

    proprietes = recuperer_proprietes()
    proprietes_options = [f"{prop[1]} ({prop[0]})" for prop in proprietes]
    techniciens = recuperer_techniciens()

    for idx, text in enumerate(labels):
        tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
        if "Propriété" in text:
            entry = tk.StringVar()
            entry.set(proprietes_options[0] if proprietes_options else "")
            option_menu = tk.OptionMenu(form_frame, entry, *proprietes_options)
            option_menu.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        elif "Date" in text:
            entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        elif "Technicien" in text:
            entry = ttk.Combobox(form_frame, values=techniciens)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry
        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[text] = entry

    def ajouter_entretien():
        values = {key: entry.get() for key, entry in entries.items()}

        if not all(values.values()):
            messagebox.showwarning("Validation", "Tous les champs doivent être remplis.")
            return

        try:
            id_propriete = values["Nom Propriété"].split("(")[1][:-1]
            date_entretien = datetime.strptime(values["Date Entretien"], "%m/%d/%Y").date() if values["Date Entretien"] else None

            connection = connecter_bd()
            cursor = connection.cursor()
            query = """INSERT INTO entretien (id_propriete, nom_entretieneur, date_entretien, type_entretien, cout, commentaire_entretien)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                id_propriete,
                values["Nom Technicien"],
                date_entretien,
                values["Type Entretien"],
                values["Coût"],
                values["Commentaire"]
            ))
            connection.commit()
            messagebox.showinfo("Succès", "Entretien ajouté avec succès")
            afficher_entretien(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'entretien: {e}")
        except ValueError:
            messagebox.showwarning("Erreur de Format", "Le format de la date est incorrect. Utilisez m/j/a.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    bouton_ajouter = tk.Button(form_frame, text="Ajouter", command=ajouter_entretien, bg='green', fg='white')
    bouton_ajouter.grid(row=len(labels), column=1, pady=10)

def modifier_entretien(id_entretien, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    form_frame = tk.Frame(frame, bg='white', padx=20, pady=20)
    form_frame.pack(pady=10)

    labels = ["Nom Propriété", "Nom Technicien", "Date Entretien", "Type Entretien", "Coût", "Commentaire"]
    entries = {}

    connection = connecter_bd()
    cursor = connection.cursor()

    try:
        query = """SELECT id_propriete, nom_entretieneur, date_entretien, type_entretien, cout, commentaire_entretien 
                   FROM entretien WHERE id_entretien = %s"""
        cursor.execute(query, (id_entretien,))
        entretien_info = cursor.fetchone()

        proprietes_options = recuperer_proprietes()

        for idx, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg='white').grid(row=idx, column=0, padx=10, pady=5)
            if "Propriété" in text:
                entry = tk.StringVar()
                entry.set(f"{next(prop[1] for prop in proprietes_options if prop[0] == entretien_info[0])} ({entretien_info[0]})")
                option_menu = tk.OptionMenu(form_frame, entry, *[f"{prop[1]} ({prop[0]})" for prop in proprietes_options])
                option_menu.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry
            elif "Date" in text:
                entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
                entry.set_date(entretien_info[2])
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry
            else:
                entry = tk.Entry(form_frame)
                entry.insert(0, entretien_info[idx + 1])
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entries[text] = entry

        def enregistrer_modifications():
            try:
                id_propriete = entries["Nom Propriété"].get().split("(")[1][:-1]
                nom_entretieneur = entries["Nom Technicien"].get()
                date_entretien = entries["Date Entretien"].get_date()
                type_entretien = entries["Type Entretien"].get()
                cout = entries["Coût"].get()
                commentaire = entries["Commentaire"].get()

                connection = connecter_bd()
                cursor = connection.cursor()
                query = """UPDATE entretien 
                           SET id_propriete = %s, nom_entretieneur = %s, date_entretien = %s, type_entretien = %s, cout = %s, commentaire_entretien = %s
                           WHERE id_entretien = %s"""
                values = (id_propriete, nom_entretieneur, date_entretien, type_entretien, cout, commentaire, id_entretien)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Entretien modifié avec succès")
                afficher_entretien(frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification de l'entretien : {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        bouton_enregistrer = tk.Button(form_frame, text="Enregistrer", command=enregistrer_modifications, bg='orange', fg='white')
        bouton_enregistrer.grid(row=len(labels), column=1, pady=10)

    except Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations de l'entretien : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def supprimer_entretien(id_entretien, frame):
    if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet entretien ?"):
        try:
            connection = connecter_bd()
            cursor = connection.cursor()
            query = "DELETE FROM entretien WHERE id_entretien = %s"
            cursor.execute(query, (id_entretien,))
            connection.commit()
            messagebox.showinfo("Succès", "Entretien supprimé avec succès")
            afficher_entretien(frame)
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'entretien : {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


