from django.conf.urls import url
from django.views.generic import TemplateView
from meta import views

import avatar.views
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/avatar/$', views.change_avatar, name='avatar_add'),
    url(r'^profile/avatar/render_primary/(?P<user>[\+\w\d\s\@\.\-_]+)/(?P<size>[\d]+)/$',
        avatar.views.render_primary,
        name='avatar_render_primary'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {'template_name': 'meta/login.html'},
        name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/'}, name='logout'),
    url(r'^forgot-password/$',
        django.contrib.auth.views.password_reset,
        {'template_name': 'meta/forgotpassword.html', 'post_reset_redirect': '/reset-requested/'},
        name='forgot_password'),
    url(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        django.contrib.auth.views.password_reset_confirm,
        {'template_name': 'meta/resetpassword.html'},
        name='password_reset_confirm'),
    url(r'^reset-requested/$', views.password_reset_requested, name='password_reset_requested'),
    url(r'^reset-done/$',
        django.contrib.auth.views.password_reset_complete,
        {'template_name': 'meta/resetdone.html'},
        name='password_reset_complete'),
    url(r'^change-password/$',
        django.contrib.auth.views.password_change,
        {'template_name': 'meta/changepassword.html', 'post_change_redirect': '/password-changed/'},
        name='change_password'),
    url(r'^password-changed/$', views.password_changed, name='password_change_done'),
    url(r'^change-email/$', views.change_email, name='change_email'),
]
