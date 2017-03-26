from spyre import server
import pandas as pd
import Indeed


class IndeedJobSearch(server.App):
    title = "Indeed Job Search"

    inputs = [{"type": "text",
               "key": "words",
               "label": "write words here",
               "value": "hello world",
               "action_id": "update_data"}]

    controls = [{"type": "button",
                 "id": "update_data"}]


    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": False}]

    def getData(self, params):
        # ticker = params['ticker']
        df = Indeed.create_df('mechanical engineer', 'baltimore', '50')
        return df

app = IndeedJobSearch()
app.launch(port=9093)
