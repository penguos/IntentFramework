import pandas as pd
import os

class HologramDataProcessor:
    # Initialize input file name, number of rows to skip, and output file name
    # we need to skip some rows since there are some non-formated lines when application starts
    def __init__(self, input_file_name, skip_rows, output_file_name):
        self.input_file_name = input_file_name
        self.skip_rows = skip_rows
        self.df = None
        self.output_file_name = output_file_name

        # Check if the input file exists and is readable
        if not os.path.isfile(self.input_file_name):
            raise FileNotFoundError(f"The input file does not exist: {self.input_file_name}")
        if not os.access(self.input_file_name, os.R_OK):
            raise PermissionError(f"The input file is not readable: {self.input_file_name}")

        # Check if the output file is writable
        # This check creates the file if it does not exist
        try:
            with open(self.output_file_name, 'a'):
                pass
        except IOError:
            raise PermissionError(f"The output file is not writable: {self.output_file_name}")

    # Define column names for reading the file
    def read_and_filter_data(self):
        columns = [
                'log_level', 'name', 'action', 'HoloMsg', 'direction', 'dst_ip', 'port',
                'port_val', 'frame_type', 'frame_type_val', 'frame_id', 'frame_id_val',
                'frame_len', 'frame_len_val', 'frame_timestamp', 'frame_timestamp_val',
                'total_sent_len', 'total_sent_len_val'
            ]
        self.df = pd.read_csv(self.input_file_name, delim_whitespace=True, header=None,
                                  skipinitialspace=True, skiprows=self.skip_rows, nrows=None, names=columns,
                                  low_memory=False)
        self.df = self.df[self.df['direction'] == 'to']
        self.df['port_val'] = pd.to_numeric(self.df['port_val'], errors='coerce')
        self.df = self.df.dropna(subset=['port_val'])

    def group_and_sort_data(self):
        # Group by port value and sort each group by frame ID and timestamp
        self.df = self.df.groupby('port_val').apply(
            lambda x: x.sort_values(['frame_id_val', 'frame_timestamp_val'])).reset_index(drop=True)

    # Convert timestamp column to numeric type and calculate time differences
    def calculate_time_differences(self):
        self.df['frame_timestamp_val'] = pd.to_numeric(self.df['frame_timestamp_val'], errors='coerce')
        self.df['timestamp_diff'] = self.df.groupby('frame_id')['frame_timestamp_val'].diff()

    def save_df_to_csv(self):
        self.df.to_csv(self.output_file_name, sep='\t', index=False, float_format='%.0f')

    def process(self):
        self.read_and_filter_data()
        self.group_and_sort_data()
        self.calculate_time_differences()
        self.save_df_to_csv()

if __name__ == "__main__":
    processor = HologramDataProcessor()
    processor.read_file_periodically()