import argparse
from parser import Parser, CPU

def parse_arguments():
    """Command line arguments parser"""
    parser = argparse.ArgumentParser(description="ETL pipeline")
    parser.add_argument("-in", "--input_dir", default="data", help="Evidence, targets, diseases, data sets input directory")
    parser.add_argument("-out", "--output_file", default="result.json", help="Reuslt JSON file output name")
    parser.add_argument("-n", "--cpus_use", default=1, help="Numbers of CPUs used to parse data sets. Deaults is 1")
    parser.add_argument("-nc", action="store_true", help="Get the number of CPUs available")
    parser.add_argument("-etl", action="store_true", help="Run ETL pipeline to get JSON file result")
    parser.add_argument("-tt", action="store_true", help="Count how many target-target pairs share a connection to at least two diseases")
    return parser

def main():
    parser=parse_arguments()
    args=parser.parse_args()
    parser = Parser(args.input_dir, args.cpus_use)
    if args.nc:
        CPU.get_avaiable_cpus()
    if args.etl:
        parser.transform_data()
        parser.export_data(args.output_file)
    if args.tt:
        parser.target_target_pair()

if __name__ == "__main__":
    main()
