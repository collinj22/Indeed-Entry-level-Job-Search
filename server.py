from spyre import server
import Indeed
import pandas as pd
import openpyxl
import time
import os
import io
server.include_df_index = True
pd.set_option('display.max_colwidth', -1)

class IndeedJobSearch(server.App):
    title = "Indeed Job Search"

    inputs = [{"type": "text",
               "key": "job",
               "label": "Job Title",
               "action_id": "update_data"},
              {"type": "text",
               "key": "location",
               "label": "Location",
               "action_id": "update_data"},
              {"type": "text",
               "key": "radius",
               "label": "Radius",
               "action_id": "update_data"}]

    controls = [{"type": "button",
                 "label": "Search",
                 "id": "update_data"},
                {"type": "button",
                 "label": "Download Excel File",
                 "id": "results_csv"}]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": False},
               {'type': 'download',
                'id': 'results_csv',
                'on_page_load': False}]

    def getData(self, params):
        df = Indeed.main(params['job'], params['location'], params['radius'])
        return df

    def getDownload(self, params):
        df = self.getData(params)
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, encoding='utf-8')
        filepath = buffer
        return filepath

if __name__ == '__main__':
    app = IndeedJobSearch()
    app.launch(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))
