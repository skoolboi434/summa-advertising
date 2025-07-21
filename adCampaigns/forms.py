from django import forms
from .models import AdvertisingCampaignSummary

class AdCampaignForm(forms.ModelForm):
    class Meta:
        model = AdvertisingCampaignSummary
        fields = ['campaign_name', 'contact_id', 'start_date', 'end_date', 'brief']  # Update as needed
