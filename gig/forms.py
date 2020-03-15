"""
    This file is part of Gig-o-Matic

    Gig-o-Matic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django import forms
from .models import Gig
from band.models import Band
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class GigForm(forms.ModelForm):
    def __init__(self, **kwargs):
        band = kwargs.pop('band', None)
        user = kwargs.pop('user', None)
        super().__init__(
            label_suffix='',
            **kwargs
        )

        if user:
            self.fields['contact'].initial = user
            self.fields['contact'].empty_label = None
        if band:
            self.fields['contact'].queryset = band.confirmed_members
            self.fields['leader'].queryset = band.confirmed_members


        if user:
            self.fields['contact'].initial = user
            self.fields['contact'].empty_label = None
        if band:
            self.fields['contact'].queryset = band.confirmed_members
            self.fields['leader'].queryset = band.confirmed_members

    def clean(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            self.add_error('date', ValidationError(_('Gig call time must be in the future'), code='invalid date'))
        setdate = self.cleaned_data['setdate']
        if setdate and setdate < date:
            self.add_error('setdate', ValidationError(_('Set time must not be earlier than the call time'), code='invalid set time'))
        enddate = self.cleaned_data['enddate']
        if enddate:
            if enddate < date:
                self.add_error('enddate', ValidationError(_('Gig end must not be earlier than the call time'), code='invalid end time'))
            elif setdate and enddate < setdate:
                self.add_error('enddate', ValidationError(_('Gig end must not be earlier than the set time'), code='invalid end time'))

        super().clean()

    send_update = forms.BooleanField(required=False)

    # def is_valid(self):
    #     if self.cleaned_data['send_update']:
    #         send_gig_announcements(self)
    #     return super().is_valid()

    class Meta:
        model = Gig
        fields = ['title','contact','status','is_private','date','setdate','enddate','address','dress','paid','leader', 'postgig',
                'details','setlist','rss_description','invite_occasionals','hide_from_calendar','send_update']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('required')}),
            'address': forms.TextInput(attrs={'placeholder': _('Cloudcuckooland')}),
            'dress': forms.TextInput(attrs={'placeholder': _('Pants Optional')}),
            'paid': forms.TextInput(attrs={'placeholder': _('As If')}),
            'postgig': forms.TextInput(attrs={'placeholder': _('Hit the streets!')}),
            'details': forms.Textarea(attrs={'placeholder': _('who? what? where? when? why?')}),
            'setlist': forms.Textarea(attrs={'placeholder': _('setlist here')}),
        }
