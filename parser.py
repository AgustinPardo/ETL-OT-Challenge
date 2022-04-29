import os
import pandas as pd
import json
import math
from multiprocessing import Process, Queue, cpu_count

class DataSet:

    def __init__(self, path, name, fields):
        self.path = path+"/"+name
        self.name = name
        self.fields = fields
        self.df = None

class Parser:

    def __init__(self, data_path):
        self.path = data_path
        self.evidence = DataSet(self.path, "evidence", ["targetId", "diseaseId", "score"])
        self.target = DataSet(self.path, "targets", ["id", "approvedSymbol"])
        self.disease = DataSet(self.path, "diseases", ["id", "name"])

    def get_data(self, path, files, queue, args):
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

    def parallel_get_data(self, path, files, args):
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
            process = Process(target=self.get_data, args=(path, files[left:right], queue, args))
            process.start()
            right = left

        # Collect the queue results
        all_results = []
        for _ in range(0, num_cpus):
            all_results+=queue.get()

        return all_results

    def parse_data(self, dataset):
        files = os.listdir(dataset.path)
        data = self.parallel_get_data(dataset.path, files, dataset.fields)
        dataset.df = pd.DataFrame(data)

    def prepare_evidence(self, dataset):

        self.parse_data(dataset)
        # Calculate median score and 3 top scores per targetId and diseaseId pair
        print("Calculating median and 3 top scores of evidence data set")
        dataset.df = dataset.df.groupby(["targetId", "diseaseId"]).agg({"score": ['mean', lambda s: sorted(list(s), reverse=True)[:3]]}).reset_index()
        columns_name =("targetId", 'diseaseId', 'median', 'top3')
        dataset.df.columns = list(map(''.join, columns_name))

    def transform_data(self):
        self.prepare_evidence(self.evidence)
        self.parse_data(self.target)
        self.parse_data(self.disease)

        print("Joining evidence, target and disease dataset")
        # Join with target
        ev_ta_df = pd.merge(self.evidence.df, self.target.df, left_on="targetId", right_on="id")
        # Join with disease
        ev_ta_di_df = pd.merge(ev_ta_df, self.disease.df, left_on="diseaseId", right_on="id")
        # Remove no usable columns
        del ev_ta_di_df["id_x"]
        del ev_ta_di_df["id_y"]

        # Sort ascending on median
        print("Sorting by median score")
        self.data_transformed = ev_ta_di_df.sort_values("median").reset_index(drop=True)

    def export_data(self, out_file):
        print(f"Exporting Results to JSON file: {out_file}")
        self.data_transformed.to_json(out_file, orient="records")
        print(f"Data exported to {out_file}")

    def target_target_pair(self):

        if self.evidence.df.empty:
            self.prepare_evidence(self.evidence)

        # Join on targetID
        tt_pair = pd.merge(self.evidence.df, self.evidence.df, left_on="targetId", right_on="targetId")

        # Remove all the rows having same diseasesID
        tt_pair_dif_diseases = tt_pair[tt_pair["diseaseId_x"] != tt_pair["diseaseId_y"]]

        tt_pair_count = tt_pair_dif_diseases["targetId"].count() / 2
        print(f"Target-Target pair sharing connection with atleast two diseases {int(tt_pair_count)}")

if __name__ == "__main__":

    parser = Parser("data")
    parser.transform_data()
    parser.export_data('output.json')
    parser.target_target_pair()