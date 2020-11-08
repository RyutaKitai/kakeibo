from django.shortcuts import render
from .forms import KakeiboForm, GoalsForm
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo, Goals
from django.db import models
import datetime
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


class GoalCreateView(CreateView):
    model = Goals
    form_class = GoalsForm
    success_url = reverse_lazy('kakeibo:setgoal_done')


def setgoal_done(request):
    return render(request, 'kakeibo/setting_goal_done.html')


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


def show_monster(request):

    # this is for weekly/mothly now

    goal_date = Goals.objects.all()
    current_total = 0
    goal_value = goal_date[0].mothly_goal
    # Following is to show the weekly fees
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

    for dollar in weekly_sum:
        current_total += dollar[2]

    percentage = (current_total / goal_value) * 100
    print(percentage)

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
    })
