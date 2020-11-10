from django import forms


class SimpleCaptchaField(forms.CharField):
    def __init__(self, label="Memo", **kwargs):
        super().__init__(label=label, required=True, **kwargs)
        self.widget.attrs['placeholder'] = "Please write 'Month' or 'Week' to choose Measuring term"

    def clean(self, value):
        value = super().clean(value)
        if value == "Month" or value == "Week":
            return value
        else:
            raise forms.ValidationError("Please enter correct answer")
