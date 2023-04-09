import pandas as pd
from openpyxl import load_workbook


def get_questions(filename):
    """
    inputs -->
    filename : an .xlsx file with a sheet named Question_Papaer in required format 
    (file.xlsx has to be in the same directory as module from where function is called)
    
    returns -->
    A list of all question in the question paper , no null values

    """
    df = pd.read_excel(filename,sheet_name='Question_Paper')
    return list(df["questions"])

def get_options(filename):
    """
    inputs -->
    filename : an .xlsx file with a sheet named Question_Papaer in required format 
    (file.xlsx has to be in the same directory as module from where function is called)
    
    returns -->
    tuple of 4 lists :-
    A : list of all option 1s of all questions returned by get_questions()
    B : list of all option 2s of all questions returned by get_questions()
    C : list of all option 3s of all questions returned by get_questions()
    D : list of all option 4s of all questions returned by get_questions()
    All indexes are matching
    """
    df = pd.read_excel(filename,sheet_name='Question_Paper')
    A = list(df["option_1"])
    B = list(df["option_2"])
    C = list(df["option_3"])
    D = list(df["option_4"])
    return A,B,C,D

def create_stu_df(filename):
    """
    inputs -->
    filename : an .xlsx file with a sheet named Question_Papaer in required format 
    (file.xlsx has to be in the same directory as module from where function is called)
    
    returns -->
    name : the student's name whose answer script is made
    stu_df : a temporary dataframe used to modify one's answers until the paper is submitted
    """
    df = pd.read_excel(filename,sheet_name='Question_Paper')
    l = len(df)
    answers = [None]*l
    correct = [0]*l
    actual = df["answers"]
    q_nos = [i+1 for i in df.index]
    category = df["category"]
    stu_df = pd.DataFrame({
        "q":q_nos,
        "attempt": answers,
        "actual":actual,
        "score": correct,
        "category":category})
    return stu_df


def attempt(df,q,ans):
    """
    inputs -->
    df : the dataframe which gets edited after every answer is marked 
    (use the stu_df which was returned by the create_stu_df() function only)
    q : the question number which is being edited 
    ans : the answer/option selected by student (make sure it is either 1,2,3,4 or None(if no answer marked))
    
    returns -->
    Nothing, just edits the temporary dataframe for every attempt
    """
    df.loc[df['q'] == q, 'attempt'] = ans
    if ans == df.loc[df['q'] == q, 'actual'].item() :
        df.loc[df['q'] == q, 'score'] = 4
    if ans != df.loc[df['q'] == q, 'actual'].item() :
        df.loc[df['q'] == q, 'score'] = -1
    if ans == None :
        df.loc[df['q'] == q, 'score'] = 0



def submit(df,name,filename):
    """
    inputs -->
    df : the dataframe which gets edited after every answer is marked  
    (here stu_df after all answers marked or time runs out)
    name : students name (one who is logged in / selected by teacher)
    filename : the .xlsx file from where the question paper is being read
    

    returns -->
    None
    This function creates a new sheet with the same name as student with all his answers
    and respective score per answer in the same .xlsx file as the Question_Paper (as mentioned in filename)
    """

    path = r'{}'.format(filename)
    book = load_workbook(path)
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)     
        df.to_excel(writer, name)  
        writer.save() 