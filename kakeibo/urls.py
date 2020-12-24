from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('kakeibo_list/', views.KakeiboListView.as_view(), name='kakeibo_list'),
    path('kakeibo_create/', views.KakeiboCreateView.as_view(), name='kakeibo_create'),
    path('create_done/', views.create_done, name='create_done'),
    path('update/<int:pk>/', views.KakeiboUpdateView.as_view(),
         name='kakeibo_update'),
    path('update_done/', views.update_done, name='update_done'),
    path('delete/<int:pk>/', views.KakeiboDeleteView.as_view(),
         name='kakeibo_delete'),
    path('delete_done/', views.delete_done, name='delete_done'),
    path('circle/', views.show_circle_graph, name='kakeibo_circle'),
    path('monster/', views.show_monster, name='kakeibo_monster'),
    path('setgoal/', views.Goals_showing, name="setgoal"),
    path('set_goal/', views.GoalCreateView.as_view(), name='set_goal'),
    path('set_goal_done/', views.set_goal_done, name='set_goal_done'),
    path('update_goal/<int:pk>', views.GoalUpdateView.as_view(), name="update_goal"),
    path('update_goal_done/', views.update_goal_done, name="update_goal_done"),
    path('delete_goal/<int:pk>', views.GoalsDeleteView.as_view(), name="delete_goal"),
    path('delete_goal_done/', views.delete_goal_done, name="delete_goal_done"),
    path('category_list/', views.show_category,
         name="category_list"),
    path('create_category/', views.CategoryCreateView.as_view(),
         name="create_category"),
    path('category_create_done/', views.category_create_done,
         name="category_create_done"),
    path('update_category/<int:pk>', views.CategoryUpdateView.as_view(),
         name="update_category"),
    path('category_update_done_yes/', views.category_update_done,
         name="category_update_done_yes"),
    path('delete_category/<int:pk>', views.CategoryDeleteView.as_view(),
         name="delete_category"),
    path('delete_category_done/', views.delete_category_done,
         name="delete_category_done"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('create/', views.UserCreateView.as_view(), name="create"),  # 追記
]
