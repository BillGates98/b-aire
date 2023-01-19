# Dependencies
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
python3.8 -m pip install tensorflow
# Verify install :
python3.8 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz
pip install numpy
pip install nltk
pip install enchant
pip install argparse
pip install pandas
pip ast

# 1. Building dictionary
cd ./base/
# import data file './base/dictionary/text_annotation.sql' in Mysql DBMS
# please configure the './config/config.json' file for the next
python3.8 ./analysis.py # show the analysis of the data

# 2.  Build NFRs
python3.8 ./textannotation.py # compute the NFRs vector
python3.8 ./acceptation.py # réalise une repartition statistique des données du dictionnaire par leurs  longueurs

#3. Build prediction model
cd ../machine_learning/
python3.8 ./main.py
# 3. Make recognition on entities : B-aire and SciSpacy
# - B-aire
cd ../b_aire/
python3.8 ./main.py
# - SciSpacy
cd ../spacy_annotation/
python3.8 ./main.py

# - Hunflair
# use this notebook available on colab because the Hunflair require CUDA environment :
# copy the data file located at ./outputs/data/data.json inside some folder in your 
# google drive and give its location inside the program and set the output to point inside the same directory even with the same name if you want*  
# https://colab.research.google.com/drive/15xXj7BWPW5MwoYo9nQVNN-tZ3Du27RIG?usp=sharing 

# Condition for evaluation
cd ../evaluation
python3.8 ./score_computation.py

cd ./visualization
python3.8 ./plot.py

cd ../../

echo "End of Running !"