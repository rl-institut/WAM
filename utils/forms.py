from django import forms


class FeedbackForm(forms.Form):
    """Input form for feedback page"""
    from_name = forms.CharField(required=False,
                                max_length=100,
                                label='Your Name (optional)')
    from_email = forms.EmailField(required=False,
                                  label='Email Address (optional)')
    subject = forms.CharField(required=True,
                              max_length=100,
                              label='Subject')
    message = forms.CharField(widget=forms.Textarea,
                              required=True,
                              label='Your Feedback')

    def submit(self):
        pass
