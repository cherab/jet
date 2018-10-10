#!/bin/bash
jobname="sensitivities"
output="$(pwd)/${jobname}_stdout.log"
error="$(pwd)/${jobname}_stderr.log"
ncores=4
qsub -N "$jobname" -cwd -m ea -M "$USER" -o "$output" -e "$error" -pe smp "$ncores" -l mem_free=105G <<EOF
#!/bin/bash
module purge
module load standard python/3.5
python3 calculate_sensitivities.py
EOF
