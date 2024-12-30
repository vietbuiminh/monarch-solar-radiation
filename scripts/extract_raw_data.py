import pandas as pd
import glob
import os

directory_path = ''  # parse directoy here
files = glob.glob(os.path.join(directory_path, '*.txt'))
csv_file_path = ''  # parse location to save csv file here

# df = pd.read_csv('working_pyro_new_combined_logs.csv')
# print(df)
# uncomment all of this for the first time run. otherwise using the combined_log.csv
df = pd.DataFrame()


def getting_file_no(file_path):
    file_name = os.path.basename(file_path)
    file_no = int(file_name[3:-4])
    return file_no


files.sort(key=getting_file_no)
start_file_no = 15
end_file_no = 15
desired_order = ['Time [UTC]',
                 ' PresOB [mBar]',
                 ' RH_OB [%]',
                 ' TempOB [C]',
                 ' Temp RTC [C]',
                 ' Bat [V]',
                 ' Pyro [uV]',
                 ' R_u [deg]',
                 ' P_u [deg]',
                 ' UVA_u',
                 ' UVB_u',
                 ' White_u',
                 ' Vis_u [lx]',
                 ' IR_S_u',
                 ' IR_M_u',
                 ' PyroT_u [C]',
                 '']
for file_path in files:
    if getting_file_no(file_path) < start_file_no or getting_file_no(file_path) > end_file_no:
        continue
    else:
        print(f'Reading file: {file_path}')
        with open(file_path, 'r') as file:
            skipped_line = file.readline().strip()
            if not skipped_line:
                print(f'Skipping empty file: {file_path}')
                continue
            column_head = ""
            if skipped_line[0:2] == '20':
                print(
                    f'File {file_path} has no heading, applying manual heading')
                column_head = "Time [UTC], PresOB [mBar], RH_OB [%], TempOB [C], Temp RTC [C], Bat [V], Pyro [uV], R_u [deg], P_u [deg], UVA_u, UVB_u, White_u, Vis_u [lx], IR_S_u, IR_M_u, PyroT_u [C],".strip()
                column_head = column_head.split(',')
                df_temp = pd.DataFrame([skipped_line.split(',')
                                        for line in skipped_line], columns=column_names)
                df_temp = df_temp[desired_order]
                df_combined = pd.concat([df, df_temp])
                df_combined.reset_index(drop=True, inplace=True)
                df = df_combined
            else:
                column_head = file.readline().strip()
                column_names = column_head.split(',')
            for i in range(len(column_names)):
                if column_names[i] == " Kipp and Zonen Voltage [uV]":
                    column_names[i] = ' Pyro [uV]'
                if column_names[i] == " IR_M_u [mV]":
                    column_names[i] = ' IR_M_u'
                if column_names[i] == " IR_S_u [mV]":
                    column_names[i] = ' IR_S_u'
            lines = file.readlines()
            df_temp = pd.DataFrame([line.strip().split(',')
                                   for line in lines], columns=column_names)
            # df_temp = df_temp[desired_order]
            # print(df_temp['Time [UTC]'])
            df_combined = pd.concat([df, df_temp])
            df_combined.reset_index(drop=True, inplace=True)
            df = df_combined
            # csv_file_path = file_path.replace('.txt', '.csv')
            # df_combined.to_csv(csv_file_path, index=False)
            # print(f'Saved to CSV: {csv_file_path}')

            # break

        # break

df.to_csv(csv_file_path, index=False)
print(f'Saved combined data to CSV: {csv_file_path}')
