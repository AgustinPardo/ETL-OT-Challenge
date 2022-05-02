# Create directories
data_dir=data
mkdir -p $data_dir/{evidence,targets,diseases}

# Get Data sets on background parallel
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/evidence --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/ -b -o $data_dir/evidence.log
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/targets --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/targets/ -b -o $data_dir/targets.log
wget --no-parent --level=1 --no-directories --directory-prefix=$data_dir/diseases --accept='*.json' -r ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/ -b -o $data_dir/diseases.log
