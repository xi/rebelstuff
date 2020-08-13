import datetime
import zipfile

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.http import HttpResponse
from django.template import Context
from django.template import Template
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import BaseDetailView

from .models import Booking
from .models import Stuff


class CalendarView(PermissionRequiredMixin, TemplateView):
    permission_required = 'rebelstuff.view_booking'
    template_name = 'rebelstuff/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stuff_list'] = Stuff.objects.all()

        today = datetime.date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        context['date_list'] = []
        for i in range(31):
            try:
                context['date_list'].append(datetime.date(year, month, i + 1))
            except ValueError:
                break

        day = datetime.timedelta(days=1)
        context['prev'] = context['date_list'][0] - day
        context['next'] = context['date_list'][-1] + day

        # for django admin template
        context['title'] = _('Calendar')
        context['site_header'] = 'RebelStuff'
        context['site_title'] = 'RebelStuff'
        context['has_permission'] = True

        return context


class ContractView(PermissionRequiredMixin, BaseDetailView):
    model = Booking
    permission_required = 'rebelstuff.view_booking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.object
        context['item_list'] = self.object.bookingitem_set.all()
        return context

    def render_content(self):
        with open(settings.CONTRACT_TEMPLATE, 'r') as fh:
            template = Template(fh.read())
        context = Context(self.get_context_data())
        return template.render(context)

    def get(self, request, *args, **kwargs):
        if not settings.CONTRACT_TEMPLATE or not settings.CONTRACT_REFERENCE:
            raise Http404

        self.object = self.get_object()

        response = HttpResponse(
            content_type='application/vnd.oasis.opendocument.text',
        )

        response['Content-Disposition'] = 'attachment; filename="%s_%s.odt"' % (
            self.object.start.strftime('%Y-%m-%d'),
            slugify(self.object.name),
        )

        zresponse = zipfile.ZipFile(response, 'w')
        with zipfile.ZipFile(settings.CONTRACT_REFERENCE, 'r') as zin:
            for name in zin.namelist():
                if name == 'content.xml':
                    content = self.render_content().encode('utf8')
                else:
                    with zin.open(name, 'r') as fh:
                        content = fh.read()
                with zresponse.open(name, 'w') as fh:
                    fh.write(content)

        return response
