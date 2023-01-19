import json
from django.db.models import F

from django.contrib import messages
from django.contrib.auth import authenticate, login as login_
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile, Dorm, Room, Setting


def home(request, *args, **kwargs):
    context = {}
    grade_1_male = UserProfile.objects.filter(grade='کارشناسی', sex=True)
    grade_1_female = UserProfile.objects.filter(grade='کارشناسی', sex=False)

    grade_2_male = UserProfile.objects.filter(grade='ارشد', sex=True)
    grade_2_female = UserProfile.objects.filter(grade='ارشد', sex=False)

    grade_3_male = UserProfile.objects.filter(grade='دکترا', sex=True)
    grade_3_female = UserProfile.objects.filter(grade='دکترا', sex=False)

    all_students = UserProfile.objects.all().exclude(grade='مدیر')

    rooms = Room.objects.all()
    context['chart1'] = {
        'male': grade_1_male.count(),
        'female': grade_1_female.count(),
    }

    context['chart2'] = {
        'male': grade_2_male.count(),
        'female': grade_2_female.count(),
    }

    context['chart3'] = {
        'male': grade_3_male.count(),
        'female': grade_3_female.count(),
    }

    context['all_students'] = all_students.count()
    rooms = Room.objects.all()
    var = 0
    for room in rooms:
        var += int(room.capacity)
    context['rooms'] = var

    context['left_rooms'] = var - context['all_students']

    if request.user.is_authenticated:
        if request.method == 'POST':
            signup = request.POST.get('signup', '3')
            room = request.POST.get('room', 'room')
            if signup == '0':
                stop_signup()
                messages.success(request=request, message='ثبت نام با موفقیت به پایان رسید')
            elif signup == '1':
                start_signup()
                messages.success(request=request, message='ثبت نام با موفقیت آغاز شد')
            if room == 'start_process_male':
                result = room_assignment(True)
                if result[0]:
                    messages.success(request=request, message='فرایندس تخصیص اتاق ها با موفقیت انجام شد.')
                else:
                    messages.error(request=request, message=f'{result[1]}')
            elif room == 'start_process_female':
                result = room_assignment(False)
                if result[0]:
                    messages.success(request=request, message='فرایندس تخصیص اتاق ها با موفقیت انجام شد.')
                else:
                    messages.error(request=request, message=f'{result[1]}')

        context['signup'] = Setting.objects.all()[0].allow_new_user
    else:
        return redirect(to=login)

    return render(request=request, template_name='Index.html', content_type='text/html',
                  status=200,
                  context=context,
                  using=None)


@csrf_exempt
def get_users(request):
    if request.method == 'POST':
        sex = request.POST.get("sex")
        print(sex)
        if sex == 'true':
            sex = True
        else:
            sex = False
        users = UserProfile.objects.filter(sex=sex)
        users_list = []
        for user in users:
            users_list.append({
                'name': user.user_instance.last_name + ' ' + user.user_instance.last_name,
                'id': user.id,
            })
        return JsonResponse({'users': users_list})


def register(request):
    context = {}
    if request.user.is_authenticated:
        return redirect(to=home)
    else:
        if request.method == 'POST':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            father_name = request.POST.get('father_name', '')
            student_number = request.POST.get('student_number', '')
            id_number = request.POST.get('id_number', '')
            phone_number = request.POST.get('phone_number', '')
            sex = request.POST.get('sex', '')
            is_paying = request.POST.get('is_paying', '')
            grade = request.POST.get('grade', '')
            early = request.POST.get('early', '')
            roommate = request.POST.get('roommate', '')
            noisy = request.POST.get('noisy', '')
            nation = request.POST.get('nation', '')
            password = request.POST.get('password', '')

            try:
                UserProfile.objects.get(student_number=student_number)
                messages.error(request, 'شماره دانشجویی تکراری می باشد.')
                return render(request=request, template_name='Registration.html', content_type='text/html',
                              status=200,
                              context=context,
                              using=None)
            except UserProfile.DoesNotExist:
                pass

            try:
                user_instance = User.objects.create_user(username=str(student_number),
                                                         email=f'{str(student_number)}@iau.ir',
                                                         password=password)
            except Exception as error:
                messages.error(request, f'{str(error)}')
                return render(request=request, template_name='Registration.html', content_type='text/html',
                              status=200,
                              context=context,
                              using=None)

            user_instance.first_name = first_name
            user_instance.last_name = last_name

            user_instance.save()
            user_profile = UserProfile.objects.create(user_instance=user_instance)
            user_profile.student_number = student_number
            if sex == '1':
                user_profile.sex = True
                last_dorm = Dorm.objects.get(sex=True)
                last_room = Room.objects.filter(dorm=last_dorm)
                user_profile.room = last_room[0]
            else:
                user_profile.sex = False
                last_dorm = Dorm.objects.get(sex=False)
                last_room = Room.objects.filter(dorm=last_dorm)
                user_profile.room = last_room[0]

            user_profile.sex = sex
            if nation == '1':
                user_profile.is_native_born = True
            else:
                user_profile.is_native_born = False

            if is_paying == '1':
                user_profile.is_paying = True
            else:
                user_profile.is_paying = False

            user_profile.father_name = father_name
            user_profile.id_card_number = id_number
            user_profile.phone_number = phone_number
            if early == '1':
                user_profile.is_early_bird = True
            else:
                user_profile.is_early_bird = False

            user_profile.grade = grade
            if roommate != '0':
                user_profile.requested_roommate_id = UserProfile.objects.get(id=roommate)

            if noisy == '1':
                user_profile.is_noisy = True
            else:
                user_profile.is_noisy = False
            user_profile.save()

            messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
            authenticate(request=request, username=str(student_number), email=f'{str(student_number)}@iau.ir',
                         password=password)
            return redirect(to=home)


        else:
            return render(request=request, template_name='Registration.html', content_type='text/html',
                          status=200,
                          context=context,
                          using=None)


def login(request):
    context = {}

    if request.user.is_authenticated:
        return redirect(to=home)
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = None
            try:
                user = authenticate(request=request, username=username, password=password)
                login_(request, user)
            except:
                pass
            if user is not None:
                return redirect(to=home)
            else:
                messages.error(request=request, message='اطلاعات وارد شده صحیح نمیباشد.')
        return render(request=request, template_name='Login.html', content_type='text/html',
                      status=200,
                      context=context,
                      using=None)


def logout_view(request):
    context = {}
    logout(request)
    return render(request=request, template_name='Login.html', content_type='text/html',
                  status=200,
                  context=context,
                  using=None)


def student_management(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_staff:
            context['students'] = UserProfile.objects.all().exclude(grade='مدیر')
            return render(request=request, template_name='StudentManagement.html', context=context)
        else:
            return redirect(home)
    else:
        return redirect(to=login)


def dorm_management(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_staff:
            context['dorms'] = Dorm.objects.all()
            return render(request=request, template_name='DormManagement.html', context=context)
        else:
            pass
    else:
        return redirect(to=login)


def room_management(request):
    context = {}

    if request.user.is_authenticated:
        if request.user.is_staff:
            context['rooms'] = Room.objects.all()
            return render(request=request, template_name='RoomManagement.html', context=context)
        else:
            pass
    else:
        return redirect(to=login)


def room_assignment(sex: bool = True) -> list:
    # for male , sample flow
    dorm = Dorm.objects.get(sex=sex)
    rooms = Room.objects.filter(dorm=dorm)
    students = UserProfile.objects.all().exclude(sex=sex).exclude(grade='مدیر')

    total_students_number = len(students)
    total_room_number = len(rooms)
    total_capacity = 0

    for room in rooms:
        total_capacity += room.capacity

    if total_capacity < total_students_number:
        return [False, 'ظرفیت اتاق ها از تعداد دانشجو ها کم تر میباشد.']

    students_score = {}
    registered_rooms = []
    for student in students:
        # student.room = None
        # student.room_confirmed = True
        # student.save()
        try:
            students_score[student.user_instance.id] = {
                'native': student.is_native_born,
                'paid': student.is_paying,
                'early': student.is_early_bird,
                'noisy': student.is_noisy,
                'requested_roommate': student.requested_roommate.id,
            }
        except:
            students_score[student.user_instance.id] = {
                'native': student.is_native_born,
                'paid': student.is_paying,
                'early': student.is_early_bird,
                'noisy': student.is_noisy,
                'requested_roommate': '0',
            }

    score_table = {
        'paid': 2,
        'native': 2,
        'bonus': 1,
    }

    sorted_users = []
    # Phase one
    for key, value in students_score.items():
        score = 0
        for key_, value_ in value.items():
            if key_ == 'native':
                if not value_:
                    score += score_table['native']
            elif key_ == 'paid':
                if not value_:
                    score += score_table['paid']
            elif key_ == 'requested_roommate':
                if value_ == '0':
                    score += score_table['bonus']
        students_score[key]['score'] = score

    grouping_divider = total_capacity // total_room_number
    level_0_users = []
    level_1_users = []
    level_2_users = []
    level_3_users = []
    level_4_users = []
    level_5_users = []
    for key, value in students_score.items():
        score = students_score[key]['score']
        if score == 0:
            level_0_users.append({
                'id': key,
                'score': 0,
                'roommate_id': students_score[key]['requested_roommate'],
            })
        elif score == 1:
            level_1_users.append({
                'id': key,
                'score': 1,
                'roommate_id': students_score[key]['requested_roommate'],
            })
        elif score == 2:
            level_2_users.append({
                'id': key,
                'score': 2,
                'roommate_id': students_score[key]['requested_roommate'],
            })
        elif score == 3:
            level_3_users.append({
                'id': key,
                'score': 3,
                'roommate_id': students_score[key]['requested_roommate'],
            })
        elif score == 4:
            level_4_users.append({
                'id': key,
                'score': 4,
                'roommate_id': students_score[key]['requested_roommate'],
            })
        elif score == 5:
            level_5_users.append({
                'id': key,
                'score': 5,
                'roommate_id': students_score[key]['requested_roommate'],
            })

        students_score[key]['score'] = score
    final_users = []
    for user in level_5_users:
        final_users.append(user)

    for user in level_4_users:
        final_users.append(user)

    for user in level_3_users:
        final_users.append(user)

    for user in level_2_users:
        final_users.append(user)

    for user in level_1_users:
        final_users.append(user)

    last_filled_room = 0
    try:
        for room in rooms:
            i = int(room.capacity)
            for i in range(0, i):
                student_ = UserProfile.objects.get(user_instance_id=final_users[last_filled_room]['id'])
                student_.room = room
                student_.room_confirmed = True
                student_.save()
                last_filled_room += 1
    except IndexError:
        pass
    except Exception as error:
        return [False, str(error)]

    return [True, '']


def stop_signup():
    setting = Setting.objects.all()[0]
    setting.allow_new_user = False
    setting.save()
    return True


def start_signup():
    setting = Setting.objects.all()[0]
    setting.allow_new_user = True
    setting.save()
    return True
