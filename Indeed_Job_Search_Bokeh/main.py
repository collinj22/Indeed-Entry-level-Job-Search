from os.path import dirname, join

import pandas as pd
from bokeh.layouts import row, widgetbox, column, layout
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter, TextInput
from bokeh.io import curdoc
import IndeedSearch

df = pd.DataFrame()
source = ColumnDataSource(df)


def search():
    data_table.columns = [TableColumn(field="name", title="Loading...")]
    df = IndeedSearch.main(query.value, location.value, radius.value)
    column_names = [TableColumn(field=c, title=c) for c in df.columns.values]
    data_table.columns = column_names
    data_table.source = ColumnDataSource(df)
    return


columns = [TableColumn(field="name", title="Job Search")]
data_table = DataTable(source=source, columns=columns, width=1100, height=500, editable=True)
query = TextInput(title="Job Title", value='', width=200)
location = TextInput(title="Location", value='', width=200)
radius = TextInput(title="Radius", value='', width=200)
search_button = Button(label="Search", button_type="success", width=200)
search_button.on_click(search)
download_button = Button(label="Download", button_type="success", width=200)
download_button.callback = CustomJS(args=dict(source=data_table.source), code='download.js')

control_row = row(query, location, radius, search_button)
curdoc().add_root(row(control_row, data_table))
curdoc().title = "Indeed Job Search"
