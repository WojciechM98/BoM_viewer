import pandas as pd
import json


class BoM:

    def __init__(self):
        self.file_path = None
        self.df = None
        self.json_settings = None
        self.import_json()

    def import_json(self):
        try:
            with open('settings.json', 'r') as file:
                self.json_settings = json.load(file)
        except:
            print("Cannot open settings json file")

    def reorder_columns(self):
        """JSON file must be specified for this function to work"""
        columns_order = list(self.json_settings["columns"].values())
        remaining_columns = [col for col in self.df if col not in columns_order]
        self.df = self.df[columns_order + remaining_columns]

    def load_file(self, excel_filepath):
        self.file_path = excel_filepath
        try:
            self.df = pd.read_csv(self.file_path)
        except ValueError:
            self.df = pd.read_excel(self.file_path)
        finally:
            if self.json_settings is not None:
                self.reorder_columns()

    def save_file(self, file_path):
        self.df.to_excel(file_path, index=False)

    def search_for_value(self, column, value):
        try:
            data = self.df.loc[self.df[column] == value]
        except:
            print("No data found")
        else:
            print(data)

    def list_differences(self, bom1_df, bom2_df):
        self.df = bom1_df
        data = []
        for index, row in bom1_df.iterrows():
            if row[self.json_settings["columns"]["Manufacturer Part Number"]]:
                data.append(bom2_df.index[bom2_df[self.json_settings["columns"]["Manufacturer Part Number"]]
                                     == row[self.json_settings["columns"]["Manufacturer Part Number"]]].tolist())
        return data

    def merge_and_sum_duplicates(self, dataframes: []):
        # Combine three dataframes
        combined_df = pd.concat(dataframes)

        # Remember oryginal column order
        original_columns = combined_df.columns.tolist()

        # Check dupes based on 'Manufacturer Part Number' column
        # Sum values 'Qty' for dupes and combine values in 'Reference' column
        combined_df = combined_df.groupby('Manufacturer Part Number', as_index=False).agg({
            'Qty': 'sum',  # sum 'Qty' column
            'Reference': lambda x: ', '.join(x),  # combine values in 'Reference'
            **{col: 'first' for col in combined_df.columns if
               col not in ['Manufacturer Part Number', 'Qty', 'Reference']}
        })

        # Revert oryginal column order
        combined_df = combined_df[original_columns]

        self.df = combined_df

    def extract_differences(self, bom1_df, bom2_df):
        data = self.list_differences(bom1_df, bom2_df)
        print(data)
        if data:
            for row in data:
                print(row)
                self.df.drop(data[0], errors="ignore", inplace=True)

    def sum_qty(self, bom1):

        for bom in list_of_boms:
            pass
        # data = self.list_differences(bom1_df, bom2_df)





    def combine_dataframes(self, bom1_df, bom2_df):
        self.df = pd.concat([bom1_df, bom2_df], ignore_index=True)

