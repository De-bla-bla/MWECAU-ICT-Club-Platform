from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MembershipInfoView(LoginRequiredMixin, TemplateView):
    """Membership information page"""
    template_name = 'membership/info.html'
    login_url = 'accounts:login'

