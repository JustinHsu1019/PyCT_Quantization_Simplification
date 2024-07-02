import time
from multiprocessing import Process
import argparse


parser = argparse.ArgumentParser(description='Run multi-process attack')
parser.add_argument('--model_name', type=str, default="transformer_fashion_mnist_two_mha", help='Name of the model')
parser.add_argument('--num_process', type=int, default=5, help='Number of processes')
parser.add_argument('--timeout', type=int, default=3600, help='Timeout in seconds')
parser.add_argument('--delta_factor', type=float, default=0.75, help='Delta factor')
parser.add_argument('--model_type', type=str, default="qnn", help='Type of the model use origin or qnn')
parser.add_argument('--first_n_img', type=int, default=5, help='Number of first images to process')
#"transformer_fashion_mnist_two_mha"
# transformer_fashion_mnist
args = parser.parse_args()
model_name = args.model_name
NUM_PROCESS = args.num_process
TIMEOUT = args.timeout
NORM_01 = False
delta_factor = args.delta_factor
model_type = args.model_type
first_n_img = args.first_n_img
if __name__ == "__main__":
    from utils.pyct_attack_exp import run_multi_attack_subprocess_wall_timeout
    from utils.pyct_attack_exp_research_question import (        
        stock_shap_1_2_3_4_8_limit_range02,imdb_shap_1_2_3_4_8_range02,imdb_transformer_shap_1_2_3_4_8_range02,fashion_mnist_transformer_shap
    )
    # inputs = pyct_lstm_stock_1_4_8_16_32_only_first_forward(model_name, first_n_img=502)
    # inputs = pyct_lstm_stock_1_2_3_4_8_limit_range02(model_name, first_n_img=502)
    # inputs = stock_shap_1_2_3_4_8_limit_range02(model_name, first_n_img=60)
    # inputs = imdb_transformer_shap_1_2_3_4_8_range02(model_name, first_n_img=5,model_type=model_type)
    inputs = fashion_mnist_transformer_shap(model_name, first_n_img=first_n_img,model_type=model_type,delta_factor=delta_factor)
    print("#"*40, f"number of inputs: {len(inputs)}", "#"*45)
    time.sleep(3)

    ########## 分派input給各個subprocesses ##########    
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
