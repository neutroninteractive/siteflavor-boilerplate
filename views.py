from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.middleware.csrf import get_token
from django.template.loader import get_template
from django.views.generic import FormView, TemplateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse_lazy

from siteflavor.boilerplate.models import BoilerplateBlogPage
from siteflavor.boilerplate.settings import ADMIN_EMAIL_ADDRESS
from common import utils
from common.forms import ContactForm
from common.views import SchoolView
from search.views import SearchSchools


class BoilerplateSchoolView(SchoolView):
    def get_context_data(self, **kwargs):
        context = super(BoilerplateSchoolView, self).get_context_data(**kwargs)
        context['blog_entries'] = BoilerplateBlogPage.objects.filter(
            live=True).order_by('-date')[:3]
        return context


class BoilerplateSearchSchools(SearchSchools):
    def get_context_data(self, **kwargs):
        context = super(BoilerplateSearchSchools, self).get_context_data(**kwargs)
        context['blog_entries'] = BoilerplateBlogPage.objects.filter(
            live=True).order_by('-date')[:3]
        return context


class ContactFormView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    template_name = 'boilerplate/boilerplate_contact_page.html'
    email = ADMIN_EMAIL_ADDRESS

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        context['admin_email_address'] = self.email
        return context

    def form_valid(self, form):
        context = form.cleaned_data
        email_template = get_template('email/contact.html')
        email_rendered = email_template.render(context)
        email = EmailMultiAlternatives(
            subject='Positron Contact Form',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.email],
        )
        email.attach_alternative(email_rendered, 'text/html')
        email.send()
        return TemplateResponse(request=self.request,
                                template=self.template_name,
                                context=context,
                                status=200)

    def form_invalid(self, form):
        token = get_token(self.request)
        context = self.get_context_data(form=form)
        context.update({'csrf_token': token})

        return TemplateResponse(request=self.request,
                                template=self.template_name,
                                context=context,
                                status=400)


class RobotsFile(utils.AbsoluteUrlMixin, TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'


class LocationsFile(utils.AbsoluteUrlMixin, TemplateView):
    template_name = 'locations_lookup.html'
    content_type = 'text/html'

