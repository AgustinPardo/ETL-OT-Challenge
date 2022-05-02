import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

from code.parser import Parser
from code.cpu import CPU
import time

class HiddenPrints:
    """Utility Class to prevent prints""" 

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


if __name__ == '__main__':
    """This test module is going to run -etl(transform_data), -tt(target_target_pair) and export options of the application. 
        It iterates trought each number of processors until the max CPU available measuring the time spend.
        From each CPU iteration it evaluates the code 3 times (3 laps) and calculate the mean time of them.
        At the end of the process you'll get a summary of the execution time spend based on the Number of CPUs used.
    """

    # Number of laps
    NUM_EVAL_LAPS = 3
    MAX_CPU_AVAILABLE = CPU.count_cpus()

    def evaluate(cpus):
        """Code o be evaluated each lap. -etl and -tt options are evaluated"""
        with HiddenPrints():
            parser = Parser("../data", cpus)
            parser.transform_data()
            parser.export_data("test_result.json")
            parser.target_target_pair()

    print("Warm up engine")
    evaluate(MAX_CPU_AVAILABLE)

    cpu_usage_times = []
    for cpus in range(1, MAX_CPU_AVAILABLE+1):
        print(f"CPUs in use: {cpus}")  
        cpu_laps_time = 0
        for lap in range(NUM_EVAL_LAPS):
            start = time.time()
            evaluate(cpus)
            end = time.time()
            diff = end - start
            print(f"    Lap number {lap+1} time: {round(diff, 3)}")
            cpu_laps_time += diff
        cpu_laps_time /= NUM_EVAL_LAPS
        cpu_usage_times.append((cpus, round(cpu_laps_time, 3)))

    delim = "\t"
    print(delim.join(i for i in ["Number of CPUs", "Execution time (s)" ]))
    for element in cpu_usage_times:
        print(delim.join(str(i) for i in element))
