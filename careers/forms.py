from django.forms import forms, CharField, TextInput, EmailField, EmailInput, ChoiceField, Select, DateField, \
    DateInput, FileField, FileInput, HiddenInput, RadioSelect


class ApplicationForm(forms.Form):
    position = CharField(
        required=False,
        max_length=100,
        widget=HiddenInput,
    )
    first_name = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    phone = CharField(
        required=True,
        max_length=12,
        min_length=12,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '555-555-5555',
                'data-format': 'custom',
                'data-delimiter': '-',
                'data-blocks': '3 3 4',
                'type': 'tel'
            }
        )
    )
    email = EmailField(
        required=True,
        max_length=100,
        widget=EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }
        )
    )
    applicant_address = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Home Address'
            }
        )
    )
    applicant_city = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }
        )
    )
    applicant_state = CharField(
        required=True,
        max_length=2,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'State',
            }
        )
    )
    applicant_zip = CharField(
        required=True,
        max_length=5,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zip',
            }
        )
    )
    eligible = CharField(
        required=True,
        max_length=3,
        widget=RadioSelect(
            choices=[
                ('Yes', 'Yes'),
                ('No', 'No')
            ],
            attrs={
                'class': 'custom-control-input',
            }
        )
    )
    transportation = CharField(
        required=True,
        max_length=3,
        widget=RadioSelect(
            choices=[
                ('Yes', 'Yes'),
                ('No', 'No')
            ],
            attrs={
                'class': 'custom-control-input',
            }
        )
    )
    cannot_work = CharField(
        required=True,
        max_length=3,
        widget=RadioSelect(
            choices=[
                ('Yes', 'Yes'),
                ('No', 'No')
            ],
            attrs={
                'class': 'custom-control-input',
            }
        )
    )
    ref_name = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reference Name'
            }
        )
    )
    ref_phone = CharField(
        required=True,
        max_length=12,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '555-555-5555',
                'data-format': 'custom',
                'data-delimiter': '-',
                'data-blocks': '3 3 4',
                'maxlength': '12',
                'minlength': '12',
                'type': 'tel'
            }
        )
    )
    ref_relation = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Relation'
            }
        )
    )
    ref_years = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Years'
            }
        )
    )
    education = ChoiceField(
        required=True,
        choices=[
            ('', 'Select an Option'),
            ('High School Diploma', 'High School Diploma'),
            ('GED', 'GED'),
            ('Some College', 'Some College'),
            ('Certificate Degree', 'Certificate Degree'),
            ("Associate's Degree", "Associate's Degree"),
            ("Bachelor's Degree", "Bachelor's Degree"),
            ("Master's Degree", "Master's Degree"),
            ("Doctorate or higher", "Doctorate or higher")
        ],
        widget=Select(
            attrs={
                'class': 'form-control custom-select',
            }
        )
    )
    start_date = DateField(
        required=True,
        widget=DateInput(
            attrs={
                'class': 'form-control appended-form-control cs-date-picker',
                'placeholder': 'Choose Date',
                'data-datepicker-options': '{"altInput": true, "altFormat": "F j, Y", "dateFormat": "Y-m-d"}'
            }
        )
    )
    resume = FileField(
        required=True,
        widget=FileInput(
            attrs={
                'class': 'cs-file-drop-input',
            }
        )
    )
    cover_letter = FileField(
        required=False,
        widget=FileInput(
            attrs={
                'class': 'cs-file-drop-input',
            }
        )
    )
