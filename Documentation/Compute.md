get ouput: sudo scp -r dschmitt@i11ssh.iti.kit.edu:~/david_master_thesis/workspace/qtm-weighted-evaluation/output /home/david/Documents/KIT/Masterarbeit/Workspace/remote_output

ssh dschmitt@i11ssh.iti.kit.edu
ssh compute12.iti.kit.edu

python3 -m venv eval-venv
pip install cython
pip install cmake
git submodule --init
pip install -e .

screen <evaluation_runner_bio.sh>
Ctrl-a d # detach (screen-Fenster verlassen; -> ausloggen)
screen -r # reattach (nach Wiedereinloggen Prozess beobachten)
Ctrl-a k # kill (angezeigten Prozess beenden)
? # Hilfebildschirm