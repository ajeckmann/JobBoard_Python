from django.urls import path
from . import views

urlpatterns=[
    path('', views.route),
    path('create_user', views.create_user),
    path('login', views.validate_login),
    path('logout', views.logout),
    path('success', views.success),
    path('newjob', views.new_job),
    path('create_job', views.create_job),
    path('view_job/<int:job_id>', views.view_job),
    path('removejob/<int:job_id>', views.remove_job),
    path('editjob/<int:job_id>', views.edit_job),
    path('updatejob/<int:job_id>', views.update_job),
    path('addjobtolist/<int:job_id>', views.add_personaljob),
    path('deletejobfromlist/<int:job_id>', views.unassign_job)

  
]