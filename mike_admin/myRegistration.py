from django.conf import settings

from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

class MyRegisterView(RegistrationView):
    html_email_template="mike_admin/auth/activation_email.html"
    
    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.
        """
        if self.request.is_secure:
            protocol="https"
        else:
            protocol="http"
        
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        context['domain']= self.request.get_host()
        context['protocol']=protocol
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = "".join(subject.splitlines())
        email_message = render_to_string(
            template_name=self.html_email_template,
            context=context,
            request=self.request,
        )
        message=EmailMessage(subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email,])
        message.content_subtype = 'html' # this is required because there is no plain text email message
        message.send()
        
        # user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
