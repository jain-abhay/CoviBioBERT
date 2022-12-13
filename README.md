## Creating CoviBioBERT Model

#### Pretraining Process 

	1. Download BioBERT repo. from github.
	2. Download BioBERT weights place it in same folder  
	3. Download and preprocess covid-19 dataset with additional python script
	4. use create_pretraining script from BioBERT to create tf_example file
	5. use run_pretraining code to start pretraining process.

#### Fine tuning process

	1. Download and store datasets in the working biobert directory set respective paths.
	2. start finetuning
	3. detokenizing
	4. evaluate



#### Commands
------------------------------------------------------------

Command to run pretraining - 

1. Download covid-19 dataset and use create_shard script to create shards out of covid-19 dataset and save shards in shards folder.

2. Create pretraining data, This script is run for each data shard - 
python ./create_pretraining_data.py --input_file=./shards/input19.txt --output_file=./pretrained_output/tf_examples.tfrecord_19 --vocab_file=./vocab.txt --do_lower_case=False --max_seq_length=128 --max_predictions_per_seq=20 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=5


3. Run pretraining command  
!python /content/drive/MyDrive/EXPR_3/run_pretraining.py \
  --input_file=/content/pretrained_output/tf_examples.tfrecord* \
  --output_dir=/content/drive/MyDrive/EXPR_3/pretrained_model \
  --do_train=True \
  --do_eval=True \
  --bert_config_file=/content/drive/MyDrive/EXPR_3/bert_config.json \
  --init_checkpoint=/content/drive/MyDrive/EXPR_3/model.ckpt-1000000 \
  --train_batch_size=32 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=100000 \
  --num_warmup_steps=100 \
  --learning_rate=2e-5


---------------------------------------------
Commands for fine tuning, make sure to place all dataset files in the datasets folder -

1. Set Environment variables - 

 %env NER_DIR=/content/drive/MyDrive/fine_expr/datasets/NER/NCBI-disease

 %env OUTPUT_DIR=/content/drive/MyDrive/fine_expr/ner_outputs

2. Set tensorflow version - 
 
 %tensorflow_version 1.x

3. Start fine-tuning process
 
 !python /content/drive/MyDrive/fine_expr/run_ner.py \
  --do_train=true \
  --do_eval=true \
  --vocab_file=/content/drive/MyDrive/fine_expr/vocab.txt \
  --bert_config_file=/content/drive/MyDrive/fine_expr/bert_config.json \
  --init_checkpoint=/content/drive/MyDrive/fine_expr/pretraining_output/model.ckpt-10000 \
  --num_train_epochs=10.0 \
  --data_dir=$NER_DIR \
  --output_dir=$OUTPUT_DIR

4. Start detokenization process
  
  !python /content/drive/MyDrive/fine_expr/biocodes/ner_detokenize.py \
  --token_test_path=$OUTPUT_DIR/token_test.txt \
  --label_test_path=$OUTPUT_DIR/label_test.txt \
  --answer_path=$NER_DIR/test.tsv \
  --output_dir=$OUTPUT_DIR

5. Finally get F1 Score output
  
  !perl /content/drive/MyDrive/fine_expr/biocodes/conlleval.pl < $OUTPUT_DIR/NER_result_conll.txt
