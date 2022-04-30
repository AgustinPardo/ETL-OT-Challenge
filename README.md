# Open Targets Software Developer Technical Test

## Prerequistes
Python 3.9.6
git
wget

#### wget instalation
Source info to installing wget:
Linux : https://www.tecmint.com/install-wget-in-linux/
Mac : https://www.maketecheasier.com/install-wget-mac/

## Get source code

#### Clone source code
Execute:
```bash
git clone https://github.com/AgustinPardo/OT-ETL-Challenge
```

## Download data sets

Go to repository folder. Execute:
```bash
cd OT-ETL-Challenge
```

### 2 options:

#### 1) Manually
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

#### 2) Using bash script
Execute:
```bash
./donwload_datases.sh
```

This script is going to get evidence, target and disease data sets on parallel. You'll find logs for each datasource.

To know if donwload datasets finish. Execute:
```bash
grep -e "FINISHED"  evidence.log targets.log diseases.log
```

Check if donwload erros. Execute:
```bash
grep -e "error" -e "fail" evidence.log targets.log diseases.log | awk -F: '{print "Line "$1": "$2}'
```

## Setting up Environment
On OT-ETL-Challenge folder. Execute:

##### 1) Create virtual environment. Execute:
```bash
python3 -m venv etl
```
##### 2) Activate Virtual environment. Execute:
```bash
source etl/bin/activate
```

##### 3) Install python dependencies. Execute:
```bash
pip3 install -r requirement.txt
```