import pandas as pd
from openpyxl import load_workbook
import plotly.express as px
from statistics import mean 
import os
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def score_list(filename):
    stu_names = get_sheets(filename)
    List = [None] * len(stu_names)
    for i in range(len(stu_names)):
        df = pd.read_excel(filename, sheet_name=stu_names[i])
        List[i] = df["score"].sum()
    return List

def Average(lst):
    return round(sum(lst) / len(lst),0)

def get_sheets(filename):
    """
    inputs -->
    filname : name of a .xlsx file

    returns -->
    names : a list of all sheet names in the .xlsx file mentioned excluding the Question_Paper sheet
    """
    xl = pd.ExcelFile(filename)
    names = xl.sheet_names[1:]
    return names


def get_xl_files():
    """
    inputs -->
    No inputs

    returns -->
    A list of names of all .xlsx files in the working directory 
    """
    extension = 'xlsx'
    all_files = glob.glob('*.{}'.format(extension))
    return all_files


def get_student_df(filename,student_name):
    """
    inputs -->
    filename : a .xlsx file (a particular test)
    student_name : the name of the student whose answer sheet is being read into a dataframe

    returns -->
    df : A dataframe which contains the student's reponses and scores for all questions in the mentioned test
    """
    df = pd.read_excel(filename, sheet_name=student_name)
    return df


def marks_split(df):
    """
    inputs -->
    df : A dataframe which contains the student's reponses and scores for all questions of a single test
    
    returns -->
    a pie chart  with his marks split into the three subjects in ["Biology","Chemistry","Physics"]
    """
    bio_score = df.loc[df['category'] == "Biology","score"].sum()
    chem_score = df.loc[df['category'] == "Chemistry","score"].sum()
    phy_score = df.loc[df['category'] == "Physics","score"].sum()
    fig = px.pie(values=[bio_score,chem_score,phy_score], names=["Biology","Chemistry","Physics"],
     color_discrete_map={"Biology":'green',
                          'Chemistry':'red',
                          'Physics':'royalblue'})
    return fig


def attempt_pattern(df):
    """
    inputs -->
    df : A dataframe which contains the student's reponses and scores for all questions of a single test
    
    returns -->
    a pie chart  with analysis of his attemt pattern i.e., split among correct,wrong and unattempted
    """
    unattempted = df.isnull().sum()["attempt"]
    wrong = df.loc[df['score'] == -1,"attempt"].count()
    right = df.loc[df['score'] == 4,"attempt"].count()
    fig = px.pie(values=[unattempted,wrong,right], names=["Unattempted","Incorrect","Correct"],
     color_discrete_map={"Unnatempted":'green',
                          'Incorrect':'red',
                          'Correct':'blue'})
    
    return fig


def quick_analysis_of_paper(df):
    """
    inputs -->
    df : A dataframe which contains the student's reponses and scores for all questions of a single test
    
    returns -->
    a sunburst chart which gives a quick and interactive combined (less detailed) visualization of the above two pie charts
    """
    df["count"] = [1]*len(df)
    fig = px.sunburst(df, path=['category',"score"], values= "count" )
    return fig

'''
def total_growth(name):
    all_files = get_xl_files()
    whole_df = pd.DataFrame()
    tests = [i[:-5] for i in all_files]
    your_scores = list()
    topper_scores = list()
    average_scores = list()
    for filename in all_files:
        temp = list()
        names = get_sheets(filename)
        for i in names:
            df = pd.read_excel(filename, sheet_name=i)
            temp.append(df["score"].sum())
        average_scores.append(mean(temp))
        topper_scores.append(max(temp))
        try:
            df = get_student_df(filename, name)
            your_scores.append(df["score"].sum())
        except:
            pass
    whole_df["test"] = tests
    whole_df["your_score"] = your_scores
    whole_df["average_score"] = average_scores
    whole_df["topper_score"] = topper_scores

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["average_score"],
            mode="markers+lines",
            name="Average Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["your_score"],
            mode="markers+lines",
            name="Your Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["topper_score"],
            mode="markers+lines",
            name="Topper Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Test Name", "Your Score", "Topper Score", "Average Score"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[whole_df.test, whole_df.your_score, whole_df.topper_score, whole_df.average_score],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text="Growth Comparison", hovermode='x'
    )

    return fig
'''
def total_growth(my_name):
    all_files = get_xl_files()
    all_files = [x for x in all_files if not x.startswith('~')]
    whole_df = pd.DataFrame()
    my_tests = []
    your_scores = list()
    topper_scores = list()
    average_scores = list()
    for filename in all_files:
        temp = list()
        names = get_sheets(filename)
        if my_name in names:
            my_tests.append(filename[:-5].upper())
            for i in names:
                df = pd.read_excel(filename, sheet_name=i)
                temp.append(df["score"].sum())

            average_scores.append(mean(temp))
            topper_scores.append(max(temp))

            df = get_student_df(filename, my_name)
            your_scores.append(df["score"].sum())

    whole_df["test"] = my_tests
    whole_df["your_score"] = your_scores
    whole_df["average_score"] = average_scores
    whole_df["topper_score"] = topper_scores

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["average_score"],
            mode="markers+lines",
            name="Average Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["your_score"],
            mode="markers+lines",
            name="Your Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["topper_score"],
            mode="markers+lines",
            name="Topper Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Test Name", "Your Score", "Topper Score", "Average Score"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[whole_df.test, whole_df.your_score, whole_df.topper_score, whole_df.average_score],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text="Growth Comparison", hovermode='x'
    )

    return fig


def subject_growth(name,subject):
    """
    inputs -->
    name : the name of the student who is currently logged in and whose growth / change has to be analyzed
    
    returns -->
    a figure which contains two vertical subplots (single variable / figure. NOT a tuple)
    row 1 : A table comparing yours,average and toppers growth on particular subjects (pcb) in all tests
    row 2 : a graph analyzing the same
    """
    all_files = get_xl_files()
    whole_df = pd.DataFrame()
    tests = [i[:-5] for i in all_files]
    your_scores = list()
    topper_scores = list()
    average_scores = list()
    for filename in all_files:
        temp =list()
        names = get_sheets(filename)
        for i in names :
            df = pd.read_excel(filename, sheet_name=i)
            sub_df = df[df['category'] == subject]
            temp.append(sub_df["score"].sum())
        average_scores.append(mean(temp))
        topper_scores.append(max(temp))
        try :
            df = get_student_df(filename,name)
            sub_df = df[df['category'] == subject]
            your_scores.append(sub_df["score"].sum())
        except :
            pass
    whole_df["test"] = tests
    whole_df["your_score"] = your_scores
    whole_df["average_score"] = average_scores
    whole_df["topper_score"] = topper_scores 
    

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
            [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["average_score"],
            mode="markers+lines",
            name="Average Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["your_score"],
            mode="markers+lines",
            name="Your Score"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["test"],
            y=whole_df["topper_score"],
            mode="markers+lines",
            name="Topper Score"
        ),
        row=2, col=1
    )


    fig.add_trace(
        go.Table(
            header=dict(
                values=["Test Name", "Your Score", "Topper Score","Average Score"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[whole_df.test,whole_df.your_score,whole_df.topper_score,whole_df.average_score],
                align = "left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text="Growth Comparison : {}".format(subject), hovermode='x'
    )

    return fig


def topper_comparison(filename,name):
    """
    inputs -->
    filename : a .xlsx file (the name of the file from where the amswer script of the student is being read)
    name : the name of the student who is currently logged in and whose comparison is being made
    
    returns -->
    a bar chart comparing the respective student's score with the average and topper's score in the whole test
    """
    names = get_sheets(filename)
    scores = list()
    for i in names :
        df = pd.read_excel(filename, sheet_name=i)
        scores.append(df["score"].sum())
    average = mean(scores)
    highest = max(scores)
    i = names.index(name)
    your_score = scores[i]
    temp_df = pd.DataFrame()
    temp_df["Score"]  = [highest,your_score,round(average,0)]
    temp_df["Paper"] = ["Topper Score","Your Score","Average Score"]
    fig = px.bar(temp_df,x="Paper", y="Score")
    return fig


def topper_subjectwise_comparison(filename,name,subject):
    """
    inputs -->
    filename : a .xlsx file (the name of the file from where the answer script of the student is being read)
    name : the name of the student who is currently logged in and whose comparison is being made
    subject : the subject on which comparison is to be made

    returns -->
    a bar chart comparing the respective student's score with the average and topper's score in 
    the particular subject of the test
    """
    xl = pd.ExcelFile(filename)
    names = xl.sheet_names[1:]
    scores = list()
    for i in names :
        df = pd.read_excel(filename, sheet_name=i)
        scores.append(df.loc[df['category'] == subject,"score"].sum())
    average = mean(scores)
    highest = max(scores)
    i = names.index(name)
    your_score = scores[i]
    temp_df = pd.DataFrame()
    temp_df["Score"]  = [highest,your_score,round(average,0)]
    temp_df["Paper"] = ["Topper Score","Your Score","Average Score"]
    fig = px.bar(temp_df,x="Paper", y="Score")
    return fig


def get_correct_rate(filename,q):
    """
    inputs -->
    filname : a .xlsx file (the name of the file from where the answer script of all the
    students is being read)
    q : the question number of the question whose correct rate in percentage is to be measured

    returns -->
    perc : a string representing the correct rate of the mentioned question in percentage
    """
    names = get_sheets(filename)
    correct = 0
    for i in names :
        df = get_student_df(filename,i)
        if df.loc[df['q'] == q,"score"].item() == 4:
            correct +=1
    percentage = correct/len(names) * 100
    perc = "{}%".format(round(percentage,2))
    return perc


def answer_comparsion(filename,name,subject = "all"):
    """
    inputs -->
    filename : a .xlsx file (the name of the file from where the answer script of all the
    students is being read)
    name : name of the student logged in and whose comparison is being made
    subject : Can take values from ["all","Biology","Chemistry","Physics"]
    if all, it performs the function for the whole question paper,otherwise for the specifies subject

    returns -->
    a figure containing a table  which compares your responses to the actual answers along with 
    correct rate % and score awarded
    NOTE : As this is from figure factory and not the general plotly it takes time to execute
    """
    df = get_student_df(filename,name)
    correct_rates = [get_correct_rate(filename,i) for i in df["q"]]
    df["correct_rates"] = correct_rates
    if subject == "all":
        fig = go.Figure(data=[go.Table(
        header=dict(values=["Question Number","Subject","Your Attempt","Actual Answer","Score Awarded","Correct Rate"],
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[df.q,df.category,df.attempt, df.actual, df.score,df.correct_rates],
                fill_color='lavender',
                align='center'))])
    else :
        sub_df = df[df['category'] == subject]
        fig = go.Figure(data=[go.Table(
        header=dict(values=["Question Number","Your Attempt","Actual Answer","Score Awarded","Correct Rate"],
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[sub_df.q,sub_df.attempt, sub_df.actual,sub_df.score,sub_df.correct_rates],
                fill_color='lavender',
                align='center'))])

    return fig
