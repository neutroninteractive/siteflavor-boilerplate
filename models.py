from django.db import models
from django import forms

from copy import deepcopy
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from common import utils
from common.constants import common_constants
from common.forms import ContactForm
from common.models.blog_models import BlogCategory
from common.mixins import DynamicPhoneNumberMixin
from search.views import SearchSchools
from search.forms import SchoolShortForm
from search.mixins import ShortformModalMixin
from siteflavor.boilerplate.settings import ADMIN_EMAIL_ADDRESS


class BoilerplateIndexPage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateIndexPage, self).get_context(request, *args, **kwargs)
        blog_entries = BoilerplateBlogPage.objects.order_by(
            '-date').live()[:3]
        context.update({'blog_entries': blog_entries, 'breadcrumbs': 'false'})
        return context

    def serve(self, request, *args, **kwargs):
        return SearchSchools.as_view()(request,
                                       context=self.get_context(request))


class BoilerplatePage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplatePage, self).get_context(request, *args, **kwargs)
        context.update({'states': common_constants.STATES})
        return context


class BoilerplateContactPage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):
    body = RichTextField()
    email = ADMIN_EMAIL_ADDRESS

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateContactPage, self).get_context(request, *args, **kwargs)
        context.update({'states': common_constants.STATES, 'form': ContactForm, 'admin_email_address': self.email})
        return context


class BoilerplateAboutPage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):
    heading = models.CharField(max_length=255, default='')
    sub_heading = RichTextField()
    body = RichTextField()
    cta_heading = models.CharField(max_length=255, default='')
    cta_sub_heading = models.CharField(max_length=255, default='')
    cta_text = models.CharField(max_length=255, default='')

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="title"),
        FieldPanel('sub_heading', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('cta_heading', classname="full"),
        FieldPanel('cta_sub_heading', classname="full"),
        FieldPanel('cta_text', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateAboutPage, self).get_context(request, *args, **kwargs)
        context.update({'states': common_constants.STATES, 'form': ContactForm})
        return context


class BoilerplateLandingPage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):
    sub_title = models.CharField(max_length=255, default='')
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('sub_title', classname="full"),
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateLandingPage, self).get_context(request, *args, **kwargs)
        blog_entries = BoilerplateBlogPage.objects.order_by(
            '-date').live()[:3]
        prefill_params = {}
        utils.save_search_variables_get(request, school_search=True)
        if request.session.get('prepop_params'):
            prefill_params.update(request.session.get('prepop_params'))
        if request.session.get('search_params'):
            prefill_params.update(request.session.get('search_params'))
        get_data = deepcopy(request.GET) if request else {}
        prefill_params.update(get_data.dict())
        if not prefill_params.get('adid'):
            prefill_params.update({'adid': 'organic'})
        short_form = SchoolShortForm(initial=prefill_params)

        context.update({'blog_entries': blog_entries, 'short_form': short_form})
        return context


class BoilerplateBlogIndexPage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):

    sub_title = models.CharField(max_length=255, default='')

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateBlogIndexPage, self).get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        context['blog_entries'] = BoilerplateBlogPage.objects.order_by('-date').child_of(self).live()
        return context

    # Parent page / subpage type rules

    parent_page_types = ['boilerplate.BoilerplateIndexPage']
    subpage_types = ['boilerplate.BoilerplateBlogPage']


class BoilerplateBlogPage(DynamicPhoneNumberMixin, ShortformModalMixin, Page):

    # Database fields

    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    categories = ParentalManyToManyField(BlogCategory, blank=True)
    tags = ClusterTaggableManager(through='BoilerplateBlogPageTag', blank=True)


    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]


    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]


    # Parent page / subpage type rules

    parent_page_types = ['boilerplate.BoilerplateBlogIndexPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super(BoilerplateBlogPage, self).get_context(request)
        blog_entries = BoilerplateBlogPage.objects.sibling_of(self, inclusive=False).live()
        blog_entries = blog_entries.order_by('-date')[:3]

        # Add extra variables and return the updated context
        prefill_params = {}
        utils.save_search_variables_get(request, school_search=True)
        if request.session.get('prepop_params'):
            prefill_params.update(request.session.get('prepop_params'))
        if request.session.get('search_params'):
            prefill_params.update(request.session.get('search_params'))
        get_data = deepcopy(request.GET) if request else {}
        prefill_params.update(get_data.dict())
        if not prefill_params.get('adid'):
            prefill_params.update({'adid': 'organic'})
        short_form = SchoolShortForm(initial=prefill_params)
        context.update({'blog_entries': blog_entries, 'short_form': short_form})
        return context


class BoilerplateBlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BoilerplateBlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BoilerplateBlogPageRelatedLink(Orderable):
    page = ParentalKey(BoilerplateBlogPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
