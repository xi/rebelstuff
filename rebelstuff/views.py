import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from .models import Stuff


class CalendarView(PermissionRequiredMixin, TemplateView):
    permission_required = 'rebelstuff.view_booking'
    template_name = 'rebelstuff/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stuff_list'] = Stuff.objects.all()

        year = self.kwargs['year']
        month = self.kwargs['month']
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
