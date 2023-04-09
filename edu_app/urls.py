"""edu_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as userviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', userviews.index),
    path('log', userviews.log_1),
    path('stud_log', userviews.stud_log),
    path('int_add', userviews.int_add),
    path('stud_reg', userviews.stud_reg),
    path('testing', userviews.testpage),
    path('inst1', userviews.viewint1),
    path('inst2', userviews.viewint2),
    path('inst3', userviews.viewint3),
    path('inst4', userviews.viewint4),
    path('neet1', userviews.viewtest1),
    path('neet2', userviews.viewtest2),
    path('neet3', userviews.viewtest3),
    path('neet4', userviews.viewtest4),
    path('view1', userviews.view1),
    path('view2', userviews.view2),
    path('view3', userviews.view3),
    path('view4', userviews.view4),
    path('tech_log', userviews.tech_log),
    path('tech_reg', userviews.tech_reg),
    path('stud_list', userviews.stud_list),
    path('stud_check', userviews.stud_check),
    path('marks_split1.html', userviews.marks_split1),
    path('marks_split2.html', userviews.marks_split2),
    path('marks_split3.html', userviews.marks_split3),
    path('marks_split4.html', userviews.marks_split4),
    path('quick_fig1.html', userviews.quick_fig1),
    path('quick_fig2.html', userviews.quick_fig2),
    path('quick_fig3.html', userviews.quick_fig3),
    path('quick_fig4.html', userviews.quick_fig4),
    path('att_pat1.html', userviews.att_pat1),
    path('att_pat2.html', userviews.att_pat2),
    path('att_pat3.html', userviews.att_pat3),
    path('att_pat4.html', userviews.att_pat4),
    path('total_g.html', userviews.total_gro),
    path('top_comp1.html', userviews.top_comp1),
    path('top_comp2.html', userviews.top_comp2),
    path('top_comp3.html', userviews.top_comp3),
    path('top_comp4.html', userviews.top_comp4),
    path('all_data', userviews.all_data),
    path('all1', userviews.all1),
    path('all2', userviews.all2),
    path('all3', userviews.all3),
    path('all4', userviews.all4),
    path('subject', userviews.subject),
    path('bio', userviews.bio),
    path('phy', userviews.phy),
    path('chem', userviews.chem),
]
