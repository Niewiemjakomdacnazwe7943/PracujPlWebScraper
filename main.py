from data import data_program
import sys
import subprocess
import streamlit as st
import json
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Analiza rynku pracy",
    page_icon="https://uisystem.gpcdn.pl/root/icon/pracuj/1.0.0/basic.ico",
)
st.markdown(
    """
    <style>
    body {
        background-color: #FF0000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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


def graph_work_modes(data):
    plt.title("Praca: Stacjonarna vs Hybrydowa vs Zdalna", fontsize=150) # TO DO: zmniejsz fontsize by napis nie byl uciety
    plt.pie(data['values'], labels=data['labels'], autopct="%.2f%%", startangle=45, colors=["#00A0FF", "red", "green"], pctdistance=0.65, textprops={'fontsize': 120})


def graph_languages(data):
    plt.title("Najbardziej poszukiwane języki programowania", fontsize=30)
    plt.barh(data['labels'], data['values'], edgecolor="black", lw=0.005, color="darkgreen")
    plt.tick_params(axis="both", labelsize=28)
    plt.xlabel("Amount of job offers", fontsize=30)
    plt.ylabel("Programming language", fontsize=30)


def graph_positions(data):
    plt.title("Najbardziej poszukiwane stanowiska")
    plt.barh(data['labels'], data['values'], color="blue", edgecolor="black", lw=2)
    plt.tick_params(axis="y", labelsize=8)


def graph_average_salary(data):
    plt.title("Średnia płaca na stanowiskach: Junior, Mid, Senior")
    bars = plt.bar(data['labels'], data['values'], color="purple", width=0.2, edgecolor="black", lw=2)
    plt.yticks([10000, 20000, 30000, 40000])
    plt.xlabel("Pozycje")
    plt.ylabel("Wynagrodzenie")
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,height,f'{height}zł',ha='center',va='bottom')


def graph_ai_jobs(data):
    plt.pie([data, 100 - data], labels=["Oferty dotyczące AI", "Pozostałe oferty"], autopct="%.2f%%", startangle=45, colors=["lime", "#00A0FF"], explode=[0.1, 0], shadow=True)
    plt.title("% ofert dotyczących AI")


analysis_data = load_analysis_data()
programming_languages = analysis_data[0]
work_modes = analysis_data[1]
positions = analysis_data[2]
ai_jobs_percentage = analysis_data[3]
average_position_salaries = analysis_data[4]
st.title("Analiza rynku pracy na Pracuj.pl", text_alignment="center")
with st.container(border=True):
    cell1, cell2, cell3 = st.columns(3, gap="large")
    cell4, cell5, cell6 = st.columns(3, gap="large")
    with cell4:
        fig, ax = plt.subplots(figsize=(40, 40))
        graph_work_modes(work_modes)
        st.pyplot(fig)
    with cell5:
        fig, ax = plt.subplots(figsize=(10, 10))
        graph_languages(programming_languages)
        st.pyplot(fig)
