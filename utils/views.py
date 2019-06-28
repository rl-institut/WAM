from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.validators import validate_email, ValidationError
from django.http.response import HttpResponseRedirect

from wam.settings import BASE_DIR
from utils.forms import FeedbackForm
from utils.mail import send_email

from configobj import ConfigObj
import os


class FeedbackView(FormView):
    """Feedback form which sends an E-mail to app admin"""

    app_name = None
    intro_text = None
    template_name = 'feedback.html'
    form_class = FeedbackForm
    success_url = '/feedback_thanks/'
    error_url = '/feedback_error/'

    def __init__(self,
                 app_name=None,
                 intro_text=None,
                 *args,
                 **kwargs):
        """
        Parameters
        ----------
        app_name : :obj:`str`
            Name of app the form should be created for
        intro_text : :obj:`str`
            Optional. Custom introductory text (inserted before form),
            defaults to standard welcome text (see template).
        """
        super(FeedbackView, self).__init__(*args, **kwargs)

        if app_name is not None:
            self.app_name = app_name

            # read and validate app admin's mail address from app.cfg
            app_config = ConfigObj(os.path.join(BASE_DIR, app_name, 'app.cfg'))
            email = app_config.get('email', None)
            if email is not None:
                try:
                    validate_email(email)
                    self.to_email = email
                except ValidationError:
                    raise ValidationError(
                        f'E-mail address in {app_name}`s app.cfg is invalid!')
        else:
            raise ValueError('Parameter "app_name" must be specified!')

        self.intro_text = intro_text

    def form_valid(self, form):
        form.submit()

        subject, body = self.prepare_message(**form.cleaned_data)
        success = send_email(to_email=self.to_email,
                             subject=subject,
                             message=body)
        if success:
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.error_url)

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)

        context['app_name'] = self.app_name
        context['intro_text'] = self.intro_text

        return context

    def prepare_message(self, **kwargs):
        subject = f'Nachricht über WAM Feedback-Formular: ' \
            f'App {self.app_name}'
        body = f'Sie haben eine Nachricht über das Feedback-Formular der WAM ' \
            f'erhalten.\n\n' \
            f'App: {self.app_name}\n' \
            f'Absender: {kwargs.get("from_name", "")} ' \
            f'({kwargs.get("from_email", "")})\n' \
            f'Betreff: {kwargs.get("subject", "")}\n' \
            f'========================================\n' \
            f'{kwargs.get("message", "")}\n' \
            f'========================================\n' \
            f'Bitte antworte nicht auf diese E-Mail, junger PadaWAM!\n' \
            f'Gez. Obi WAM Kenobi'
        return subject, body


class FeedbackSuccessful(TemplateView):
    template_name = 'feedback_successful.html'


class FeedbackError(TemplateView):
    template_name = 'feedback_error.html'