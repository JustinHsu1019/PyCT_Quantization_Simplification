import time
from multiprocessing import Process
import argparse
import ast

parser = argparse.ArgumentParser(description='Run multi-process attack')
parser.add_argument('--model_name', type=str, default="imdb_LSTM_08509", help='Name of the model')
parser.add_argument('--num_process', type=int, default=5, help='Number of processes')
parser.add_argument('--timeout', type=int, default=7200, help='Timeout in seconds')
parser.add_argument('--delta_factor', type=float, default=0.75, help='Delta factor')
parser.add_argument('--model_type', type=str, default="qnn", help='Type of the model use origin or qnn')
parser.add_argument('--first_n_img', type=int, default=1, help='Number of first images to process')
parser.add_argument('--ton_n_shap_list', type=str, default="[1,2,4,8,16,32]", help='List of top n shap values')


args = parser.parse_args()
model_name = args.model_name
NUM_PROCESS = args.num_process
TIMEOUT = args.timeout
NORM_01 = False
delta_factor = args.delta_factor
model_type = args.model_type
first_n_img = args.first_n_img
ton_n_shap_list = ast.literal_eval(args.ton_n_shap_list) 
if __name__ == "__main__":
    from utils.pyct_attack_exp import run_multi_attack_subprocess_wall_timeout
    from utils.pyct_attack_exp_research_question import (        
        stock_shap_1_2_3_4_8_limit_range02,imdb_shap_1_2_3_4_8_range02,imdb_transformer_shap_1_2_3_4_8_range02,mnist_lstm_1_2_3_4_8_range02,mnist_lstm_15_1_2_3_4_8_range02,sentiment_lstm_lstm_15_1_2_3_4_8_range02
    )
    # inputs = pyct_lstm_stock_1_4_8_16_32_only_first_forward(model_name, first_n_img=502)
    # inputs = pyct_lstm_stock_1_2_3_4_8_limit_range02(model_name, first_n_img=502)
    # inputs = stock_shap_1_2_3_4_8_limit_range02(model_name, first_n_img=60)
    inputs = imdb_shap_1_2_3_4_8_range02(model_name,ton_n_shap_list=ton_n_shap_list ,first_n_img=first_n_img,model_type=model_type,delta_factor=delta_factor)
    print("#"*40, f"number of inputs: {len(inputs)}", "#"*45)
    time.sleep(3)
    all_subprocess_tasks = [[] for _ in range(NUM_PROCESS)]
    cursor = 0
    for task in inputs:    
        all_subprocess_tasks[cursor].append(task)    
       
        cursor+=1
        if cursor == NUM_PROCESS:
            cursor = 0


    running_processes = []
    for sub_tasks in all_subprocess_tasks:
        if len(sub_tasks) > 0:
            p = Process(target=run_multi_attack_subprocess_wall_timeout, args=(sub_tasks, TIMEOUT, NORM_01,model_type,delta_factor))
            p.start()
            running_processes.append(p)
            time.sleep(1) # subprocess start 的間隔時間
       
    for p in running_processes:
        p.join()

    print('done')
