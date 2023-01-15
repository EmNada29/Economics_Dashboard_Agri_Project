#On importe la classe du backend qui gère la DB SQL
from backend import Database

#On importe la fonction du dashboard qui analyse les données et génère le dashboard
from dashboard import data_analysis

#On importe les packages
from PySide2 import QtWidgets, QtCore
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import panel as pn
pn.extension('tabulator')

#Package pas utilisé finalement
from panel.template import DarkTheme
import hvplot.pandas


#Chargement de la base de données dans une variable
database = Database("pse.db")

#Création du GUI
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSE - Application par défaut")
        self.setup_ui()
        self.setup_connections()


    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.e1 = QtWidgets.QLineEdit()
        self.e2 = QtWidgets.QLineEdit()
        self.e2.setMaxLength(15)
        self.e3 = QtWidgets.QLineEdit()
        self.e3.setMaxLength(4)
        self.e4 = QtWidgets.QLineEdit()
        self.e4.setMaxLength(4)
        self.e5 = QtWidgets.QLineEdit()
        self.e5.setMaxLength(4)
        self.e6 = QtWidgets.QLineEdit()
        self.e6.setMaxLength(4)
        self.e7 = QtWidgets.QLineEdit()
        self.e7.setMaxLength(4)
        self.e8 = QtWidgets.QLineEdit()
        self.e8.setMaxLength(4)
        self.e9 = QtWidgets.QLineEdit()
        self.e9.setMaxLength(4)
        self.e10 = QtWidgets.QLineEdit()
        self.e10.setMaxLength(4)

        self.e1_label = QtWidgets.QLabel("Nom de l'exploitation")
        self.e2_label = QtWidgets.QLabel("Num. SIREN")
        self.e3_label = QtWidgets.QLabel("Année (aaaa)")
        self.e4_label = QtWidgets.QLabel("SAU (ha)")
        self.e5_label = QtWidgets.QLabel("Surface Indicateur 1 (ha)")
        self.e6_label = QtWidgets.QLabel("Surface Indicateur 2 (ha)")
        self.e7_label = QtWidgets.QLabel("Surface Indicateur 3 (ha)")
        self.e8_label = QtWidgets.QLabel("Performance Indicateur 1 (ha)")
        self.e9_label = QtWidgets.QLabel("Performance Indicateur 2 (ha)")
        self.e10_label = QtWidgets.QLabel("Performance Indicateur 3 (ha)")


        self.button1 = QtWidgets.QPushButton("Voir tout")
        self.button2 = QtWidgets.QPushButton("Chercher une exploitation")
        self.button3 = QtWidgets.QPushButton("Ajouter")
        self.button4 = QtWidgets.QPushButton("Mettre à jour")
        self.button5 = QtWidgets.QPushButton("Supprimer")
        self.button6 = QtWidgets.QPushButton("Fermer")
        self.button7 = QtWidgets.QPushButton("Charger les données")
        self.button8 = QtWidgets.QPushButton("Analyser l'exploitation")

        self.lw_users = QtWidgets.QListWidget()
        self.lw_users.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

        self.lw_users_2 = QtWidgets.QListWidget()
        self.lw_users_2.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)


        self.main_layout.addWidget(self.e1_label)
        self.main_layout.addWidget(self.e1)
        self.main_layout.addWidget(self.e2_label)
        self.main_layout.addWidget(self.e2)
        self.main_layout.addWidget(self.e3_label)
        self.main_layout.addWidget(self.e3)
        self.main_layout.addWidget(self.e4_label)
        self.main_layout.addWidget(self.e4)
        self.main_layout.addWidget(self.e5_label)
        self.main_layout.addWidget(self.e5)
        self.main_layout.addWidget(self.e6_label)
        self.main_layout.addWidget(self.e6)
        self.main_layout.addWidget(self.e7_label)
        self.main_layout.addWidget(self.e7)
        self.main_layout.addWidget(self.e8_label)
        self.main_layout.addWidget(self.e8)
        self.main_layout.addWidget(self.e9_label)
        self.main_layout.addWidget(self.e9)
        self.main_layout.addWidget(self.e10_label)
        self.main_layout.addWidget(self.e10)

        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.main_layout.addWidget(self.button7)
        self.main_layout.addWidget(self.button3)
        self.main_layout.addWidget(self.button4)
        self.main_layout.addWidget(self.button5)
        self.main_layout.addWidget(self.lw_users)
        self.main_layout.addWidget(self.button8)
        self.main_layout.addWidget(self.lw_users_2)
        self.main_layout.addWidget(self.button6)


    def setup_connections(self):
        self.button1.clicked.connect(self.view_command)
        self.button2.clicked.connect(self.search_command)
        self.button3.clicked.connect(self.add_command)
        self.button4.clicked.connect(self.update_command)
        self.button5.clicked.connect(self.delete_command)
        self.button7.clicked.connect(self.get_selected_row)
        self.button8.clicked.connect(self.analyse_command)
        self.button6.clicked.connect(self.close)


    def add_command(self):
        database.insert(self.e1.text(), self.e2.text(), self.e3.text(),
                        self.e4.text(), self.e5.text(), self.e6.text(),
                        self.e7.text(), self.e8.text(), self.e9.text(),
                        self.e10.text())
        self.lw_users.clear()
        list_to_add =[]
        list_to_add.append(self.e1.text() + self.e2.text() + self.e3.text())
        self.lw_users.addItems(list_to_add)

        # On remplit la 2ème listbox, avec juste le Nom_Exploitation
        con = sqlite3.connect("pse.db")
        cur = con.cursor()

        request_2 = f"select DISTINCT Nom_Exploitation from pse"
        cur.execute(request_2)
        results_2 = cur.fetchall()
        for _ in results_2:
            self.lw_users_2.addItems(_)


    def delete_command(self):
        for item in self.lw_users.selectedItems():
            id_to_remove=item.text()[0]+item.text()[1]
        #print(id_to_remove)
        database.delete(id_to_remove)
        self.lw_users.clear() #A garder ?
        self.view_command()


    def view_command(self):
        self.lw_users.clear()
        self.lw_users_2.clear()

        con = sqlite3.connect("pse.db")
        cur = con.cursor()
        i=1
        while i<1000: #On aura un msg d'erreur dès que i > au nombre d'entrées dans la base SQL pse.db. Voir comment corriger (si besoin ?)
            users_instances = []
            lines = []
            request = f"select id, Nom_Exploitation, SIREN, Annee from pse WHERE id={i}"
            cur.execute(request)
            results = cur.fetchone()
            #print(results)
            if results != None:
                for _ in results:
                    users_instances.append(_)
                line=f"{users_instances[0]}  {users_instances[1]}  {users_instances[2]} {users_instances[3]}"
                lines.append(line)
                self.lw_users.addItems(lines)
                i+=1
            else:
                i += 1

        # On remplit la 2ème listbox, avec juste le Nom_Exploitation
        request_2 = f"select DISTINCT Nom_Exploitation from pse"
        cur.execute(request_2)
        results_2 = cur.fetchall()
        for _ in results_2:
            self.lw_users_2.addItems(_)


    def search_command(self):
        self.lw_users.clear()

        #On appelle d'abord la fonction de la classe Database (Backend)
        for row in database.search(self.e1.text(), self.e2.text(), self.e3.text(),
                        self.e4.text(), self.e5.text(), self.e6.text(),
                        self.e7.text(), self.e8.text(), self.e9.text(),
                        self.e10.text()):
            results_bis=[]
            lines_bis = []
            results_bis.append(row)
            #print(results_bis)
            if results_bis != None:
                line_bis = f"{results_bis[0][0]} {results_bis[0][1]} {results_bis[0][2]} {results_bis[0][3]}"
                #print(line_bis)
                lines_bis.append(line_bis)
                self.lw_users.addItems(lines_bis)


    def get_selected_row(self):
     #IDEE POUR PLUS TARD : améliorer en appelant la fonction avec un event et non un push button
     for item in self.lw_users.selectedItems():
        id_to_update = item.text()[0]+item.text()[1]
        #print(id_to_update)
        users_instances = []
        con = sqlite3.connect("pse.db")
        cur = con.cursor()
        request = f"select * from pse WHERE id={id_to_update}"
        cur.execute(request)
        results = cur.fetchone()
        for _ in results:
            users_instances.append(_)
        #print(users_instances)

        self.e1.setText(users_instances[1])
        self.e2.setText(str(users_instances[2]))
        self.e3.setText(str(users_instances[3]))
        self.e4.setText(str(users_instances[4]))
        self.e5.setText(str(users_instances[5]))
        self.e6.setText(str(users_instances[6]))
        self.e7.setText(str(users_instances[7]))
        self.e8.setText(str(users_instances[8]))
        self.e9.setText(str(users_instances[9]))
        self.e10.setText(str(users_instances[10]))


    def update_command(self):
        for item in self.lw_users.selectedItems():
            id_to_update = item.text()[0]+item.text()[1]
            print(id_to_update)
        database.update(id_to_update,self.e1.text(), self.e2.text(), self.e3.text(),
                        self.e4.text(), self.e5.text(), self.e6.text(),
                        self.e7.text(), self.e8.text(), self.e9.text(),
                        self.e10.text() )
        self.view_command()

    def analyse_command(self):
        for item in self.lw_users_2.selectedItems():
            user_choosen= item.text()
        #On importe le script DASHBOARD (i.e. la fonction : data analysis)
        return data_analysis(user_choosen)
        #Pb à régler : le GUI ne se ferme pas correctement après après de la fonction data_analysis
        self.close

'''
#A remplacer car je pense que c'est cette partie qui bug
app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
'''

#J'ai remplacé par ce bout de code, mais ça ne résoud pas le pb de la fermeture de la fenêtre
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    #app.exec_()
    sys.exit(app.exec_())