from os.path import dirname, join

import pandas as pd
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter, TextInput
from bokeh.io import curdoc
import IndeedSearch

df = pd.DataFrame()
source = ColumnDataSource(df)


def search():
    data_table.columns = [TableColumn(field="name", title="Loading...")]
    df = IndeedSearch.main(query.value, location.value, radius.value)
    column_names = [
        TableColumn(field=c, title=c) for c in df.columns.values
        ]
    data_table.columns = column_names
    data_table.source = ColumnDataSource(df)
    return


columns = [TableColumn(field="name", title="Job Search")]
data_table = DataTable(source=source, columns=columns, width=1100, height=500)
query = TextInput(title="Job Title", value='')
location = TextInput(title="Location", value='')
radius = TextInput(title="Radius", value='')
search_button = Button(label="Search", button_type="success", width=180)
search_button.on_click(search)
download_button = Button(label="Download", button_type="success", width=180)
download_button.callback = CustomJS(args=dict(source=data_table.source), code='download.js')


controls = widgetbox(search_button, download_button)
table = widgetbox(data_table)
text = widgetbox(query, location, radius)
left_column = column(text, controls)
curdoc().add_root(row(left_column, table))
curdoc().title = "Indeed Job Search"
