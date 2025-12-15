from data import data_program
import sys
import subprocess
import streamlit as st
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt



def load_analysis_data():
    with open("data/analysis_data.json") as data_file:
        data = json.load(data_file)
    work_positions = data[2]
    translated_positions = {}
    for key in work_positions:
        translated_positions[work_positions[key]['translation']] = work_positions[key]['count']
    loaded_data = [
        {
        "labels": list(data[0].keys()),
        "values": list(data[0].values())
        },
        {
            "labels": list(data[1].keys()),
            "values": list(data[1].values())
        },
        {
            "labels": list(translated_positions.keys()),
            "values": list(translated_positions.values())
        },
        data[3],
        {
            "labels": list(data[4].keys()),
            "values": list(data[4].values())
        }
    ]
    return loaded_data

analysis_data = load_analysis_data()
programming_languages = analysis_data[0]
work_modes = analysis_data[1]
positions = analysis_data[2]
ai_jobs_percentage = analysis_data[3]
average_position_salaries = analysis_data[4]
graph_1 = plt.figure()
plt.pie(work_modes['values'], labels=work_modes['labels'], autopct="%.2f%%", startangle=45, colors=["#00A0FF","red","green"])
plt.title("Stosunek ofert pracy zdalnej vs hybrydowej vs stacjonarnej")
plt.show()
graph_2 = plt.figure()
plt.title("Najbardziej poszukiwane języki programowania")
plt.barh(programming_languages['labels'], programming_languages['values'], edgecolor="black", lw=1, color="darkgreen")
plt.xlabel("Amount of job offers")
plt.show()
graph_3 = plt.figure()
plt.title("Najbardziej poszukiwane stanowiska")
plt.barh(positions['labels'], positions['values'], color="blue", edgecolor="black", lw=2)
plt.tick_params(axis="y", labelsize=8)
plt.show()
graph_4 = plt.figure()
plt.title("Średnia płaca na stanowiskach: Junior, Mid, Senior")
bars = plt.bar(average_position_salaries['labels'], average_position_salaries['values'], color="purple", width=0.2, edgecolor="black", lw=2)
plt.yticks([10000, 20000, 30000, 40000])
plt.xlabel("Pozycje")
plt.ylabel("Wynagrodzenie")
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height}zł',
        ha='center',
        va='bottom'
    )
plt.show()
graph_5 = plt.figure()
plt.pie([ai_jobs_percentage, 100 - ai_jobs_percentage],labels=["Oferty dotyczące AI", "Pozostałe oferty"], autopct="%.2f%%", startangle=45, colors=["lime","#00A0FF"], explode=[0.1,0], shadow=True)
plt.title("% ofert dotyczących AI")
plt.show()
