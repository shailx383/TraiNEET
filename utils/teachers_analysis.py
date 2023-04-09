import pandas as pd
from openpyxl import load_workbook
import plotly.express as px
from statistics import mean 
import os
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.student_analysis import *
import pickle

def full_score_comparison(filename):
    """
    inputs -->
    filename : a .xlsx file wich contains all the test details , i.e., the question paper along with
    all the students answer scripts

    returns -->
    A bar chart comparing all the students scores together 
    """
    names = get_sheets(filename)
    scores = list()
    for i in names :
        df = pd.read_excel(filename, sheet_name=i)
        scores.append(df["score"].sum())
    temp_df = pd.DataFrame()
    temp_df["Students"]  = names
    temp_df["Score"] = scores
    fig = px.bar(temp_df,x="Students", y="Score")
    return fig


def cluster_comparison(subject):
    model = pickle.load(open("kmeans.pkl", "rb"))

    student_dict = di = get_student_dict(subject)

    kmeans_df = pd.DataFrame()
    kmeans_df["student"] = list(student_dict.keys())
    kmeans_df["min"] = [min(i) for i in list(student_dict.values())]
    kmeans_df["avg"] = [mean(i) for i in list(student_dict.values())]
    X = kmeans_df.iloc[:, [1, 2]].values
    y_kmeans = model.predict(X)
    clusters = ["Strong" if i == 1 else "Weak" if i == 2 else "Average" for i in y_kmeans]
    visual_df = pd.DataFrame()
    visual_df["minimum_score"] = X[:, 0]
    visual_df["average_score"] = X[:, 1]
    visual_df["cluster"] = clusters

    fig = px.scatter(visual_df, x="minimum_score", y="average_score", color="cluster")
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text="Categorizing students by strength in : {}".format(subject)
    )
    return fig


def get_student_dict(subject):
    files = get_xl_files()
    names = get_sheets(files[0])
    student_dict = {}
    for i in names:
        exec("%s = %s" % (i, list()))
        for filename in files:
            try:
                df = get_student_df(filename, i)
                df = df[df['category'] == subject]
                exec("%s.append(%s)" % (i, df["score"].sum()))
            except:
                pass
        student_dict[i] = eval(i)

    return student_dict