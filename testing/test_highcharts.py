
import pandas
from django.views.generic import TemplateView

from utils.highcharts import Highchart


class HighchartsTestView(TemplateView):
    template_name = 'tests/test_highcharts.html'

    def get_context_data(self, **kwargs):
        df = pandas.DataFrame(
            {'a': range(3), 'b': range(4, 7)},
            index=['c', 'd', 'e']
        )
        print(df)
        hc = Highchart(
            df,
            'column',
            title='Test Barchart',
            x_title='Time [h]',
            y_title='Investment [€]'
        )
        context = {'hc': hc.render('hc')}
        return context
