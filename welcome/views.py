from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import requests
from django.core.mail import send_mail
from django.contrib import messages
from .models import User, Schedule, Request, classRequest

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'welcome/index.html'
    def get_queryset(self):
        return "index success"


def index(request):
    if request.method=='POST':
        name = request.POST.get('cf-name')
        about = request.POST.get('cf-about')
        email = request.POST.get('cf-email')
        subject = request.POST.get('cf-number')
        message = request.POST.get('cf-message')

        data = {
            'name': name,
            'email': email,
            'about': about,
            'subject': subject,
            'message': message
        }
        message = '''
        From:\n\t\t{}\n
        Email:\n\t\t{}\n
        About:\n\t\t{}\n
        Subject:\n\t\t{}\n
        Message:\n\t\t{}\n
        '''.format(data['name'], data['email'], data['about'], data['subject'], data['message'])
        send_mail('Tutor Me Contact Form', message, 'tutormedjango@gmail.com', ['tutormedjango@gmail.com']) 
        messages.success(request, 'Your message has been sent successfully!')

    return render(request, 'welcome/index.html', {})

class selectTypeView(generic.ListView):
    template_name = 'welcome/selectType.html'
    def get_queryset(self):
        return "selectType success"

class tutorView(generic.ListView):
    template_name = 'welcome/tutor.html'
    context_object_name = 'requests_list'
    def get_queryset(self):
        return Request.objects.all()

class tutorRequestsView(generic.ListView):
    template_name = 'welcome/tutorRequests.html'
    context_object_name = 'requests_list'
    def get_queryset(self):
          return classRequest.objects.all().order_by('-upvotes')

class studentView(generic.ListView):
    template_name = 'welcome/student.html'
    context_object_name = 'requests_list'
    def get_queryset(self):
        return Request.objects.all()
    
class changeRateView(generic.ListView):
    template_name = 'welcome/changeRate.html'
    def get_queryset(self):
        return 'changeRate success'

class addBioView(generic.ListView):
    template_name = 'welcome/addBio.html'
    def get_queryset(self):
        return 'addBio success'

class selectClassView(generic.ListView):
    template_name = 'welcome/selectClasses.html'

    def get_context_data(self, **kwargs):
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232'
        res = requests.get(url)
        resJson = res.json()
        context = super().get_context_data(**kwargs)
        context['subjects'] = resJson['subjects']
        return context
    def get_queryset(self):
        return 'select Class success'

def findClass(request):
    model = User
    try:
        crsSubject = request.POST['class']
    except (KeyError, User.DoesNotExist):
        return render(request, 'welcome/selectClasses.html', {
            'comments': User,
            'error_message': "Add all necessary fields",
        })
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + crsSubject  + '&page=1'
    if request.POST['crsNum'] != "":
        url += '&catalog_nbr=' + request.POST['crsNum']
    classes = requests.get(url).json()
    seen = []
    classesFiltered = []
    for x in classes:
        if x['catalog_nbr'] not in seen:
            seen.append(x['catalog_nbr'])
            classesFiltered.append(x)
    return render(request,'welcome/listClasses.html',{'classesFiltered' : classesFiltered})

def addToSchedule(request, user_id):
    if request.user.type == 'tut':
        user = User.objects.get(pk = user_id)
        try:
            schedule = Schedule.objects.get(User = user)
        except Schedule.DoesNotExist:
            schedule = Schedule(schedule = [], tutorTimings = [], User = user)
            schedule.save()
        list = request.POST.getlist('class')
        for x in list:
            if(x not in schedule.schedule):
                schedule.schedule.append(x)
                schedule.save()            
        url = '/' + user.email
        if(user.type == 'stu'):
            url += '/student/'
        else:
            url +='/tutor/'
        return HttpResponseRedirect((url))
    else:
        classReq = request.POST['class']
        schedules = Schedule.objects.filter(schedule__icontains=request.POST['class'])
        return render(request,'welcome/listTutors.html',{'schedules' : schedules, 'classReq': classReq})

def finishSignup(request):
    model = User
    try:
        choice = request.POST['type']
    except (KeyError, User.DoesNotExist):
        return render(request, 'welcome/selectType.html', {
            'comments': User,
            'error_message': "Add all fields",
        })
    else:
        user = request.user
        user.type = choice
        user.save()
        url = '/' + user.email
        if(user.type == 'stu'):
            url += '/student/'
        else:
            url +='/tutor/'
        return HttpResponseRedirect((url))

# def tutorSignUp(request, subject, catalog_nbr, descr):
#     model = User
#     identifier = subject + ' ' + catalog_nbr + ': ' + descr
#     if(identifier not in model.classes_signed_up):
#         model.classes_signed_up.add(identifier)
#     user = request.user
#     url = '/' + user.email + '/tutor/'
#     return HttpResponseRedirect(url)

def findClassByName(request):
    courseName = request.POST['crsName']
    if courseName == "":
        res = []
    else:
        apiUrl = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&keyword=' + courseName
        courses = requests.get(apiUrl).json()
        res = []
        already_seen = set()
        for course in courses:
            if(course['crse_id'] in already_seen):
                continue
            already_seen.add(course['crse_id'])
            res.append(course)
    return render(request,'welcome/listClasses.html',{'classesFiltered' : res})

class selectTimingsView(generic.ListView):
    template_name = 'welcome/selectTimings.html'
    def get_queryset(self):
        return "timings success"

def viewTutorTime(request, user_id, classReq):
    try:
        tutor = request.POST['tutor']
    except:
        # Redisplay the question voting form.
        schedules = Schedule.objects.filter(schedule__icontains=classReq)
        return render(request, 'welcome/listTutors.html', {
            'schedules' : schedules, 
            'classReq': classReq,
            'error_message': "You must select a tutor before hitting request",
        })
    else:
        spl = request.POST.get('tutor').split(' ')
        tutorId = spl[0]
        course = spl[1] + ' ' + spl[2]
        tutorUser = User.objects.get(pk=tutorId)
        tutorSchedule = Schedule.objects.get(User = tutorUser)
        tutorAvailableTimes = tutorSchedule.tutorTimings
        return render(request,'welcome/viewTutorTime.html',{'tutorUser' : tutorUser, 'tutorAvailableTimes' : tutorAvailableTimes, 'course': course})
     
def requestTutorTime(request, user_id, tutor_id, course):
    tutorUser = User.objects.get(pk=tutor_id)
    tutorSchedule = Schedule.objects.get(User=tutorUser)
    time = request.POST.get('tutorTime')
    user = User.objects.get(pk=user_id)
    try:
        request = Request.objects.get(student = user, tutor = tutorUser, course = course, time = time)
    except:             
        request = Request(student = user, tutor = tutorUser, course = course, time = time)
        request.save()
    url = '/' + user.email
    if(user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))
def requestTutorForClass(request, classReq):
    try:
        newClassReq = classRequest.objects.get(course = classReq)
        if request.user.email not in newClassReq.studentRequested:
            newClassReq.upvotes += 1
            newClassReq.studentRequested.append(request.user.email)
    except:
        newClassReq = classRequest(course = classReq, studentRequested = [], tutorsAlreadyAccepted = [])
        newClassReq.studentRequested.append(request.user.email)
    newClassReq.save()
    url = '/welcome/tutorRequests'
    return HttpResponseRedirect((url))

def tutorRequestAction(request, request_id, course):
    choice = request.POST.get('choice')
    ClassReq = classRequest.objects.get(pk = request_id)
    if choice == 'Request':
        if request.user.email not in ClassReq.studentRequested:
            ClassReq.upvotes += 1
            ClassReq.studentRequested.append(request.user.email)
        url = '/welcome/tutorRequests'
        ClassReq.save()
    elif choice == 'Accept':
        try:
            schedule = Schedule.objects.get(User = request.user)
        except:
            schedule = Schedule(schedule = [], tutorTimings = [], User = request.user)
            schedule.save()
        if(course not in schedule.schedule and request.user.email not in ClassReq.tutorsAlreadyAccepted):
            schedule.schedule.append(course)
            ClassReq.tutorsAlreadyAccepted.append(request.user.email)
            ClassReq.tutorsAccepted += 1
            url = '/' + request.user.email + '/tutor/'  
        else:
            url = '/welcome/tutorRequests'  
        schedule.save()
        ClassReq.save()
    elif choice == 'Delete':
        ClassReq = classRequest.objects.get(pk = request_id)
        ClassReq.delete()
        url = '/welcome/tutorRequests'
    return HttpResponseRedirect((url))


def confirmTimings(request, user_id):
    user = User.objects.get(pk=user_id)
    list = request.POST.getlist('class')
    for timing in list:
        spl = timing.split(' ')
        day = spl[0]
        time = spl[1] + spl[2]
        course_time = day + ' ' + time
        try:
            schedule = Schedule.objects.get(User = user)
        except:
            schedule = Schedule(schedule = [], tutorTimings = [], User = user)
            schedule.save()
        if(course_time not in schedule.tutorTimings):
            schedule.tutorTimings.append(course_time)
        schedule.save()
    url = '/' + user.email
    if(user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))

def requestChoice(request, request_id):
    req = Request.objects.get(pk = request_id)
    choice = request.POST.get('choice')
    if choice == 'Accept':
        req.accepted='acc'
    else:
        req.accepted = 'dec'
    req.save()
    url = '/' + request.user.email
    if(request.user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))

def deleteTime(request, time_to_delete):
    user = request.user
    schedule = Schedule.objects.get(User = user)
    schedule.tutorTimings.remove(time_to_delete)
    schedule.save()
    url = '/' + request.user.email
    if(request.user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))
def deleteClassTutor(request, class_to_delete):
    user = request.user
    schedule = Schedule.objects.get(User = user)
    schedule.schedule.remove(class_to_delete)
    schedule.save()
    url = '/' + request.user.email
    if(request.user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))

def deleteRequest(request,request_id):
    req_to_delete = Request.objects.get(pk = request_id)
    req_to_delete.delete()
    url = '/' + request.user.email
    if(request.user.type == 'stu'):
        url += '/student/'
    else:
        url +='/tutor/'
    return HttpResponseRedirect((url))

def changeTutorRate(request):
    user = request.user
    newRate = request.POST['newRate']

    if newRate == "":
        return render(request, 'welcome/changeRate.html', {
            'comments': User,
            'error_message': "Please Enter a Rate Before Clicking Submit",
        })
    else:
        user.rate = newRate
        user.save()
        url = '/' + request.user.email + '/tutor/'
        return HttpResponseRedirect((url))

def addTutorBio(request):
    user = request.user
    newBio = request.POST['bio']

    if newBio == "":
        return render(request, 'welcome/addBio.html', {
            'comments': User,
            'error_message': "Please Enter a Bio Before Clicking Submit",
        })
    else:
        user.bio = newBio
        user.save()
        url = '/' + request.user.email + '/tutor/'
        return HttpResponseRedirect((url))
        
class contactView(generic.ListView):
    template_name = 'welcome/contact.html'
    def get_queryset(self):
        return 'contact success'


# def contact(request):
#     if request.method=='POST':
#         name = request.POST.get('cf-name')
#         about = request.POST.get('cf-about')
#         email = request.POST.get('cf-email')
#         subject = request.POST.get('cf-number')
#         message = request.POST.get('cf-message')

#         data = {
#             'name': name,
#             'email': email,
#             'about': about,
#             'subject': subject,
#             'message': message
#         }
#         message = '''
#         From:\n\t\t{}\n
#         Email:\n\t\t{}\n
#         About:\n\t\t{}\n
#         Subject:\n\t\t{}\n
#         Message:\n\t\t{}\n
#         '''.format(data['name'], data['email'], data['about'], data['subject'], data['message'])
#         send_mail('Tutor Me Contact Form', message, 'tutormedjango@gmail.com', ['tutormedjango@gmail.com']) 
#         messages.success(request, 'Your message has been sent successfully!')

#     return render(request, 'welcome/contact.html', {})
