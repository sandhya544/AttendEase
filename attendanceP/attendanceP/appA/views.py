from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import student, attend, data
import datetime


# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            if user.is_superuser:
                return redirect('adminpage')
            else:
                return render(request, 'appA/student.html')
    return render(request, 'appA/index.html')


@login_required(login_url='index')
def adminPage(request):
    trainers = data.objects.all().values('trainer').distinct()
    topics = data.objects.all().values('topic').distinct()

    if request.method == "POST":
        if "register" in request.POST:
            username = request.POST['username'].lower()
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            email = username + "@svrec.ac.in"
            gender = request.POST['gender']
            branch = request.POST['branch']
            mobile = request.POST['mobile']
            parent_mobile = request.POST['p_mobile']
            if password != confirm_password:
                messages.error(request, "Password and Confirm Password are not same")
                return render(request, 'appA/admin.html')
            else:
                user = authenticate(request, username=username, email=email)
                if user is None:
                    user = User.objects.create_user(username=username, password=password, last_name=last_name,
                                                    first_name=first_name, email=email)
                    user.save()
                    stu = student.objects.create(name=first_name + " " + last_name, roll_no=username, email=email,
                                                 gender=gender, branch=branch, mobile=mobile,
                                                 parent_mobile=parent_mobile)
                    stu.save()
                    messages.success(request, "Successfully Registered")
                    return render(request, 'appA/admin.html')
                else:
                    messages.error(request, "User Already Exists")
                    return render(request, 'appA/admin.html')
        elif "attendance" in request.POST:
            department = request.POST['branch']
            return redirect('takeAttendance', branch=department)
        elif "add_data" in request.POST:
            topic = request.POST['topic']
            trainer = request.POST['trainer']
            batch = request.POST['batch']
            total_classes = request.POST['total_classes']
            try:
                d = data.objects.get(batch=batch, topic=topic, trainer=trainer)
                messages.error(request, "Data Already Exists")
                return render(request, 'appA/admin.html')
            except data.DoesNotExist:
                d = data.objects.create(batch=batch, topic=topic, trainer=trainer, total_classes=total_classes)
                d.save()
                messages.success(request, "Data Added Successfully")
                return render(request, 'appA/admin.html')

    return render(request, 'appA/admin.html', {'trainers': trainers, 'topics': topics})


@login_required(login_url='index')
def takeAttendance(request, branch):
    students = student.objects.filter(branch=branch)
    topic = data.objects.all().values('topic').distinct()
    trainer = data.objects.all().values('trainer').distinct()
    batches = data.objects.all().values('batch').distinct()
    print(students.count(), type(students.count()))

    counter = list(range(students.count()))

    zip_list = zip(students, counter)
    date = datetime.date.today()
    if request.method == "POST":
        batch = request.POST['batch']
        topic = request.POST['topic']
        trainer = request.POST['trainer']
        total_classes = request.POST['total_classes']
        if "submit" in request.POST:
            for i in range(students.count()):
                roll_no = request.POST["S" + str(i)]
                status = request.POST["R"+str(i)]
                if status == "present":
                    present_classes = 1
                    try:
                        attd = attend.objects.get(roll_no=roll_no, date=date)
                        attd.present_classes += present_classes
                        attd.save()
                    except attend.DoesNotExist:
                        s=student.objects.get(roll_no=roll_no)
                        print(s.branch,type(s.branch))
                        attd = attend.objects.create(roll_no=roll_no,name=s.name, batch=batch, topic=topic, trainer=trainer,
                                                     total_classes=total_classes, present_classes=present_classes,department=s.branch)

                        attd.save()
                else:
                    try:
                        attd = attend.objects.get(roll_no=roll_no, date=date)
                        attd.total_classes = total_classes
                        attd.save()
                    except attend.DoesNotExist:
                        s = student.objects.get(roll_no=roll_no)
                        attd = attend.objects.create(roll_no=roll_no,name=s.name, batch=batch, topic=topic, trainer=trainer,
                                                     total_classes=total_classes, present_classes=0)
                        attd.save()
            messages.success(request, "Attendance Taken Successfully")
            return redirect('index')
    return render(request, 'appA/attendance.html', {'students': students, 'zip_list': zip_list, 'topics': topic,
                                                    'trainers': trainer, 'date': date, 'batches': batches})


@login_required(login_url='index')
def viewAttendance(request):
    if request.method == "POST":
        if "view" in request.POST:
            roll_no = request.POST['roll_no']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            try:
                att = attend.objects.filter(roll_no=roll_no, date__range=[start_date, end_date])
                return render(request, 'appA/viewAttendance.html', {'att': att})
            except attend.DoesNotExist:
                messages.error(request, "No Attendance Found")
                return render(request, 'appA/viewAttendance.html')
    return render(request, 'appA/viewAttendance.html')
