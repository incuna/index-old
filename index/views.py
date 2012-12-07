import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from incuna.utils import class_view_decorator
from social_auth.exceptions import AuthFailed
from social_auth.views import complete

from .models import CardImage, IndexCard, Tag


logger = logging.getLogger(__name__)


class HomeView(ListView):
    """Index page lists all cards."""
    template_name = 'home.html'

    def get_queryset(self):
        """Shows recent image for every Card Image."""
        return CardImage.objects.order_by('indexcard', '-id').distinct('indexcard')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


@class_view_decorator(login_required)
class IndexCardDetail(DetailView):
    model = IndexCard


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed as e:
            logger.error(e)
            messages.error(request, "Your Google Apps domain isn't authorized for this app")
            return HttpResponseRedirect('/')


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)

