from django.shortcuts import render
from .forms import KakeiboForm, GoalsForm, CategoryForm
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo, Goals
from django.db import models
import datetime
import calendar
from django.db.models import Sum


class KakeiboListView(ListView):
    # Model name(database)
    model = Kakeibo
    # Template (front-end)
    template_name = 'kakeibo/kakeibo_list.html'

    def queryset(self):
        return Kakeibo.objects.all()


class KakeiboCreateView(CreateView):
    model = Kakeibo
    form_class = KakeiboForm
    success_url = reverse_lazy('kakeibo:create_done')


def create_done(request):
    return render(request, 'kakeibo/create_done.html')


class KakeiboUpdateView(UpdateView):
    model = Kakeibo
    form_class = KakeiboForm
    success_url = reverse_lazy('kakeibo:update_done')


def update_done(request):
    return render(request, 'kakeibo/update_done.html')


class KakeiboDeleteView(DeleteView):
    model = Kakeibo
    success_url = reverse_lazy('kakeibo:delete_done')


def delete_done(request):
    return render(request, 'kakeibo/delete_done.html')


###
# Following for goal setting
###


def Goals_showing(request):
    current_goal = Goals.objects.all()
    current_totalmoney = 0
    goal_value = 0
    Is_exist = None
    Is_exist_oppposite = None
    currentstate = "unknown"

    if len(current_goal) != 0:
        Is_exist = None
        if "W" in list(str(current_goal[0].memo)):
            current_range = [d.isoformat()
                             for d in get_week(datetime.datetime.now().date())]
            goal_value = current_goal[0].weekly_goal
            currentstate = "Weekly"
        elif "M" in list(str(current_goal[0].memo)):
            current_range = [d.isoformat()
                             for d in get_month(datetime.datetime.now().date())]
            goal_value = current_goal[0].mothly_goal
            currentstate = "Monthly"

        money_sum = []
        f_year, f_month, f_date = current_range[0].split("-")
        first_date = f_year + "-" + f_month + "-" + f_date
        l_year, l_month, l_date = current_range[len(
            current_range)-1].split("-")
        last_date = l_year + "-" + l_month + "-" + l_date

        total_a_week = Kakeibo.objects.filter(
            date__range=(first_date, last_date))
        category_total = total_a_week.values('money')

        for j in range(len(category_total)):
            money = category_total[j]['money']
            category = Category.objects.get(
                pk=total_a_week.values("category")[j]['category'])
            datestr = total_a_week.values('date')[j].get(
                "date").strftime("%Y-%m-%d")
            money_sum.append(
                [datestr, category.category_name, money])

        for doll in money_sum:
            current_totalmoney += doll[2]
    else:
        Is_exist = "Auto"

    if Is_exist == None:
        Is_exist_oppposite = "Auto"
    else:
        Is_exist_oppposite = None

    return render(request, 'kakeibo/goals_show.html', {
        'Is_exist': Is_exist,
        'Is_exist_oppposite': Is_exist_oppposite,
        'current_totalmoney': current_totalmoney,
        'goal_value': goal_value,
        'currentstate': currentstate,
        'current_goal': current_goal,
    })


class GoalCreateView(CreateView):
    model = Goals
    form_class = GoalsForm
    success_url = reverse_lazy('kakeibo:set_goal_done')


def set_goal_done(request):
    return render(request, 'kakeibo/setting_goal_done.html')


class GoalUpdateView(UpdateView):
    model = Goals
    form_class = GoalsForm
    success_url = reverse_lazy('kakeibo:update_goal_done')


def update_goal_done(request):
    return render(request, 'kakeibo/update_goal_done.html')


class GoalsDeleteView(DeleteView):
    model = Goals
    success_url = reverse_lazy('kakeibo:delete_goal_done')


def delete_goal_done(request):
    return render(request, 'kakeibo/delete_goal_done.html')


def show_circle_graph(request):

    kakeibo_data = Kakeibo.objects.all()

    total = 0
    for item in kakeibo_data:
        total += item.money

    category_list = []
    category_data = Category.objects.all().order_by('-category_name')
    for item in category_data:
        category_list.append(item.category_name)

    current_week = [d.isoformat()
                    for d in get_week(datetime.datetime.now().date())]
    weekly_sum = []
    f_year, f_month, f_date = current_week[0].split("-")
    first_date = f_year + "-" + f_month + "-" + f_date
    l_year, l_month, l_date = current_week[6].split("-")
    last_date = l_year + "-" + l_month + "-" + l_date

    total_a_week = Kakeibo.objects.filter(date__range=(first_date, last_date))
    category_total = total_a_week.values('money')
    print(total_a_week)
    print(category_total)

    for j in range(len(category_total)):
        money = category_total[j]['money']
        category = Category.objects.get(
            pk=total_a_week.values("category")[j]['category'])
        datestr = total_a_week.values('date')[j].get(
            "date").strftime("%Y-%m-%d")
        weekly_sum.append(
            [datestr, category.category_name, money])

    border_color_list = ['254,97,132,0.8', '54,164,235,0.8', '0,255,65,0.8', '255,241,15,0.8',
                         '255,94,25,0.8', '84,77,203,0.8', '204,153,50,0.8', '214,216,165,0.8',
                         '33,30,45,0.8', '52,38,89,0.8']
    border_color = []
    for x, y in zip(category_list, border_color_list):
        border_color.append([x, y])

    background_color_list = ['254,97,132,0.5', '54,164,235,0.5', '0,255,65,0.5', '255,241,15,0.5',
                             '255,94,25,0.5', '84,77,203,0.5', '204,153,50,0.5', '214,216,165,0.5'
                             '33,30,45,0.5', '52,38,89,0.5']
    background_color = []
    for x, y in zip(category_list, background_color_list):
        background_color.append([x, y])

    new_sum = []
    count = 0
    ite = 1
    print(len(category_list))
    for i in range(len(category_list) * 7 + len(category_list)):
        if count < 7:
            if any([True for ai in weekly_sum if current_week[count] == ai[0]]):
                c = 0
                is_there = False
                for d, j in enumerate(weekly_sum):
                    c += 1
                    if current_week[count] == j[0] and category_list[ite-1] == j[1]:
                        new_sum.append(weekly_sum[d])
                        is_there = True
                        break
                    if c == len(weekly_sum) and is_there == False:
                        new_sum.append(
                            [current_week[count], category_list[ite - 1], 0])
            else:
                new_sum.append(
                    [current_week[count], category_list[ite-1], 0])
            count += 1
        else:
            count = 0
            ite += 1

    return render(request, 'kakeibo/kakeibo_circle.html', {
        'current_week': current_week,
        'category_list': category_list,
        'border_color': border_color,
        'background_color': background_color,
        'matrix_list': new_sum,
        "othersum": weekly_sum,
    })


one_day = datetime.timedelta(days=1)


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.

    'date' may be a datetime or date instance (the same type is returned).
    """
    day_idx = (date.weekday() +
               1) % 7  # turn sunday into 0, monday into 1, etc.
    sunday = date - datetime.timedelta(days=day_idx)
    date = sunday
    for n in range(7):
        yield date
        date += one_day


def get_month(date):
    """Return the full week (Sunday first) of the week containing the given date.

    'date' may be a datetime or date instance (the same type is returned).
    """
    num_days = calendar.monthrange(date.year, date.month)
    x = datetime.date(int(date.year), int(date.month), 1)

    print(str(x).split()[0])
    for n in range(int(num_days[1])):
        yield x
        x += one_day


def show_monster(request):
    #""""" Following data for this function """#
    goal_data = Goals.objects.all()
    kakeibo_data = Kakeibo.objects.all()

    #""""" Following for monster """#
    # initialize values
    current_total = 0
    goal_value = 0
    current_measuring = "Unknown"
    Is_morethanone = False

    # do only if there is data in goal_data
    if len(goal_data) > 0:
        memo_mean = goal_data[0].memo
        if "W" in list(memo_mean):
            current_measuring = "Weekly"
            goal_value = goal_data[0].weekly_goal
            months_or_week_dates = [d.isoformat()
                                    for d in get_week(datetime.datetime.now().date())]
        elif "M" in list(memo_mean):
            goal_value = goal_data[0].mothly_goal
            current_measuring = "Monthly"
            months_or_week_dates = [d.isoformat()
                                    for d in get_month(datetime.datetime.now().date())]
        first_year, first_month, first_date = months_or_week_dates[0].split(
            "-")
        first_day = first_year + "-" + first_month + "-" + first_date
        last_year, last_month, last_date = months_or_week_dates[len(
            months_or_week_dates)-1].split("-")
        last_day = last_year + "-" + last_month + "-" + last_date

        total_a_week_or_month = Kakeibo.objects.filter(
            date__range=(first_day, last_day))
        category_total_money = total_a_week_or_month.values('money')
        for ijj in category_total_money:
            current_total += ijj["money"]

        Is_morethanone = True

    if goal_value == 0:
        percentage = 0
        current_total = 0
    else:
        percentage = (current_total / goal_value) * 100

    print(percentage)

    #"""" Following for weekly ones """"#
    category_list = []
    category_data = Category.objects.all().order_by('-category_name')
    for item in category_data:
        category_list.append(item.category_name)

    current_week = [d.isoformat()
                    for d in get_week(datetime.datetime.now().date())]

    weekly_sum = []
    f_year, f_month, f_date = current_week[0].split("-")
    first_date = f_year + "-" + f_month + "-" + f_date
    l_year, l_month, l_date = current_week[6].split("-")
    last_date = l_year + "-" + l_month + "-" + l_date

    total_a_week = Kakeibo.objects.filter(date__range=(first_date, last_date))
    category_total = total_a_week.values('money')

    for j in range(len(category_total)):
        money = category_total[j]['money']
        category = Category.objects.get(
            pk=total_a_week.values("category")[j]['category'])
        datestr = total_a_week.values('date')[j].get(
            "date").strftime("%Y-%m-%d")
        weekly_sum.append(
            [datestr, category.category_name, money])

    border_color_list = ['254,97,132,0.8', '54,164,235,0.8', '0,255,65,0.8', '255,241,15,0.8',
                         '255,94,25,0.8', '84,77,203,0.8', '204,153,50,0.8', '214,216,165,0.8',
                         '33,30,45,0.8', '52,38,89,0.8']
    border_color = []
    for x, y in zip(category_list, border_color_list):
        border_color.append([x, y])

    background_color_list = ['254,97,132,0.5', '54,164,235,0.5', '0,255,65,0.5', '255,241,15,0.5',
                             '255,94,25,0.5', '84,77,203,0.5', '204,153,50,0.5', '214,216,165,0.5'
                             '33,30,45,0.5', '52,38,89,0.5']
    background_color = []
    for x, y in zip(category_list, background_color_list):
        background_color.append([x, y])

    meaning = "Plz enter your aim of this month/week"
    if percentage <= 20:
        meaning = "NICE"
    elif percentage <= 40:
        meaning = "OKAY"
    elif percentage <= 60:
        meaning = "SOSO"
    elif percentage <= 80:
        meaning = "BE CAREHULE"
    elif percentage <= 99:
        meaning = "ALLMOST.."
    else:
        meaning = "OMG"
    new_sum = []
    count = 0
    ite = 1
    for i in range(len(category_list) * 7):
        if count < 7:
            if any([True for ai in weekly_sum if current_week[count] == ai[0]]):
                for d, j in enumerate(weekly_sum):
                    if current_week[count] == j[0] and category_list[ite-1] == j[1]:
                        new_sum.append(weekly_sum[d])
                        break
            else:
                new_sum.append(
                    [current_week[count], category_list[ite-1], 0])
            count += 1
        else:
            count = 0
            ite += 1

    return render(request, 'kakeibo/monster.html', {
        'goal_values': goal_value,
        'current_totals': current_total,
        'percentages': round(percentage),
        'current_week': current_week,
        'category_list': category_list,
        'border_color': border_color,
        'background_color': background_color,
        'matrix_list': new_sum,
        "othersum": weekly_sum,
        "meaning": meaning,
        "current_measuring": current_measuring,
    })


class CategoryListView(ListView):
    # Model name(database)
    model = Category
    # Template (front-end)
    template_name = 'kakeibo/category_list.html'

    def queryset(self):
        return Category.objects.all()


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('kakeibo:category_create_done')


def category_create_done(request):
    return render(request, 'kakeibo/category_create_done.html')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('kakeibo:category_update_done_yes')


def category_update_done(request):
    return render(request, 'kakeibo/category_update_done.html')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('kakeibo:delete_category_done')


def delete_category_done(request):
    return render(request, 'kakeibo/category_delete_done.html')
