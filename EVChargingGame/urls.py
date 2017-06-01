from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^$', 'subscribe.views.subscribe'),
    	#url(r'^$', RedirectView.as_view(url='/accounts/login/')),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^subscribe/$', 'subscribe.views.subscribe'),
		url(r'^about/$', 'subscribe.views.about'),
		url(r'^webapp/', include('webapp.urls')),
		url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),
	    url(r'^accounts/', include('allauth.urls')),
	    url(r'^start/', 'webapp.views.quiz'),
	    url(r'^go/', 'webapp.views.go'),
	    url(r'^go_again/', 'webapp.views.go2'),
	    url(r'^jair/', 'webapp.views.aamas'),
	    url(r'^ijcai/', 'webapp.views.aamas'),
	    url(r'^orchid/', 'webapp.views.orchid'),
	    url(r'^leaderboard/', 'webapp.views.orchidLeaderboard')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
