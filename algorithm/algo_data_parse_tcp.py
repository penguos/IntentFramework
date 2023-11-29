import time
import pandas as pd
import numpy as np
import os
class TcpDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        # Check if the input file exists and is readable
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The input file does not exist: {self.file_path}")
        if not os.access(self.file_path, os.R_OK):
            raise PermissionError(f"The input file is not readable: {self.file_path}")

    # tcp record output should be periodically parsed
    def read_file_periodically(self):
        last_line_count = 0
        df = pd.DataFrame()

        while True:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                current_line_count = len(lines)

            if current_line_count > last_line_count:
                max_len = self.get_file_stat(self.file_path)
                col_names = [i for i in range(max_len)]
                data = pd.read_csv(self.file_path, sep=' ', low_memory=False, names=col_names, skiprows=range(1, last_line_count))
                updated_df = self.process_data(data)
                df = pd.concat([df, updated_df])
                print("Read total df ss data:", df.shape)
                last_line_count = current_line_count

            time.sleep(10)  # Adjust the sleep time as needed

    def get_file_stat(self, input_file):
        max_len = 0
        with open(input_file) as f:
            for line in f:
                max_len = max(max_len, len(line.split(' ')))
        return max_len

    # In different linux kernel version and TCP congestion control variants, TCP print information may have different key and value,
    # so here we parse each required key value and count them one by one.
    def process_data(self, data):
        row_sz, col_sz = data.shape
        time_list, retrans_list, retrans_done_list, rtt_list, rtt_var_list, delivery_rate_list, cwnd_list, lost_list, reorder_list, rto_list = [list() for _ in range(10)]


        # use "retrans" because some ss files has "byte_retrans"
        tcp_ss_key_retrans, tcp_ss_key_rtt, tcp_ss_key_rto, tcp_ss_key_reordering, tcp_ss_key_delivery_rate = "retrans", "rtt", "rto", "reordering", "delivery_rate"
        tcp_ss_key_cwnd, tcp_ss_key_lost = "cwnd:", "lost:"
        retrans_count, retrans_count_done = 0, 0

        for row_idx in range(row_sz):
            line = data.iloc[row_idx]
            flag_dict = {"time": False, "cwnd": False, "rtt": False, "retrans": False, "rto": False, "lost": False,
                         "reorder": False}
            for val in line:
                if val == np.nan:
                    continue

                syn_sent = False
                if val == "SYN-SENT":
                    syn_sent = True
                if syn_sent:
                    break

                if tcp_ss_key_cwnd in str(val):
                    if not flag_dict['cwnd']:
                        cwnd_list.append(float(val.split(':')[1]))
                        flag_dict['cwnd'] = True
                        # cwnd will alway present so we add time here
                        time_list.append(line[0])

                if tcp_ss_key_retrans in str(val) and '/' in str(val):
                    if flag_dict['retrans']:
                        retrans_list.pop()
                        retrans_done_list.pop()
                    retrans_list.append(int(val.split('/')[1]))
                    retrans_count += 1
                    retrans_done_list.append(int(val.split('/')[0].split(':')[1]))
                    retrans_done_list.append(0)
                    flag_dict['retrans'] = True
                    retrans_count_done += 1

                if tcp_ss_key_rtt in str(val) and "mrtt" not in str(val) and "minrtt" not in str(val) and "rcv_rtt" not in str(val):
                    if flag_dict['rtt']:
                        rtt_list.pop()
                        rtt_var_list.pop()
                    rtt_var_val = float(val.split('/')[1])
                    rtt_var_list.append(rtt_var_val)
                    rtt_list.append(float(val.split('/')[0].split(':')[1]))
                    flag_dict['rtt'] = True

                if tcp_ss_key_rto in str(val):
                    if flag_dict['rto']:
                        rto_list.pop()
                    rto_list.append(float(val.split(':')[1]))
                    flag_dict['rto'] = True

                if tcp_ss_key_reordering in str(val):
                    if flag_dict['reorder']:
                        reorder_list.pop()
                    reorder_list.append(float(val.split(':')[1]))
                    flag_dict['reorder'] = True

                if tcp_ss_key_lost in str(val):
                    if flag_dict['lost']:
                        lost_list.pop()
                    lost_list.append(float(val.split(':')[1]))
                    flag_dict['lost'] = True

            if not flag_dict['lost']:
                lost_list.append(0)

            if not flag_dict['reorder']:
                reorder_list.append(0)

            if not flag_dict['rto']:
                rto_list.append(0)

            if not flag_dict['rtt']:
                rtt_var_list.append(0)
                rtt_list.append(0)

            if not flag_dict['retrans']:
                retrans_count += 1
                retrans_list.append(0)
                retrans_done_list.append(0)

            if not flag_dict['cwnd']:
                cwnd_list.append(0)

            # make sure all required keys have same number of values
            assert len(cwnd_list) == len(rtt_var_list) == len(rtt_list) == len(retrans_list) == len(rto_list) == len(time_list)

        tcp_ss_dict = {"cwnd": cwnd_list, "rtt": rtt_list,
                       "retrans": retrans_list, "rto": rto_list, "rtt_var": rtt_var_list}

        return pd.DataFrame(tcp_ss_dict)


if __name__ == "__main__":
    processor = TcpDataProcessor('D:/data/Mininet_IWQOS/Path_Variation/BBR/normal/P1/tcp_ss_example_data')
    processor.read_file_periodically()
