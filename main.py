import argparse

import os
import copy
import pandas as pd
import subprocess

def merge_result(result_path):
    final = []
    col = None
    is_make_column = False
    for file in os.listdir(result_path):

        if "_stats.csv" in os.path.basename(file):
            try:
                data = pd.read_csv(result_path+"/"+file)
                if not is_make_column:
                    col = list(data.columns[1:])
                    col[0] = "vuser"
                    is_make_column = True
                dt =copy.deepcopy(data.values[-1][1:])
                dt[0] =file.split("_")[0]
                final.append(dt)
            except Exception as e:
                print(e)
            else:
                is_make_column = True
    final =sorted(final,key=lambda x:x[0])
    final_result = pd.DataFrame(final, columns=col)
    save_filename = "final_result_" + os.path.basename(result_path) + ".csv"
    final_result.to_csv(result_path+ "/"+ save_filename)


def create_folder_if_not_exists(folder_path):
    if os.path.exists(folder_path):
        raise Exception(f"{folder_path}  folder is already exist")
    else:
        os.makedirs(folder_path)


def make_env_file(locustfile_full_path, target_address, users, test_name, version):
    if os.path.exists("./.env"):
        os.remove("./.env")
    with open("./.env", 'w') as f:
        f.write(f"LOCUSTFILE={locustfile_full_path}\n")
        f.write(f"TARGET_ADDRESS={target_address}\n")
        f.write(f"USERS={users}\n")
        f.write(f"TEST_NAME={test_name}\n")
        f.write(f"VERSION={version}\n")


def run_docker_compose():
    print("--------start---------")
    cmd = ['docker-compose', 'up', '--scale', 'worker=4', '--force-recreate']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout:
        print(line)
    p.wait()
    print(p.returncode)

    cmd = ['docker-compose', 'down']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout:
        print(line)
    p.wait()
    print(p.returncode)
    print("--------end---------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--version', type=str)
    parser.add_argument('--locustfile_name_in_locustfiles', type=str)
    parser.add_argument('--target_address', type=str, help="172.20.93.18:8888")
    parser.add_argument('--use_warm_up', type=str, default=False, required=False)

    args = parser.parse_args()

    test_name = args.locustfile_name_in_locustfiles.replace(".py", "")
    result_folder_path = f"./result/{test_name}_{args.version}"
    locustfile_full_path = f"/mnt/locust/locustfiles/{args.locustfile_name_in_locustfiles}"
    create_folder_if_not_exists(result_folder_path)
    if args.use_warm_up:
        make_env_file(locustfile_full_path, args.target_address, 512, test_name, args.version)
    for users in [1, 32, 64, 128, 256, 512]:
        make_env_file(locustfile_full_path, args.target_address, users, test_name, args.version)
        run_docker_compose()
    merge_result(result_folder_path)
