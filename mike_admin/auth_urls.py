from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from django_registration.backends.activation.views import RegistrationView, ActivationView

from mike_admin import views
from mike_admin.forms import AccountForm

# app_name='mike_admin'
urlpatterns = [
    # Account Creation urls
    path('register/',
        RegistrationView.as_view(
            form_class=AccountForm, 
            template_name='mike_admin/auth/register.html',
            success_url='/account/register/complete/', 
            email_subject_template='mike_admin/emails/activation_email_header.txt',
            email_body_template='mike_admin/emails/activation_email_body.html',  
        ),
        name='django_registration_register'),
    # FIXME
    path('activate/<str:activation_key>/', ActivationView.as_view(
        template_name='mike_admin/auth/activate.html', 
        success_url='/account/activate/complete/',
    ), name='activate'),
   
    path("activate/complete/",
        TemplateView.as_view(
            template_name="mike_admin/auth/activation_complete.html"
        ),
        name="django_registration_activation_complete",
    ),
     path(
        "register/complete/",
        TemplateView.as_view(
            template_name="mike_admin/auth/registration_complete.html"
        ),
        name="django_registration_complete",
    ),
    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="mike_admin/auth/registration_closed.html"
        ),
        name="django_registration_disallowed",
    ),
    
    # Login Url Patterns
    path('login/', auth_views.LoginView.as_view( template_name='mike_admin/auth/login.html'), name='login'),
    
    path('password_reset/',
          auth_views.PasswordResetView.as_view(template_name="mike_admin/auth/password_reset.html", 
                        email_template_name="mike_admin/emails/password_reset.html",
                        html_email_template_name="mike_admin/emails/password_reset.html", 
                        success_url="/account/password_reset/done/"), 
         name="password_reset"),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="mike_admin/auth/password_reset_done.html"), name="password_reset_done"),
    # FIXME
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="mike_admin/auth/password_reset_confirm.html", 
        post_reset_login=True, success_url="/account/reset/complete/" ), name="password_reset_confirm"),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="mike_admin/auth/password_reset_complete.html"), name="password_reset_complete"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name="mike_admin/auth/password_change.html", success_url='/account/change_password/done/' ), name="change_password"),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name="mike_admin/auth/password_change_done.html"), name="change_password_done"),
    # path('', include('djangos_registration.backends.activation.urls')),
]