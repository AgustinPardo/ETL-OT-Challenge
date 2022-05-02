import os
import argparse
from code.parser import Parser, CPU


def parse_arguments():
    """Command line arguments parser"""
    parser = argparse.ArgumentParser(description="ETL pipeline")
    parser.add_argument("-in", "--input_dir", default="data", help="Evidence, targets, diseases, data sets input directory. Optional argument default is 'data'")
    parser.add_argument("-out", "--output_file", default="result.json", help="Reuslt JSON file output name. Optional argument default name is 'resutl.json'")
    parser.add_argument("-n", "--cpus_use", default=1, help="Numbers of CPUs used to parse data sets. Optional argument deault is 1")
    parser.add_argument("-nc", action="store_true", help="Get the number of CPUs available")
    parser.add_argument("-etl", action="store_true", help="Run ETL pipeline to get JSON file result")
    parser.add_argument("-tt", action="store_true", help="Count how many target-target pairs share a connection to at least two diseases")
    return parser


def main():
    """Application manage function"""
    parser=parse_arguments()
    args=parser.parse_args()
    parser = Parser(args.input_dir, args.cpus_use)

    # Check if exist input directory
    if not(os.path.exists(args.input_dir)):
        raise FileNotFoundError(f'{args.input_dir} directory does not exists')

    # Check if exist evidence, targets, diseases directories
    data_directories = os.listdir(args.input_dir)
    for dir in ["evidence", "targets", "diseases"]:
        if dir not in data_directories:
            raise FileNotFoundError(f'{dir} directory does not exists')
    
    if args.nc:
        CPU.get_avaiable_cpus()
    if args.etl:
        parser.transform_data()
        parser.export_data(args.output_file)
    if args.tt:
        parser.target_target_pair()

if __name__ == "__main__":
    main()
