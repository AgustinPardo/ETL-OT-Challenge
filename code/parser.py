import os
import pandas as pd
import json
import math
from multiprocessing import Process, Queue
from code.cpu import CPU


class DataSet:
    """Class to store dataset data"""

    def __init__(self, path, name, fields):
        self.path = path+"/"+name
        self.name = name
        self.fields = fields
        self.df = pd.DataFrame


class Parser:
    """Class to parse data from evidence, targets and diseases datasets"""

    def __init__(self, data_path, cpus_use):
        self.evidence = DataSet(data_path, "evidence", ["targetId", "diseaseId", "score"])
        self.target = DataSet(data_path, "targets", ["id", "approvedSymbol"])
        self.disease = DataSet(data_path, "diseases", ["id", "name"])
        self.cpus = CPU(cpus_use).cpus

    def get_data(self, path, files, queue, args):
        """Open each file of dataset, read as json and append result in a Queue"""

        list_for_df = []
        for file in files:
            file=open(path+"/"+file)
            readlines = file.readlines()
            file.close()
            for line in readlines:
                dict_to_list = json.loads(line)
                # Keep only args requested
                dict_to_list = {x:dict_to_list[x] for x in args}
                list_for_df.append(dict_to_list)

        # Add result to queue
        queue.put(list_for_df)

    def parallel_get_data(self, path, files, args):
        """Create chunks of files, run get_data on parallel and create a Queue to store the results"""

        # Number of CPUs
        num_cpus = self.cpus

        # Set a Queue to store each process result
        queue = Queue()

        # Set chunks to distributed over CPUs number
        num_files=len(files)
        chunk_step=math.ceil(num_files/self.cpus)

        for w in range(num_cpus):
            chunk_l=chunk_step*w
            chunk_r=chunk_step*(w+1)
            if chunk_r>num_files:
                chunk_r=num_files
            process = Process(target=self.get_data, args=(path, files[chunk_l:chunk_r], queue, args))
            process.start()
            chunk_r = chunk_l

        # Collect the queue results
        all_results = []
        for _ in range(0, num_cpus):
            all_results+=queue.get()

        return all_results

    def parse_data(self, dataset):
        """Get list of dataset files and parse them in a pandas DataFrame"""

        print(f"Reading {dataset.name} dataset")
        files = os.listdir(dataset.path)
        data = self.parallel_get_data(dataset.path, files, dataset.fields)
        print(f"Parsing {dataset.name} dataset")
        dataset.df = pd.DataFrame(data)

    def prepare_evidence(self, dataset):
        """Calculate median and 3 top scores of evidece dataset"""

        # Calculate median score and 3 top scores per targetId and diseaseId pair
        print("Calculating median and 3 top scores of evidence dataset")
        dataset.df = dataset.df.groupby(["targetId", "diseaseId"]).agg({"score": ['mean', lambda s: sorted(list(s), reverse=True)[:3]]}).reset_index()
        columns_name =("targetId", 'diseaseId', 'median', 'top3_score')
        dataset.df.columns = list(map(''.join, columns_name))

    def transform_data(self):
        """Merge evidence with target and diseases datasets. Sort by median score"""

        print(f"CPUs in use: {self.cpus}")  
        self.parse_data(self.evidence)
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
        """Export calculated statistics on the datasets"""

        self.data_transformed.to_json(out_file, orient="records")
        print(f"JSON format results exported to {out_file}")

    def target_target_pair(self):
        """Target-Target pair sharing connection with atleast two diseases calculation"""

        # In case target-target pair option(-tt) is run alone
        if self.evidence.df.empty:
            self.parse_data(self.evidence)
            self.evidence.df = self.evidence.df.drop_duplicates(["targetId", "diseaseId"]).reset_index()       

        # Join on targetId
        tt_pair = pd.merge(self.evidence.df, self.evidence.df, left_on="diseaseId", right_on="diseaseId")

        # Remove all the rows having same diseasesId
        tt_pair = tt_pair[tt_pair["targetId_x"] != tt_pair["targetId_y"]]

        # Count how many diseases are connected to both pair of targets
        tt_pair = tt_pair.groupby(['targetId_x', 'targetId_y']).size().reset_index(name="count")
        
        # Count how many pair of targets have more than 2 diseases connected. Divide by 2 to prevent count two times same pair-pair connection
        tt_pair_count = tt_pair[tt_pair["count"] >= 2]["count"].count() / 2
        print(f"Target-Target pair sharing connection with atleast two diseases {int(tt_pair_count)}")
        
        return tt_pair_count
