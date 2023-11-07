from django import forms


class ReservationForm(forms.Form):
    start_date = forms.DateField(
        label='Check-In Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    end_date = forms.DateField(
        label='Check-Out Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    room_type = forms.ChoiceField(
        label='Room Type',
        choices=(
            ('standard', 'Standard'),
            ('deluxe', 'Deluxe'),
            ('suite', 'Suite'),
        ),
        widget=forms.RadioSelect,
    )
    guest_first_name = forms.CharField(
        label='Guest First Name',
        max_length=100,
    )
    guest_last_name = forms.CharField(
        label='Guest Last Name',
        max_length=100,
    )
    guest_email = forms.EmailField(
        label='Email',
        max_length=100,
    )
    country_code = forms.ChoiceField(
        label='Country Code',
        choices=(
            ('+1', '+1 (USA)'),
            ('+44', '+44 (UK)'),
            # Add more country codes as needed
        ),
    )
    guest_phone = forms.CharField(
        label='Phone',
        max_length=20,
    )
    guest_address = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={'rows': 4}),
        max_length=200,
    )
