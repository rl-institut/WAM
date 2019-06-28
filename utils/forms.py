from django import forms


class FeedbackForm(forms.Form):
    from_name = forms.CharField(required=False,
                                max_length=100,
                                label='Ihr Name (optional)')
    from_email = forms.EmailField(required=False,
                                  label='Ihre E-Mail-Adresse (optional)')
    subject = forms.CharField(required=True,
                              max_length=100,
                              label='Betreff')
    message = forms.CharField(widget=forms.Textarea,
                              required=True,
                              label='Ihr Feedback')

    def submit(self):
        pass
