# Open Targets Software Developer Technical Test

## Prerequistes
Python 3.9.6
git
wget

#### wget instalation
Source info to installing wget:

Linux : https://www.tecmint.com/install-wget-in-linux/

Mac : https://www.maketecheasier.com/install-wget-mac/

# Follow the next steps to get the source code, download data sets, and the enviromvent ready to run the application.

## 1) Get source code

Clone source code. Execute:
```bash
git clone https://github.com/AgustinPardo/OT-ETL-Challenge
```

Go to repository folder. Execute:
```bash
cd OT-ETL-Challenge
```

## 2) Download data sets

### 2 options:

##### 1) Manually
Create directories. Execute:
```bash
data_dir=data
mkdir -p $data_dir/{evidence,targets,diseases}
```

Get data sets. Execute:
```bash
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/evidence --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/diseases --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/targets --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/targets/
```

##### 2) Using download_datases.sh script

Add permisions. Execute:
```bash
chmod 700 download_datases.sh
```

Run script. Execute:
```bash
./download_datases.sh
```

This script is going to create a folder labeled "data" to get evidence, target and disease datasets. The execution will be a background paralell process for each dataset. On "data" folder you'll find logs for each dataset. In the logs you can check if all the files were sucessfully downloaded and if execution was done/finished. This could take beetween 20 to 40 minutes depending on the internet speed.


To know if download datasets finish. On "data" folder execute:
```bash
grep -e "FINISHED" evidence.log targets.log diseases.log
```

Check for donwload errors. On "data" folder execute:
```bash
grep -e "error" -e "fail" evidence.log targets.log diseases.log | awk -F: '{print "Line "$1": "$2}'
```

## 3) Setting up environment
On "OT-ETL-Challenge" folder. Execute:

##### 1) Create virtual environment. Execute:
```bash
python -m venv etl
```
##### 2) Activate virtual environment. Execute:
```bash
source etl/bin/activate
```

##### 3) Install python dependencies. Execute:
```bash
pip install -r requirement.txt
```

## 4) Running application

##### Run main.py script

Usage options:
| Flag       | Description                                 | Default  |
|:-----------:|:-------------------------------------------:|:---------:|
| "-in"      | Data sets directory                          | "data" |
| "-out"     | Result JSON file output name                 | "result.json" |
| "-n"       | Numbers of CPUs used to parse data sets           | 1 |   
| "-nc"      | Get the number of CPUs available             |   |
| "-elt"     | Run ETL pipeline to get JSON file result     |   |
| "-tt"      | Count how many target-target pairs share a connection to at least two diseases |   |

Get the result JSON file using 8 CPUs. Execute:
```bash
python main.py -etl -n 8
```

Count how many target-target pairs share a connection to at least two diseases using 8 CPUs Execute:
```bash
python main.py -tt -n 8
```

Get how many CPUs are available on your execution environment. Execute:
```bash
python main.py -nc
```
