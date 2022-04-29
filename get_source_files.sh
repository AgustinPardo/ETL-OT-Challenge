# Create directories
data_dir=data
mkdir -p $data_dir/{evidence,targets,diseases}

# Get Data sets on parallel
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/evidence --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/ -b
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/diseases --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/ -b
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/targets --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/targets/ -b

# Checking wget log for errors
grep -e "error" -e "fail" wget-log wget-log.1 wget-log.2 | awk -F: '{print "Line "$1": "$2}'

# Check donwload finish
grep -e "FINISHED"  wget-log wget-log.1 wget-log.2