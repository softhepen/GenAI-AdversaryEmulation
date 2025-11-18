#!/bin/bash
#SBATCH --job-name=rag_pipeline
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --output=logs/rag_pipeline_%j.out
#SBATCH --error=logs/rag_pipeline_%j.err

module load python/3.9.7
module load cuda/11.7
module load gcc/10.2.0

python -m venv $WORK/my_env_test
source $WORK/my_env_test/bin/activate

pip install --upgrade pip
pip install -r requirements.txt