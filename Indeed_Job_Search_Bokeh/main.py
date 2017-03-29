from os.path import dirname, join

import pandas as pd
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter, TextInput
from bokeh.io import curdoc
import IndeedSearch

# source = ColumnDataSource(data=dict())

df = pd.DataFrame()
source = ColumnDataSource(df)


def search():
    df = IndeedSearch.main(query.value, location.value, radius.value)
    column_names = [
        TableColumn(field=c, title=c) for c in df.columns.values
        ]
    data_table.columns = column_names
    data_table.source = ColumnDataSource(df)
    return


query = TextInput(title="Job Title", value='')
location = TextInput(title="Location", value='')
radius = TextInput(title="Radius", value='')
search_button = Button(label="Search", button_type="success")
search_button.on_click(search)
# download_button = Button(label="Download", button_type="success")
# download_button.callback = CustomJS(args=dict(source=source),
#                                     code=open(join(dirname(__file__), "download.js")).read())

columns = [
    TableColumn(field="name", title="Job Search"),
]
data_table = DataTable(source=source, columns=columns, width=800)
controls = widgetbox(search_button)
table = widgetbox(data_table)
text = widgetbox(query, location, radius)
curdoc().add_root(row(controls, text, table))
curdoc().title = "Indeed Job Search"
