import pandas as pd
import os
# result_path = {test_name}_{version}

import copy

def merge_result(result_path):
    final =[]
    col=None
    is_make_column=False
    for file_path in os.listdir(result_path):

        if "_stats.py" in os.path.basename(file_path):
            try:
                data= pd.read_csv(file_path)
                if not is_make_column:
                    col= list(data.columns[1:])
                    col[0]="vuser"
                    is_make_column=True

                final.append( copy.deepcopy(data[-1][1:]))
            except Exception as e:
                print(e)
            else:
                is_make_column = True



    final_result = pd.DataFrame(final,columns=col)
    save_filename ="final_result_"+os.path.basename(result_path)+".csv"
    final_result.to_csv(result_path/save_filename)






