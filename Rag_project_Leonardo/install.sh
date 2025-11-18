#!/bin/bash
#SBATCH --account=IscrC_GE-OS
#SBATCH --partition=boost_usr_prod
#SBATCH --time=04:00:00
#SBATCH --ntasks-per-node=1                  
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4                 
#SBATCH --gres=gpu:1
#SBATCH --mem=494000                        
#SBATCH --error=pipeline_err.log
#SBATCH --output=pipeline_output.log
#SBATCH --job-name=llama4-inference

module load python/3.9.7
module load cuda/11.7
module load gcc/10.2.0

python -m venv $WORK/my_env_test
source $WORK/my_env_test/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

srun ./main.py
