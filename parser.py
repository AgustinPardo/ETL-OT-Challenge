import os
import time
import pandas as pd
import json
import math
from multiprocessing import Process, Queue, cpu_count

def get_data(path, files, queue, *args):
    list_for_df = []
    for file in files:
        file=open(path+"/"+file)
        readlines = file.readlines()
        file.close()
        for line in readlines:
            dict_to_list = json.loads(line)
            # Keep only args requested data
            dict_to_list = {x:dict_to_list[x] for x in args}
            list_for_df.append(dict_to_list)

    # Add result to queue
    queue.put(list_for_df)

def parallel_get_data(path, files, *args):
    # Set number of CPUs
    # num_workers = cpu_count()
    num_cpus = 6

    # Set a Queue to store each process result
    queue = Queue()

    # Set chunks to distributed over CPUs number
    num_files=len(files)
    chunk_step=math.ceil(num_files/num_cpus)

    for w in range(num_cpus):
        left=chunk_step*w
        right=chunk_step*(w+1)
        if right>num_files:
            right=num_files
        process = Process(target=get_data, args=(path, files[left:right], queue, *args))
        process.start()
        right = left

    # Collect the queue results
    all_results = []
    for _ in range(0, num_cpus):
        all_results+=queue.get()

    return all_results

def parse_data(files_path, *args):

    files = os.listdir(files_path)
    data = parallel_get_data(files_path, files, *args)
    dataframe = pd.DataFrame(data)

    return dataframe


def tranform_data():
    evidence_df = parse_data("data/evidence/", "targetId", "diseaseId", "score")
    target_df = parse_data("data/targets/", "id", "approvedSymbol")
    diseases_df = parse_data("data/diseases/", "id", "name")

    # Calculate median score and 3 top scores per targetId and diseaseId pair
    print("Calculating Median and 3 top scores")
    evidence_df = evidence_df.groupby(["targetId", "diseaseId"]).agg({"score": ['mean', lambda s: sorted(list(s), reverse=True)[:3]]}).reset_index()
    columns_name =("targetId", 'diseaseId', 'median', 'top3')
    evidence_df.columns = list(map(''.join, columns_name))

    print("Joining evidence, target and disease dataset")
    # Join with target
    ev_ta_df = pd.merge(evidence_df, target_df, left_on="targetId", right_on="id")
    # Join with disease
    ev_ta_di_df = pd.merge(ev_ta_df, diseases_df, left_on="diseaseId", right_on="id")
    # Remove no usable columns
    del ev_ta_di_df["id_x"]
    del ev_ta_di_df["id_y"]

    # Sort ascending on median
    print("Sorting by median score")
    ev_ta_di_df = ev_ta_di_df.sort_values("median").reset_index(drop=True)

    return ev_ta_di_df

def export_data(df, out_file):
    print(f"Exporting Results to JSON file: {out_file}")
    df.to_json(out_file, orient="records")
    print(f"Data exported to {out_file}")

def target_target_pair(df):
    df1 = df
    df2 = df
    # Join on targetID
    tt_pair = pd.merge(df1, df2, left_on="targetId", right_on="targetId")

    # Remove all the rows having same diseasesID
    tt_pair_dif_diseases = tt_pair[tt_pair["diseaseId_x"] != tt_pair["diseaseId_y"]]

    tt_pair_count = tt_pair_dif_diseases["targetId"].count() / 2
    print(f"Target-Target pair sharing connection with atleast two diseases {int(tt_pair_count)}")

if __name__ == "__main__":
    # ARG_PARSER = argparse.ArgumentParser()
    # ARG_PARSER.add_argument(
    #     "--datadir",
    #     help="Directory where evidence, targets and diseases are stored",
    #     default="data",
    # )
    # ARG_PARSER.add_argument(
    #     "--outfile",
    #     help="The name of the output file where results will be stored",
    #     default="evidence_mt3.json",    )

    # CLI_ARGS = ARG_PARSER.parse_args()
    # data_dir = CLI_ARGS.datadir
    # outfile = CLI_ARGS.outfile

    # print(data_dir, outfile)

    df = tranform_data()
    export_data(df, "output.json")
    target_target_pair(df)
    