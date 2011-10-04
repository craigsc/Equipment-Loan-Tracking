from django.db import models
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django.contrib.auth.models import User


class Person(models.Model):
    '''
    A person capable of borrowing.
    '''
    gtid = models.CharField(max_length=9, blank=False, unique=True, verbose_name="GT ID")
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)


class Item(models.Model):
    '''
    An item that TSO can loan out.
    '''
    serial_number = models.CharField(blank=True, null=True, max_length=255, unique=True)
    description = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        '''Null out serial number if blank, make it all caps otherwise'''
        if not self.serial_number:
            self.serial_number = None
        else:
            self.serial_number = self.serial_number.upper()
        super(Item, self).save(*args, **kwargs)


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    location_field = models.CharField(max_length=100, verbose_name="Location")
    notes_field = models.TextField(verbose_name="Notes", blank=True)
    loan_datetime = models.DateTimeField(auto_now_add=True,
                                         verbose_name="Date Loaned")
    return_datetime = models.DateTimeField(null=True,
                                           verbose_name="Date Returned")
    returned_to = models.ForeignKey(User, blank=True, null=True)
    item = models.ForeignKey(Item, blank=False)
    loaned_to = models.ForeignKey(Person, blank=False)

    def __unicode__(self):
        return self.id


class DivFormMixin:
    '''
    Mix this into a django.forms.Form to enable a new output method 'as_div' that
    will output divs for use with blueprint.css
    '''
    def as_div(self):
        "Returns this form rendered as HTML <divs>s"
        return self._html_output(
            normal_row=u'<div class="span-13 last"><div class="span-3">%(label)s%(errors)s</div><div class="span-10 last">%(field)s</div>%(help_text)s</div>',
            error_row=u'<div class="error span-13 last">%s</div>',
            row_ender=u'</div>',
            help_text_html=u'<div class="quiet legend prepend-3 span-10 last">%s</div>',
            errors_on_separate_row=False)


class LoanForm(ModelForm, DivFormMixin):
    class Meta:
        model = Loan
        exclude = ('item', 'return_datetime', 'returned_to',)
    loaned_to = ModelChoiceField(queryset=Person.objects, widget=HiddenInput)


class ItemForm(ModelForm, DivFormMixin):
    class Meta:
        model = Item


class PersonForm(ModelForm, DivFormMixin):
    class Meta:
        model = Person
