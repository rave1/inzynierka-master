from django import forms
from django.contrib.auth.models import User
from wca.models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset
from allauth.account.forms import SignupForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = "post"
    #     self.helper.layout = Layout(
    #         Row(
    #             Column("username", css_class="form-group col-md-6 mb-0"),
    #             Column("email", css_class="form-group col-md-6 mb-0"),
    #             css_class="form-row",
    #         ),
    #         Row(
    #             Column("first_name", css_class="form-group col-md-6 mb-0"),
    #             Column("last_name", css_class="form-group col-md-6 mb-0"),
    #             css_class="form-row",
    #         ),
    #         Submit(
    #             "submit",
    #             "Save Changes",
    #             css_class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-6 rounded mt-4",
    #         ),
    #     )


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "first arg is the legend of the fieldset",
                "like_website",
                "favorite_number",
                "favorite_color",
                "favorite_food",
                "notes",
            ),
            Submit("submit", "Submit", css_class="button white"),
        )

    class Meta:
        model = Profile
        fields = ["wca_id"]


class CustomSignupForm(SignupForm):
    wca_id = forms.CharField(max_length=10, label="WCA ID")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.profile.wca_id = self.cleaned_data["wca_id"]
        user.profile.save()
        return user
