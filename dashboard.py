import sqlite3
import sys
import PySide2.QtWidgets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

from PySide2 import QtWidgets, QtCore
import panel as pn
#Pas utilisé finalement
from panel.template import DarkTheme
pn.extension('tabulator')
import hvplot.pandas


def data_analysis(user_choosen):
    con = sqlite3.connect("pse.db")
    cur = con.cursor()
    # On charge dans un DataFrame de pandas la DB SQL pse.db
    data = pd.read_sql_query("SELECT * FROM pse", con)

    # print(data)
    # On trie la DB data (df) par ordre alphabétique, puis par année
    data = data.sort_values(by=["Nom_Exploitation", "Annee"], ascending=True)
    data_to_display = data.iloc[:, 1:]
    # Régler ce pb : enlever le séparateur de milliers
    # data_to_display.pd.io.formats.style.Styler.format(thousands=None)

    # print(data_to_display)
    data_to_display = data_to_display.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10,
                                           sizing_mode='stretch_width')

    # print(data_to_display)
    # print(data)

    #######################################################################################################################
    #################INFOS GENERALES SUR LA PERFORMANCE####################################################################
    #######################################################################################################################

    #######################################################################################################################
    ########################################################FIG1 - GENERALE################################################
    #######################################################################################################################
    # Make DataFrame Pipeline Interactive
    # idf : interactive data frame
    idf = data.interactive()

    # Define Panel widgets
    year_slider = pn.widgets.IntSlider(name="Actualiser jusqu'à ", start=2021, end=2026, step=1, value=2026)

    # Radio buttons Pour les 6 années
    yaxis_user = pn.widgets.RadioButtonGroup(
        name='Y axis',
        options=['INDICATEUR1_score', 'INDICATEUR2_score', 'INDICATEUR3_score'],
        button_type='success'
    )


    user_pipeline = (
        idf[(idf.Annee <= year_slider)]
       )

    user_plot = user_pipeline.hvplot(x='Annee', by='Nom_Exploitation', y=yaxis_user, line_width=2,
                                     title="Suivi annuel de toutes les exploitations")


    #https://courspython.com/interfaces.html

    #######################################################################################################################
    #########################################INDICATEUR 1##################################################################
    #######################################################################################################################
    # Paramètres pour les 3 indicateurs
    labels = ['2021', '2022', '2023', '2024', '2025', '2026']
    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig_1, ax = plt.subplots()
    data_choosen_surface = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR1"], "NaN")
    data_choosen_score = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR1_score"], "NaN")

    #print(data_choosen_surface)
    #print(data_choosen_score)

    #On récupère les items (6) en exluant les NaN créés avec le numpy.where()
    data_choosen_surface=data_choosen_surface.__getitem__(data_choosen_surface!="NaN")
    data_choosen_score=data_choosen_score.__getitem__(data_choosen_score!="NaN")

    #print(data_choosen_surface)
    #print(data_choosen_score)

    #Avec les map() et list(), on reconvertie les items en int
    int_data_choosen_surface=list(map(int, data_choosen_surface))
    int_data_choosen_score=list(map(int, data_choosen_score))

    #On récupère des valeurs pour les figures 4,5 et 6
    fig4_val1=int_data_choosen_score[5]

    fig4_val1_1=int_data_choosen_score[0]
    fig4_val1_2=int_data_choosen_score[1]
    fig4_val1_3=int_data_choosen_score[2]
    fig4_val1_4=int_data_choosen_score[3]
    fig4_val1_5=int_data_choosen_score[4]
    fig4_val1_6=int_data_choosen_score[5]

    #print(data_choosen_surface)
    #print(data_choosen_score)

    col1 = ax.bar(labels, int_data_choosen_surface, width, label='Surface (ha)', color='seagreen')
    col2 = ax.bar(labels,int_data_choosen_score , width, label='Objectif atteint (ha)', color='mediumseagreen', hatch="///",
                  edgecolor='black')

    ax.bar_label(col1, padding=1)
    ax.bar_label(col2, padding=1)

    ax.set_ylabel('hectares (ha)')
    ax.set_title("Score pour l'indicateur 1")
    ax.legend()

    #######################################################################################################################
    #########################################INDICATEUR 2##################################################################
    #######################################################################################################################

    fig_2, ax = plt.subplots()
    data_choosen_surface = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR2"], "NaN")
    data_choosen_score = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR2_score"], "NaN")

    data_choosen_surface=data_choosen_surface.__getitem__(data_choosen_surface!="NaN")
    data_choosen_score=data_choosen_score.__getitem__(data_choosen_score!="NaN")

    int_data_choosen_surface=list(map(int, data_choosen_surface))
    int_data_choosen_score=list(map(int, data_choosen_score))

    #On récupère des valeurs pour les figures 4,5 et 6
    fig4_val2=int_data_choosen_score[5]

    fig5_val2_1=int_data_choosen_score[0]
    fig5_val2_2=int_data_choosen_score[1]
    fig5_val2_3=int_data_choosen_score[2]
    fig5_val3_4=int_data_choosen_score[3]
    fig5_val4_5=int_data_choosen_score[4]
    fig5_val5_6=int_data_choosen_score[5]


    col1 = ax.bar(labels, int_data_choosen_surface, width, label='Surface (ha)', color='steelblue')
    col2 = ax.bar(labels, int_data_choosen_score, width, label='Objectif atteint (ha)', color='lightskyblue', hatch="///",
                  edgecolor='black')

    ax.bar_label(col1, padding=1)
    ax.bar_label(col2, padding=1)

    ax.set_ylabel('hectares (ha)')
    ax.set_title("Score pour l'indicateur 2")
    ax.legend()

    # plt.show()

    #######################################################################################################################
    #########################################INDICATEUR 3##################################################################
    #######################################################################################################################

    fig_3, ax = plt.subplots()
    data_choosen_surface = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR3"], "NaN")
    data_choosen_score = np.where(data["Nom_Exploitation"] == user_choosen, data["INDICATEUR3_score"], "NaN")

    data_choosen_surface=data_choosen_surface.__getitem__(data_choosen_surface!="NaN")
    data_choosen_score=data_choosen_score.__getitem__(data_choosen_score!="NaN")

    int_data_choosen_surface=list(map(int, data_choosen_surface))
    int_data_choosen_score=list(map(int, data_choosen_score))

    #On récupère des valeurs pour les figures 4,5 et 6
    fig4_val3=int_data_choosen_score[5]

    fig6_val3_1=int_data_choosen_score[0]
    fig6_val3_2=int_data_choosen_score[1]
    fig6_val3_3=int_data_choosen_score[2]
    fig6_val3_4=int_data_choosen_score[3]
    fig6_val3_5=int_data_choosen_score[4]
    fig6_val3_6=int_data_choosen_score[5]


    col1 = ax.bar(labels, int_data_choosen_surface, width, label='Surface (ha)', color='darksalmon')
    col2 = ax.bar(labels, int_data_choosen_score, width, label='Objectif atteint (ha)', color='coral', hatch="///",
                  edgecolor='black')

    ax.bar_label(col1, padding=1)
    ax.bar_label(col2, padding=1)

    ax.set_ylabel('hectares (ha)')
    ax.set_title("Score pour l'indicateur 3")
    ax.legend()

    #######################################################################################################################
    ########################################################FIG4 - GENERALE################################################
    #######################################################################################################################

    # make figure and assign axis objects
    fig_4, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig_4.subplots_adjust(wspace=0)

    # pie chart parameters
    #overall_ratios = [.27, .56, .17]
    overall_ratios = [fig4_val1, fig4_val2, fig4_val3]

    labels = ['Part du score, Indicateur 1', 'Part du score, Indicateur 2', 'Part du score, Indicateur 3']
    explode = [0.1, 0, 0]
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                         labels=labels, explode=explode)

    # bar chart parameters

    years_ratios=[fig4_val1_1 / fig4_val1_6,
                  (fig4_val1_2 - fig4_val1_1) / fig4_val1_6,
                  (fig4_val1_3 - fig4_val1_2) / fig4_val1_6,
                  (fig4_val1_4 - fig4_val1_3) / fig4_val1_6,
                  (fig4_val1_5 - fig4_val1_4) / fig4_val1_6,
                  (fig4_val1_6 - fig4_val1_5) / fig4_val1_6
                  ]

    years_labels = ["2021","2022","2023","2024","2025","2026"]
    bottom = 1
    width = .2

    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(years_ratios, years_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                     alpha=0.1 + (1/6) * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title("Pourcentage d'atteinte de l'objectif, par année")
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(years_ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)

    #######################################################################################################################
    ########################################################FIG5 - GENERALE################################################
    #######################################################################################################################

    # make figure and assign axis objects
    fig_5, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig_5.subplots_adjust(wspace=0)

    # pie chart parameters
    overall_ratios = [fig4_val2, fig4_val1, fig4_val3]

    labels = ['Part du score, Indicateur 2', 'Part du score, Indicateur 1',  'Part du score, Indicateur 3']
    explode = [0.1, 0, 0]
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                         labels=labels, explode=explode)

    # bar chart parameters

    years_ratios=[fig5_val2_1/fig5_val5_6,
                (fig5_val2_2-fig5_val2_1)/fig5_val5_6,
                (fig5_val2_3-fig5_val2_2)/fig5_val5_6,
                (fig5_val3_4-fig5_val2_3)/fig5_val5_6,
                (fig5_val4_5-fig5_val3_4)/fig5_val5_6,
                (fig5_val5_6-fig5_val4_5)/fig5_val5_6
                  ]


    years_labels = ["2021","2022","2023","2024","2025","2026"]
    bottom = 1
    width = .2

    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(years_ratios, years_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                     alpha=0.1 + (1/6) * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title("Pourcentage d'atteinte de l'objectif, par année")
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(years_ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)

    #######################################################################################################################
    ########################################################FIG6 - GENERALE################################################
    #######################################################################################################################

    # make figure and assign axis objects
    fig_6, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig_6.subplots_adjust(wspace=0)

    # pie chart parameters
    overall_ratios = [fig4_val3, fig4_val1, fig4_val2]

    labels = ['Part du score, Indicateur 3', 'Part du score, Indicateur 1', 'Part du score, Indicateur 2']
    explode = [0.1, 0, 0]
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                         labels=labels, explode=explode)

    # bar chart parameters

    years_ratios=[fig6_val3_1 / fig6_val3_6,
                  (fig6_val3_2 - fig6_val3_1) / fig6_val3_6,
                  (fig6_val3_3 - fig6_val3_2) / fig6_val3_6,
                  (fig6_val3_4 - fig6_val3_3) / fig6_val3_6,
                  (fig6_val3_5 - fig6_val3_4) / fig6_val3_6,
                  (fig6_val3_6 - fig6_val3_5) / fig6_val3_6
                  ]


    years_labels = ["2021","2022","2023","2024","2025","2026"]
    bottom = 1
    width = .2

    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(years_ratios, years_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                     alpha=0.1 + (1/6) * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title("Pourcentage d'atteinte de l'objectif, par année")
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(years_ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)

    #Laisser le plt.show() en commentaire, sinon l'exécution du script éditera tous les graphiques
    #plt.show()

    #######################################################################################################################
    ########################################################DASHBOARD - LAYOUT#############################################
    #######################################################################################################################

    sumup="Projet python avec frontend (GUI, réalisé avec QTWidgets, talbeau de bord (dashboard) avec panel) et backend (base de données SQL, avec le package python Sqlite3) " \
          "permettant d'afficher un formulaire dans lequel l'utilisateur peut insérer de nouvelles donnnées, parcourir la " \
          "base de données, charger de précédentes données dans le formulaire, les modifier, les supprimer." \
          " " \
          "Réalisé par Emilian Nadau" \
          " " \
          "emilian.nadau@gmail.com"
    description="Cette application permet d'entrer des données relatives à des exploitations agricoles, année par année (de 2021 à 2026). " \
                "L'utilisateur peut ensuite afficher dans un tableau de suivi un graphique retranscrivant les performances de toutes " \
                "les exploitations, de 2021 à 2026, une base de données interative, et des graphiques (pie et barchats) relatifs " \
                "à l'exploitation selectionnée dans la fenêtre correspondante. "

    # Layout using Template
    template = pn.template.FastListTemplate(
        title='PSE - Tableau de bord par défaut',
        #theme=DarkTheme,
        sidebar=[pn.pane.Markdown("# Paiements pour services écosystémiques (PSE)"),
                 pn.pane.PNG('caption.png', sizing_mode='scale_both'),
                 pn.pane.Markdown("## Années sélectionnées"), year_slider,
                 pn.pane.Markdown(f"### {sumup}"),
                 pn.pane.Markdown(f"### {description}")],
        main=[pn.Row(pn.Column("# Vue d'ensemble, toutes exploitations comprises", width=2000)),
              pn.Row(pn.Column(yaxis_user, user_plot.panel(width=700), margin=(0,5)),
                     pn.Column(data_to_display)),
              pn.Row(pn.Column(f"# Analyse graphique pour l'utilisateur : {user_choosen}", width=2000)),
              pn.Row(pn.Column(fig_4),
                     pn.Column(fig_5),
                     pn.Column(fig_6)),
              pn.Row(pn.Column(fig_1),
                     pn.Column(fig_2),
                     pn.Column(fig_3))],
        accent_base_color="#88d8b0",
        header_background="#88d8b0",
    )
    template.show()
    template.servable()