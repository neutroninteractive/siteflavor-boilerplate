from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps import views as wagtail_views

from common.external.academix_direct.controller import AcademixDirectController
from common.external.campus_explorer.controller import CampusExplorerController
from common.external.neutron_interactive.controller import NeutronInteractiveController
from common.external.provide_media.controller import ProvideMediaController
from common.external.quinstreet.controller import QuinstreetVocationalController
from common.external.thruline_marketing.controller import ThrulineMarketingController
from common.external.edu_maximizer.controller import EduMaximizerController
from common.external.lead_current.controller import LeadCurrentController
from common.urls import commonpatterns, staticpatterns
from common.views import UnsubscribeFormView, deployinfo, SchoolNameRedirectView, SchoolConfirmationRedirect, SchoolIndexView, StateIndexView, CityIndexView, GainfulEmploymentView
from offer.urls import externalofferpatterns, offerpatterns
from offer.views import QuinstreetSmsOffer
from search.views import SchoolShortFormSubmit, ConfirmationView
from siteflavor.boilerplate.views import BoilerplateSchoolView, BoilerplateSearchSchools, ContactFormView, RobotsFile
from siteflavor.boilerplate.sitemaps import SchoolsSitemap
from .sitemaps import StaticViewSitemap

admin.autodiscover()

sitemaps = {
    'static': StaticViewSitemap,
    'cms': wagtail_views.Sitemap,
    'schools': SchoolsSitemap,
}

confirmationpatterns = [
    url(r'^(?P<page>.+\.html)$', ConfirmationView.as_view(), name='custom'),
]

urlpatterns = [
    url(r'^robots.txt$', RobotsFile.as_view(), name="robots_file"),
    url(r'^sitemap\.xml$', wagtail_views.index, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', wagtail_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^common/', include(commonpatterns, namespace='common')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^external-offer/', include(externalofferpatterns, namespace='external_offer')),
    url(r'^offer/', include(offerpatterns, namespace='offer')),
    url(r'^schools/shortform/submit/$',
        SchoolShortFormSubmit.as_view(), name='school_shortform'),
    url(r'^schools/search/', BoilerplateSearchSchools.as_view(), name='school_search'),
    url(r'^schools/confirmation/', SchoolConfirmationRedirect.as_view(),
        name='school_confirmation_redirect'),
    url(r'^schools/(?P<state>[-\w]+)/(?P<city>[-\w]+)/(?P<slug>[-\w]+)/(?P<unit_id>\d+)/$',
        BoilerplateSchoolView.as_view(), name='school'),
    url(r'^schools/(?P<state>[-\w]+)/(?P<city>[-\w]+)/$',
        CityIndexView.as_view(), name='city_index'),
    url(r'^schools/(?P<state>[-\w]+)/$', StateIndexView.as_view(),
        name='state_index'),
    url(r'^schools/', SchoolIndexView.as_view(),
        name='school_index'),
    url(r'^school/redirect/(?P<pk>\d+)/$', SchoolNameRedirectView.as_view(),
        name='school_name_redirect'),
    url(r'^sms-offer-submit/', QuinstreetSmsOffer.as_view(), name='sms_offer_submit'),
    url(r'^confirmation/', include(confirmationpatterns, namespace='confirmation')),
    url(r'^unsubscribe/', UnsubscribeFormView.as_view(), name='unsubscribe'),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^contact-form/', ContactFormView.as_view(), name='contact-form'),
    url(r'^', include(staticpatterns, namespace='static')),
    url(r'^deployinfo', deployinfo),
    url(r'^external/campus-explorer/submit/(?P<config_pk>\d+)/',
        CampusExplorerController.as_view(), name='campus_explorer'),
    url(r'^external/thruline-marketing/submit/(?P<config_pk>\d+)/',
        ThrulineMarketingController.as_view(), name='thruline_marketing'),
    url(r'^external/academix-direct/submit/(?P<config_pk>\d+)/',
        AcademixDirectController.as_view(), name='academix_direct'),
    url(r'^external/quinstreet-vocational/submit/(?P<config_pk>\d+)/',
        QuinstreetVocationalController.as_view(), name='quinstreet_vocational'),
    url(r'^external/provide-media/submit/(?P<config_pk>\d+)/',
        ProvideMediaController.as_view(), name='provide_media'),
    url(r'^external/edu-maximizer/submit/(?P<config_pk>\d+)/',
        EduMaximizerController.as_view(), name='edu_maximizer'),
    url(r'^external/lead-current/submit/(?P<config_pk>\d+)/',
        LeadCurrentController.as_view(), name='lead_current'),
    url(r'^external/neutron-interactive/submit/',
        NeutronInteractiveController.as_view(), name='neutron_interactive'),
    url(r'^gainful-employment', GainfulEmploymentView.as_view(),
        name='gainful_employment')
]

urlpatterns += [
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^', include(wagtail_urls)),
]

urlpatterns += staticfiles_urlpatterns()
