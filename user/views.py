from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from user.models import att_1 as a1
from user.models import att_2 as a2
from user.models import att_3 as a3
from user.models import att_4 as a4
from utils import answering as a
from utils import student_analysis as sa
from utils import teachers_analysis as ta
import plotly.io as pio
import pandas as pd
from openpyxl import load_workbook
import plotly.express as px
from statistics import mean
import os
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py


# Create your views here.
# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader                                                                                                             

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''

    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser


def index(request):
    '''Render the index page'''

    if mobileBrowser(request):
        t = loader.get_template('START.html')
    else:
        t = loader.get_template('START.html')

    c = {}  # normally your page data would go here

    return HttpResponse(t.render(c))

def log_1(request):
    if request.method=='GET':
        return render(request,'START.html')

def stud_log(request):
    if request.method=='GET':
        return render(request,'stud_log.html')
    elif request.method=='POST':
        user = request.POST['username']
        pwd = request.POST['passwd']
        user_int = User.objects.get(username = user)
        print(user_int.first_name)
        total_g = sa.total_growth(user_int.first_name)
        pio.write_html(total_g, file="total_g.html", auto_open=False)
        if request.GET['b'] == 'ck':
            var = User.objects.get(username = user)
            if var.is_staff:
                return render(request, 'err2.html')
            else:
                user = authenticate(request, username=user, password=pwd)
                if user is not None:
                    log(request,user)
                    logged_in = request.user
                    return render(request, 'stud_home.html', {'logged_in':logged_in} )
                else:
                    return render(request, 'login_error.html')

def int_add(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method =='POST':
        return render(request, 'stud_reg.html')

def stud_reg(request):
    if request.method=='GET':
        return render(request,'stud_reg.html')
    elif request.method=='POST':
        username=request.POST['username']
        passwd=request.POST['passwd']
        phno=request.POST['phno']
        email=request.POST['email']
        f_name=request.POST['f_name']
        l_name = request.POST['l_name']
        if request.GET['a'] == 'db':
            user=User.objects.create_user(username,email,passwd)
            user.first_name = f_name
            user.last_name = l_name
            user.save()
            return render(request,'START.html')
        else:
            return render(request,'homepage.html')
    
def testpage(request):
    if request.method=='GET':
        try:
            val1 = a1.objects.get(user = request.user.id)
        except:
            val1 = None
        try:
            val2 = a2.objects.get(user=request.user.id)
        except:
            val2 = None
        try:
            val3 = a3.objects.get(user=request.user.id)
        except:
            val3 = None
        try:
            val4 = a4.objects.get(user=request.user.id)
        except:
            val4 = None
        return render(request,'testlist.html',{'val1':val1,'val2':val2,'val3':val3,'val4':val4})

def viewint1(request):
    if request.method == 'GET':
        return render(request, 'instr1.html')

def viewint2(request):
    if request.method == 'GET':
        return render(request, 'instr2.html')

def viewint3(request):
    if request.method == 'GET':
        return render(request, 'instr3.html')

def viewint4(request):
    if request.method == 'GET':
        return render(request, 'instr4.html')

def viewtest1(request):
    if request.method == 'GET':
        q_list = a.get_questions('neet1.xlsx')
        opt1, opt2, opt3, opt4 = a.get_options('neet1.xlsx')
        q_no = {'q'+str(i + 1): {'q': q_list[i], 'o1': opt1[i], 'o2': opt2[i], 'o3': opt3[i], 'o4': opt4[i]} for i in range(len(q_list))}
        return render(request, 'neet1.html', {'q_no':q_no})
    elif request.method == 'POST':
        df_1 = a.create_stu_df('neet1.xlsx')
        name = request.user.first_name
        main_lst=[]
        for i in range(1,61):
            try:
                main_lst.append(int(request.POST['q%s'%(i)]))
            except:
                main_lst.append(None)
        for q in df_1['q']:
            a.attempt(df_1, q, main_lst[q-1])
        a.submit(df_1, name, 'neet1.xlsx')
        if request.GET['b']=='s2':
            t_1 = a1()
            t_1.test_name = "neet1.xlsx"
            t_1.user = request.user
            t_1.save()
        logged_in = request.user
        return render(request, 'stud_home.html',{'logged_in':logged_in})

 
def viewtest2(request):
    if request.method == 'GET':
        q_list = a.get_questions('neet2.xlsx')
        opt1, opt2, opt3, opt4 = a.get_options('neet2.xlsx')
        q_no = {'q'+str(i + 1): {'q': q_list[i], 'o1': opt1[i], 'o2': opt2[i], 'o3': opt3[i], 'o4': opt4[i]} for i in range(len(q_list))}
        return render(request, 'neet2.html', {'q_no':q_no})
    elif request.method == 'POST':
        df_2 = a.create_stu_df('neet2.xlsx')
        name = request.user.first_name
        main_lst=[]
        for i in range(1,61):
            try:
                main_lst.append(int(request.POST['q%s'%(i)]))
            except:
                main_lst.append(None)
        for q in df_2['q']:
            a.attempt(df_2, q, main_lst[q-1])
        a.submit(df_2, name, 'neet2.xlsx')
        if request.GET['b']=='s2':
            t_1 = a2()
            t_1.test_name = "neet2.xlsx"
            t_1.user = request.user
            t_1.save()
        logged_in = request.user
        return render(request, 'stud_home.html',{'logged_in':logged_in})


def viewtest3(request):
    if request.method == 'GET':
        q_list = a.get_questions('neet3.xlsx')
        opt1, opt2, opt3, opt4 = a.get_options('neet3.xlsx')
        q_no = {'q'+str(i + 1): {'q': q_list[i], 'o1': opt1[i], 'o2': opt2[i], 'o3': opt3[i], 'o4': opt4[i]} for i in range(len(q_list))}
        return render(request, 'neet3.html', {'q_no':q_no})
    elif request.method == 'POST':
        df_3 = a.create_stu_df('neet3.xlsx')
        name = request.user.first_name
        main_lst=[]
        for i in range(1,61):
            try:
                main_lst.append(int(request.POST['q%s'%(i)]))
            except:
                main_lst.append(None)
        for q in df_3['q']:
            a.attempt(df_3, q, main_lst[q-1])
        a.submit(df_3, name, 'neet3.xlsx')
        if request.GET['b']=='s2':
            t_1 = a3()
            t_1.test_name = "neet3.xlsx"
            t_1.user = request.user
            t_1.save()
        logged_in = request.user
        return render(request, 'stud_home.html',{'logged_in':logged_in})


def viewtest4(request):
    if request.method == 'GET':
        q_list = a.get_questions('neet4.xlsx')
        opt1, opt2, opt3, opt4 = a.get_options('neet4.xlsx')
        q_no = {'q'+str(i + 1): {'q': q_list[i], 'o1': opt1[i], 'o2': opt2[i], 'o3': opt3[i], 'o4': opt4[i]} for i in range(len(q_list))}
        return render(request, 'neet4.html', {'q_no':q_no})
    elif request.method == 'POST':
        df_4 = a.create_stu_df('neet4.xlsx')
        name = request.user.first_name
        main_lst=[]
        for i in range(1,61):
            try:
                main_lst.append(int(request.POST['q%s'%(i)]))
            except:
                main_lst.append(None)
        for q in df_4['q']:
            a.attempt(df_4, q, main_lst[q-1])
        a.submit(df_4, name, 'neet4.xlsx')
        if request.GET['b']=='s2':
            t_1 = a4()
            t_1.test_name = "neet4.xlsx"
            t_1.user = request.user
            t_1.save()
        logged_in = request.user
        return render(request, 'stud_home.html',{'logged_in':logged_in})

def view1(request):
    if request.method == 'GET':
        df_1 = sa.get_student_df('neet1.xlsx',request.user.first_name)
        marks_fig = sa.marks_split(df_1)
        pio.write_html(marks_fig, file="marks_split1.html", auto_open = False)
        quick_fig = sa.quick_analysis_of_paper(df_1)
        pio.write_html(quick_fig, file="quick_fig1.html", auto_open=False)
        att_pat = sa.attempt_pattern(df_1)
        pio.write_html(att_pat, file="att_pat1.html", auto_open=False)
        top_comp = sa.topper_comparison('neet1.xlsx', request.user.first_name)
        pio.write_html(top_comp, file="top_comp1.html", auto_open=False)
        bio_score = df_1.loc[df_1['category'] == "Biology", "score"].sum()
        chem_score = df_1.loc[df_1['category'] == "Chemistry", "score"].sum()
        phy_score = df_1.loc[df_1['category'] == "Physics", "score"].sum()
        return render(request, 'view1.html',
                      {'total': df_1['score'].sum(), 'bio': bio_score, 'chem': chem_score, 'phy': phy_score})

def view2(request):
    if request.method == 'GET':
        df_2 = sa.get_student_df('neet2.xlsx',request.user.first_name)
        marks_fig = sa.marks_split(df_2)
        pio.write_html(marks_fig, file="marks_split2.html", auto_open = False)
        quick_fig = sa.quick_analysis_of_paper(df_2)
        pio.write_html(quick_fig, file="quick_fig2.html", auto_open=False)
        att_pat = sa.attempt_pattern(df_2)
        pio.write_html(att_pat, file="att_pat2.html", auto_open=False)
        top_comp = sa.topper_comparison('neet2.xlsx', request.user.first_name)
        pio.write_html(top_comp, file="top_comp2.html", auto_open=False)
        bio_score = df_2.loc[df_2['category'] == "Biology", "score"].sum()
        chem_score = df_2.loc[df_2['category'] == "Chemistry", "score"].sum()
        phy_score = df_2.loc[df_2['category'] == "Physics", "score"].sum()
        return render(request, 'view2.html',
                      {'total': df_2['score'].sum(), 'bio': bio_score, 'chem': chem_score, 'phy': phy_score})

def view3(request):
    if request.method == 'GET':
        df_3 = sa.get_student_df('neet3.xlsx',request.user.first_name)
        marks_fig = sa.marks_split(df_3)
        pio.write_html(marks_fig, file="marks_split3.html", auto_open = False)
        quick_fig = sa.quick_analysis_of_paper(df_3)
        pio.write_html(quick_fig, file="quick_fig3.html", auto_open=False)
        att_pat = sa.attempt_pattern(df_3)
        pio.write_html(att_pat, file="att_pat3.html", auto_open=False)
        top_comp = sa.topper_comparison('neet3.xlsx', request.user.first_name)
        pio.write_html(top_comp, file="top_comp3.html", auto_open=False)
        bio_score = df_3.loc[df_3['category'] == "Biology", "score"].sum()
        chem_score = df_3.loc[df_3['category'] == "Chemistry", "score"].sum()
        phy_score = df_3.loc[df_3['category'] == "Physics", "score"].sum()
        return render(request, 'view3.html',
                      {'total': df_3['score'].sum(), 'bio': bio_score, 'chem': chem_score, 'phy': phy_score})

def view4(request):
    if request.method == 'GET':
        df_4 = sa.get_student_df('neet4.xlsx',request.user.first_name)
        marks_fig = sa.marks_split(df_4)
        pio.write_html(marks_fig, file="marks_split4.html", auto_open = False)
        quick_fig = sa.quick_analysis_of_paper(df_4)
        pio.write_html(quick_fig, file="quick_fig4.html", auto_open=False)
        att_pat = sa.attempt_pattern(df_4)
        pio.write_html(att_pat, file="att_pat4.html", auto_open=False)
        top_comp = sa.topper_comparison('neet4.xlsx', request.user.first_name)
        pio.write_html(top_comp, file="top_comp4.html", auto_open=False)
        bio_score = df_4.loc[df_4['category'] == "Biology", "score"].sum()
        chem_score = df_4.loc[df_4['category'] == "Chemistry", "score"].sum()
        phy_score = df_4.loc[df_4['category'] == "Physics", "score"].sum()
        return render(request, 'view4.html', {'total':df_4['score'].sum(), 'bio':bio_score, 'chem':chem_score, 'phy':phy_score})

def tech_log(request):
    if request.method=='GET':
        return render(request,'tech_log.html')
    elif request.method=='POST':
        user = request.POST['username']
        pwd = request.POST['passwd']
        if request.GET['b'] == 'ck':
            var = User.objects.get(username = user)
            if var.is_staff:
                user = authenticate(request, username=user, password=pwd)
                if user is not None:
                    log(request,user)
                    logged_in = request.user
                    return render(request, 'tech_home.html', {'logged_in':logged_in} )
                else:
                    return render(request, 'login_error.html')
            else:
                return render(request, 'err1.html')
    

def tech_reg(request):
    if request.method=='GET':
        return render(request,'tech_reg.html')
    elif request.method=='POST':
        username=request.POST['username']
        passwd=request.POST['passwd']
        phno=request.POST['phno']
        email=request.POST['email']
        f_name=request.POST['f_name']
        l_name = request.POST['l_name']
        if request.GET['a'] == 'db':
            user=User.objects.create_user(username, email, passwd, is_staff='True')
            user.first_name = f_name
            user.last_name = l_name
            user.save()
            return render(request,'START.html')
        else:
            return render(request,'homepage.html')

def stud_list(request):
    if request.method=='GET':
        l = []
        vals = User.objects.all()
        for i in vals:
            if i.is_staff:
                pass
            else:
                l.append(i)
        print(l)
        return render(request,'stud_list.html',{'stud':l})


def stud_check(request):
    if request.method == 'GET':
        return render(request, 'stud_check.html')
    elif request.method=='POST':
        user = request.POST['username']
        pwd = request.POST['passwd']
        if request.GET['b'] == 'ck':
            var = User.objects.get(username=user)
            if var.is_staff:
                return render(request, 'err3.html')
            else:
                user = authenticate(request, username=user, password=pwd)
                if user is not None:
                    log(request, user)
                    logged_in = request.user
                    try:
                        val1 = a1.objects.get(user=request.user.id)
                    except:
                        val1 = None
                    try:
                        val2 = a2.objects.get(user=request.user.id)
                    except:
                        val2 = None
                    try:
                        val3 = a3.objects.get(user=request.user.id)
                    except:
                        val3 = None
                    try:
                        val4 = a4.objects.get(user=request.user.id)
                    except:
                        val4 = None
                    print(val1,val2,val3,val4)
                    return render(request, 'testlist_tech.html', {'logged_in': logged_in, 'val1':val1,'val2':val2,'val3':val3,'val4':val4})
                else:
                    return render(request, 'login_error.html')


def marks_split1(request):
    if request.method == 'GET':
        return render(request, 'marks_split1.html')

def marks_split2(request):
    if request.method == 'GET':
        return render(request, 'marks_split2.html')

def marks_split3(request):
    if request.method == 'GET':
        return render(request, 'marks_split3.html')

def marks_split4(request):
    if request.method == 'GET':
        return render(request, 'marks_split4.html')

def quick_fig1(request):
    if request.method == 'GET':
        return render(request, 'quick_fig1.html')

def quick_fig2(request):
    if request.method == 'GET':
        return render(request, 'quick_fig2.html')

def quick_fig3(request):
    if request.method == 'GET':
        return render(request, 'quick_fig3.html')

def quick_fig4(request):
    if request.method == 'GET':
        return render(request, 'quick_fig4.html')

def att_pat1(request):
    if request.method == 'GET':
        return render(request, 'att_pat1.html')

def att_pat2(request):
    if request.method == 'GET':
        return render(request, 'att_pat2.html')

def att_pat3(request):
    if request.method == 'GET':
        return render(request, 'att_pat3.html')

def att_pat4(request):
    if request.method == 'GET':
        return render(request, 'att_pat4.html')

def total_gro(request):
    if request.method == 'GET':
        return render(request, 'total_g.html')

def top_comp1(request):
    if request.method == 'GET':
        return render(request, 'top_comp1.html')

def top_comp2(request):
    if request.method == 'GET':
        return render(request, 'top_comp2.html')

def top_comp3(request):
    if request.method == 'GET':
        return render(request, 'top_comp3.html')

def top_comp4(request):
    if request.method == 'GET':
        return render(request, 'top_comp4.html')

def ans_comp1(request):
    if request.method == 'GET':
        return render(request, 'top_comp1.html')

def ans_comp2(request):
    if request.method == 'GET':
        return render(request, 'top_comp2.html')

def ans_comp3(request):
    if request.method == 'GET':
        return render(request, 'top_comp3.html')


def all_data(request):
    if request.method == 'GET':
        return render(request, 'all_data.html')

def all1(request):
    if request.method == 'GET':
        full_fig = ta.full_score_comparison('neet1.xlsx')
        pio.write_html(full_fig, file="full_fig1.html", auto_open=False)
        return render(request, 'full_fig1.html')

def all2(request):
    if request.method == 'GET':
        full_fig = ta.full_score_comparison('neet2.xlsx')
        pio.write_html(full_fig, file="full_fig2.html", auto_open=False)
        return render(request, 'full_fig2.html')

def all3(request):
    if request.method == 'GET':
        full_fig = ta.full_score_comparison('neet3.xlsx')
        pio.write_html(full_fig, file="full_fig3.html", auto_open=False)
        return render(request, 'full_fig3.html')

def all4(request):
    if request.method == 'GET':
        full_fig = ta.full_score_comparison('neet4.xlsx')
        pio.write_html(full_fig, file="full_fig4.html", auto_open=False)
        return render(request, 'full_fig4.html')

def subject(request):
    if request.method == 'GET':
        return render(request, 'subjects.html')

def bio(request):
    if request.method == 'GET':
        bio_fig = ta.cluster_comparison("Biology")
        pio.write_html(bio_fig, file="bio_fig.html", auto_open=False)
        return render(request, 'bio_fig.html')

def chem(request):
    if request.method == 'GET':
        bio_fig = ta.cluster_comparison("Chemistry")
        pio.write_html(bio_fig, file="chem_fig.html", auto_open=False)
        return render(request, 'chem_fig.html')

def phy(request):
    if request.method == 'GET':
        bio_fig = ta.cluster_comparison("Physics")
        pio.write_html(bio_fig, file="phy_fig.html", auto_open=False)
        return render(request, 'phy_fig.html')





        









            
    
