from django.db import models
from django.forms import ModelForm


class Item(models.Model):
    '''
    An item that TSO can loan out.
    '''
    description = models.TextField(blank=False)


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    location_field = models.CharField(max_length=100, verbose_name="Location")
    contact_field = models.EmailField(verbose_name="Contact Email")
    notes_field = models.TextField(verbose_name="Notes")
    item = models.ForeignKey(Item, blank=False)

    def __unicode__(self):
        return self.id


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        exclude = ('item')


class ItemForm(ModelForm):
    class Meta:
        model = Item
