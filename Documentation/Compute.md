get ouput: scp -r dschmitt@i11ssh.iti.kit.edu:~/david_master_thesis/workspace/qtm-weighted-evaluation/output /home/david/Documents/KIT/Masterarbeit/Workspace/remote_output

ssh dschmitt@i11ssh.iti.kit.edu
ssh compute12.iti.kit.edu

python3 -m venv eval-venv
source eval-venv/bin/activate

pip install cython
pip install cmake
git submodule init
pip install -e .

screen bash evaluation_runner_bio.sh
Ctrl-a d # detach (screen-Fenster verlassen; -> ausloggen)
screen -r # reattach (nach Wiedereinloggen Prozess beobachten)
Ctrl-a k # kill (angezeigten Prozess beenden)
? # Hilfebildschirm

exact=""

python3 python_scripts/compare_to_exact.py ../../remote_output/output/QTM_bio/biological/sorted/biomatrix_minimum_sorted.csv ../bio_exact_solution/bio-solutions.csv