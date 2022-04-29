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

if __name__ == '__main__':

    start = time.time()
    files_evidence = os.listdir("data/evidence/")
    files_targets = os.listdir("data/targets")
    files_diseases = os.listdir("data/diseases")
    evidence = parallel_get_data("data/evidence", files_evidence, "targetId", "diseaseId", "score")
    target = parallel_get_data("data/targets", files_targets, "id", "approvedSymbol")
    disease = parallel_get_data("data/diseases", files_diseases, "id", "name")

    df_evidence = pd.DataFrame(evidence)
    df_target = pd.DataFrame(target)
    df_disease = pd.DataFrame(disease)

    print(df_evidence.shape)
    print(df_target.shape)
    print(df_disease.shape)

    #df = pd.merge(df_evidence, df_target, left_on="targetId", right_on="id")




