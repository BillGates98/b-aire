`The evaluations on bern2 took 57min on 633 documents and the results are in section Evaluation below`

# B-aire : Biological - Artificial Intelligence for Entities Recognition.
## Simplified version _1.0_ .

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Named entity recognition tool for biological domain.
- Carry out the installation of the various tools before any execution
- You can execute each part independently of the others


## Features : Available for Linux First

- You can modify your dictionary and restart the assessments as you wish
- You can train your own model on your data
- You have an implementation of Hunflair on google colab
- You already have an implementation of spacy in the project sources

> The next step concerns the installation and execution .

After installing and cloning the project, you need to move to the root, you can directly execute the following commands.

## Installations 
The installation prepares the environment in which the evaluations will take place without worries.

B-aire requires [Python(>=3.8) and pip](https://pip.pypa.io/en/stable/installation/#get-pip-py) to run.

## Installation

```sh
# Dependencies
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
python3 -m pip install tensorflow

pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz
pip install numpy
pip install nltk
pip install enchant
pip install argparse
pip install pandas
pip ast
```

Let's go : 

```sh
> 1. Building dictionary :
""" 
    Import data file './base/dictionary/text_annotation.sql' in Mysql DBMS
    Configure the './config/config.json' file for the next
"""
cd ./base/
python3 ./analysis.py # show the analysis of the data

> 2.  Build NFRs
python3 ./textannotation.py # compute the NFRs vector
python3 ./acceptation.py # performs a statistical distribution of the dictionary data by their lengths

> 3. Build prediction model
cd ../machine_learning/
python3 ./main.py

> 4. Run recognition on entities : B-aire and SciSpacy
# * B-aire
cd ../b_aire/
    # - genia
    python3 ./main.py --path '../gold_standard/data/' --extension '.txt' --source 'genia' --outputf '../outputs/data/data.json' 
    # - cineca 
    python3 ./main.py --path '../data/genia/biogenia-test/' --extension '.txt' --source 'cineca' --outputf '../outputs/data/data.json' 

# * SciSpacy
cd ../spacy_annotation/
python3 ./main.py

# * Hunflair
""" 
    use this notebook available on colab because the Hunflair require CUDA environment :
    copy the data file located at './outputs/data/data.json' inside some folder in your 
    google drive and give its location inside the program and set the output to point inside 
    the same directory even with the same name if you want.
    `_Google Colab_` :  https://colab.research.google.com/drive/15xXj7BWPW5MwoYo9nQVNN-tZ3Du27RIG?usp=sharing
 """

> 5. Additional
cd ../evaluation
python3 ./score_computation.py

cd ./visualization
python3 ./plot.py

cd ../../
echo "End of Running !"
```
## Evaluation between B-aire, Bern2, Hunflair, SciSpacy on Cineca Dataset of European Project

![Comparison between 4 tools on cineca](https://github.com/BillGates98/b-aire/blob/main/evaluation/visualization/global_fmeasure_comparing_cineca.png)

## License

MIT
**Free Software, Hell Yeah!**

