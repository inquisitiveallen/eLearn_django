import datetime
import json
from locale import format

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

# Create your views here.
# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import OrderForm, InterestForm, RegisterForm
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    top_courses = Course.objects.all().order_by('-price')[:5]
    browserCLose = request.session.get_expire_at_browser_close()
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 0
    # response = HttpResponse()
    # heading1 = '<p>' + '<b>' + 'List of topics: ' + '</b>' + '</p>'
    # response.write(heading1)
    # for topic in top_list:
    #  para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
    #  response.write(para)
    # top_courses = Course.objects.all().order_by('-price')[:5]
    # heading2 = '<p>' + '<b>' + 'List of courses: ' + '</b>' + '</p>'
    # response.write(heading2)
    # for course in top_courses:
    #  para1 = '<p>' + str(course) + '</p>'
    #  if course.for_everyone:
    #   para1 = '<p>' + str(course) + '<i>' + ' - This Course is For Everyone!' + '</i>' + '</p>'
    #   # para1 = para1 + 'This Course is For Everyone!'
    #  else:
    #   para1 = '<p>' + str(course) + '<i>' + ' - This Course is Not For Everyone!' + '</i>' + '</p>'
    #   # para1 = para1 + 'This Course is Not For Everyone!'
    #  # para1 = '<p>' + str(course) + '</p>'
    #  response.write(para1)
    # return response
    return render(request, 'myapp/index.html', {'top_list': top_list, 'top_course': top_courses,
                                                'last_login': last_login, 'browserCLose': browserCLose})


def about(request):
    about_visits = request.COOKIES.get('about_visits')
    if about_visits:
        cookie_count = int(about_visits) + 1
    else:
        cookie_count = 1
    about_response = render(request, 'myapp/about.html', {'count': cookie_count})
    about_response.set_cookie(key='about_visits', value=cookie_count, max_age=300)
    return about_response


# def about(request):
#     # about_response = HttpResponse()
#     # about_content = '<p>' + '<b>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</b>' + '</p> '
#     # about_response.write(about_content)
#     # # return HttpResponse('This is an E-learning Website! Search our Topics to find all available Courses.')
#     # return about_response
#     return render(request, 'myapp/about.html')


def detail(request, top_no):
    # t = get_object_or_404(Topic,id=top_no)
    # t_category = t.get_category_display()
    # courses = Course.objects.filter(topic=top_no)
    # detail_response = HttpResponse()
    # heading1 = '<p>' + '<b>' + 'Category of the topic: ' + '</b>' + '</p>'
    # detail_response.write(heading1)
    # t_para = '<p>' + str(t_category) + '</p>'
    # detail_response.write(t_para)
    # heading2 = '<p>' + '<b>' + 'List of courses of the topic: ' + '</b>' + '</p>'
    # detail_response.write(heading2)
    # for course in courses:
    #  t_para = '<p>' + str(course) + '</p>'
    #  detail_response.write(t_para)
    # return detail_response
    t = get_object_or_404(Topic, id=top_no)
    t_category = t.get_category_display()
    courses = Course.objects.filter(topic=top_no)
    # return render(request, 'myapp/detail0.html', {'topic_category': t_category})
    return render(request, 'myapp/detail.html', {'topic_name': t, 'topic_category': t_category, 'courses': courses})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                if order.course.price > 150:
                    order.course.discount()
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    top_list = Topic.objects.all().order_by('id')[:10]
    top_courses = Course.objects.all().order_by('-price')[:5]
    course_detail = Course.objects.get(id=cour_id)
    interested = course_detail.interested
    if request.method == 'POST':
        myform = InterestForm(request.POST)
        if myform.is_valid():
            form_interested = myform.cleaned_data['interested']
            if int(form_interested) == 1:
                interested += 1
                course_detail.interested = interested
                course_detail.save()
                return render(request, 'myapp/index.html', {'top_list': top_list, 'top_course': top_courses})
                # msg = 'Your course has been ordered successfully.'
    else:
        myform = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': myform, 'course_name': course_detail})
    # return render(request, 'myapp/coursedetail.html', {'course_name': course_detail})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            # return HttpResponse("You are logged in")
        request.session.set_test_cookie()

        now = datetime.datetime.now()
        json_str = json.dumps(now, default=str)
        request.session['last_login'] = json_str
        request.session.set_expiry(3600)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    # del request.session['last_login']
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/myapp/login/')
def myaccount(request):
    username = request.user

    try:

        curr_student = get_object_or_404(Student, username=username)
        sid = curr_student.id
        course_ordered = Order.objects.filter(student=sid)
        topic_interested = curr_student.interested_in.all()
        return render(request, 'myapp/myaccount.html',
                      {'student': curr_student, 'orders': course_ordered, 'topics': topic_interested})

    except:
        return render(request, 'myapp/myaccount.html')


# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             #messages.success(request, "Registration successful.")
#             return HttpResponseRedirect(reverse('login'))
#         else:
#             return HttpResponse('Registration Unsuccessful. Invalid Information')
#     form = RegisterForm()
#     return render(request, 'myapp/register.html', context={'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def myorders(request):
    username = request.user

    try:
        curr_student = get_object_or_404(Student, username=username)
        sid = curr_student.id

        course_ordered = Order.objects.filter(student=sid)
        return render(request, 'myapp/myorders.html',
                      {'student': curr_student, 'orders': course_ordered})

    except:
        return render(request, 'myapp/myorders.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('UserEmail')
        password = "passwordNew"
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        send_mail(
            "New Password",  # subject
            password,  # message
            'lancerguidewindsor@gmail.com',  # from
            [email],  # to
        )
        return HttpResponse("We have emailed you a new password")
    else:
        return render(request, 'myapp/passwordreset.html')
