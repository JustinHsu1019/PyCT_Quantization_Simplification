# PyCT


The main objective of PyCT is to produce as a minimum number of different input arguments to achieve as much coverage of the target function as possible by feeding the produced arguments one in an iteration. The currently supported input arguments can only be integers or strings. Other types of arguments may be supported in the future.


---


## Abstract


Concolic testing is a software testing technique for generating concrete inputs of programs to increase code coverage and has been developed for years. For programming languages such as C, JAVA, x86 binary code, and JavaScript, there are already plenty of available concolic testers. However, the concolic testers for Python are relatively less. Since Python is a popular programming language, we believe there is a strong need to develop a good one.


Among the existing testers for Python, PyExZ3 is the most well-known and advanced. However, we found some issues of PyExZ3: (1) it implements only a limited number of base types’ (e.g., integer, string) member functions and(2) it automatically downcasts concolic objects and discards related symbolic information as it encounters built-in types’ constructors.


Based on the concept of PyExZ3, we develop a new tool called PyCT to alleviate these two issues. PyCT supports a more complete set of member functions of data types including integer, string, and range. We also proposes a new method to upcast constants to concolic ones to prevent unnecessary downcasting. Our evaluation shows that with more member functions being supported, the coverage rate is raised to (80.20%) from (71.55%). It continues to go up to (85.68%) as constant upcasting is also implemented.


---


## Prerequisites


- [Python](https://www.python.org/downloads/) version == 3.8.5<br>s
  Basically, it should also work for other versions not lower than 3.8. Simply follow the usual installation instructions for Python.<br>


- [CVC4](https://github.com/CVC4/CVC4) commit version == [d1f3225e26b9d64f065048885053392b10994e715](https://github.com/cvc5/cvc5/blob/d1f3225e26b9d64f065048885053392b10994e71/INSTALL.md)<br>
  Since our CVC4 version has to cope with that of the base project PyExZ3 when we compare the performance of the two, our designated version above cannot be the latest. Otherwise, the CVC4 Python API bindings used in PyExZ3 cannot work.<br>The installation instructions for CVC4 is almost the same as that in the provided link, except that the configuration command should be modified to `./configure.sh --language-bindings=python --python3` for the use of CVC4 Python API bindings. A user must ensure by himself/herself that the command `cvc4` can be found by an operating system shell. Otherwise the tool may not work.<br>


- [pipenv](https://pypi.org/project/pipenv/)<br>
  This is required for the use of the virtual environment mechanism in our project. Install it as a usual Python package.<br>


- additional settings<br>
  1. For CVC4 to be findable by the Python API, `export PYTHONPATH={path-to-CVC4-build-folder}/src/bindings/python` should be put in `~/.bashrc`.
  2. For pipenv to create a virtual environment in each project folder, `export PIPENV_VENV_IN_PROJECT=1` should be put in `~/.bashrc`, too.


---


## Installation


1. Clone our project to the local repository.<br>
Type `$ git clone https://github.com/PyCTsimplify/PyCT_Quantization_Simplification.gitt`<br>
2. Type `$ cd PyCT` and then `$ pipenv shell` for the first time to create a virtual environment.<br>
3. Type `$ pipenv install` to install required packages for this environment.
4. Type `$ exit` or `$ deactivate` to leave this virtual environment.
5. For case #46 of the integration test to work, one must repeat step 2. to 4. in the folder `./test/realworld/rpyc` for its own virtual environment first.


---


## Usage


Keep in mind that always type `$ pipenv shell` or `$ source .venv/bin/activate` in this project directory beforehand when starting an experiment, and always type `$ exit` or `$ deactivate` after the experiment finishes.


For example, to measure the target function `string_find(a, b)` in the target file `./test/strings/string_find.py`, and to let the two initial arguments be `a = ''` and `b = ''`, we can simply type the following command. A user can inspect all options of this script by typing `$ ./pyct.py -h`.
```
 $ ./pyct.py test.strings.string_find "{'a':'','b':''}" -r . -s string_find
```
or
```
 $ ./pyct.py test.strings.string_find "{'a':'','b':''}"
```
Then the output would be:
```
  ct.explore    INFO     Inputs: {'a': '', 'b': ''}
  ct.explore    INFO     Return: 1
  ct.explore    INFO     Not Covered Yet: /root/PyCT/test/strings/string_find.py [9]
  ct.explore    INFO     === Iterations: 1 ===
  ct.explore    INFO     Inputs: {'a': 'ggg', 'b': ''}
  ct.explore    INFO     Return: 1
  ct.explore    INFO     Not Covered Yet: /root/PyCT/test/strings/string_find.py [9]
  ct.explore    INFO     === Iterations: 2 ===
  ct.explore    INFO     Inputs: {'a': 'ADBECggg', 'b': ''}
  ct.explore    INFO     Return: 2
  ct.explore    INFO     Not Covered Yet: /root/PyCT/test/strings/string_find.py {}


Total iterations: 2
```


---


## Simplification Testing
```
./dnnct_wrapper.py dnn_example/cnn_simple.h5 dnn_example/img.in
```
To run DNN testing with customizable parameters, use the following command:
Available options:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--model_name` | Name of the model to test | `--model_name mnist_lstm_09785` |
| `--num_process` | Number of parallel processes | `--num_process 8` |
| `--timeout` | Timeout for each test in seconds | `--timeout 3600` |
| `--delta_factor` | Factor for adjusting test sensitivity |  `--delta_factor 0.75` |
| `--model_type` | Model type, either "origin" or "qnn" | `--model_type qnn` |
| `--first_n_img` | Number of images to process | `--first_n_img 10` |
| `--ton_n_shap_list` | List of top n SHAP values | `--ton_n_shap_list "[1,2,4,8,16,32]"` |

### Detailed Parameter Descriptions

- `--model_name`: Specifies the name of the deep learning model to test. This should correspond to your saved model file name.

- `--num_process`: Sets the number of parallel processes to run. Increasing this value can speed up testing but will also increase system resource usage.

- `--timeout`: Maximum runtime for each individual test. If a test exceeds this time, it will be terminated.

- `--delta_factor`: his parameter adjusts the sensitivity of the test. Lower values make the test more sensitive, potentially finding more edge cases but may increase false positives. Higher values do the opposite. **Important:** This parameter is only effective when `--model_type` is set to "qnn". For "origin" model type, this parameter has no effect.

- `--model_type`: This parameter specifies the type of model, which is particularly important for quantization testing:
  - "origin": Indicates the original floating-point model.
  - "qnn": Indicates a Quantized Neural Network. These models use integer or fixed-point arithmetic to reduce computational requirements.
  
  Choosing "qnn" activates specific quantization-related testing procedures, which may include checking quantization errors, testing quantization boundary conditions, etc.

- `--first_n_img`: Specifies the number of images to process. This is useful for limiting the scope of testing or for quick preliminary tests.

- `--ton_n_shap_list`: Specifies a list of top n SHAP values to consider. SHAP values help explain the output of machine learning models. This parameter allows you to specify different numbers of top SHAP values to analyze, which can be useful for understanding the most important features influencing the model's decisions at various levels of detail. 
### Usage Example

```bash
python dnnct_transformer_multi.py --model_name transformer_fashion_mnist
 --num_process 5 --timeout 1000 --delta_factor 0.75 --model_type qnn --first_n_img 10 --ton_n_shap_list [1,2,4,8]
```

This command will:
- Use the "transformer_fashion_mnist" model
- Run 5 parallel processes
- Set a timeout of 1000 seconds
- Set the delta_factor to 0.75
- Use the Quantized Neural Network (QNNs) mode
- Process the first 10 images
- Top SHAP values 1,2,4,8
## CNN Testing

To run CNN-specific testing with customizable parameters, use the following command:

```bash
python dnnct_cnn_multi.py --first_n_img` 100 --ton_n_shap_list [1,2,3,4,5,6,7,8]
```

### Available Options

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--model_name` | Name of the CNN model to test | "mnist_sep_act_m6_9628" | `--model_name custom_cnn_model` |
| `--num_process` | Number of parallel processes | 5 | `--num_process 8` |
| `--timeout` | Timeout for each test in seconds | 100 | `--timeout 300` |
| `--delta_factor` | Factor for adjusting test sensitivity | 0.75 | `--delta_factor 0.5` |
| `--model_type` | Model type, either "origin" or "qnn" | "qnn" | `--model_type origin` |
| `--first_n_img` | Number of images to process | 1 | `--first_n_img 10` |
| `--ton_n_shap_list` | List of top n SHAP values | [1,2,4,8]| `--ton_n_shap_list "[1,2,4,8]"` |

## LSTM Testing

To run LSTM-specific testing with customizable parameters, use the following command:

```bash
python dnnct_rnn_multi.py --first_n_img` 50 
```

### Available Options

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--model_name` | Name of the LSTM model to test | "imdb_LSTM_08509" | `--model_name custom_lstm_model` |
| `--num_process` | Number of parallel processes | 5 | `--num_process 8` |
| `--timeout` | Timeout for each test in seconds | 7200 | `--timeout 3600` |
| `--delta_factor` | Factor for adjusting test sensitivity | 0.75 | `--delta_factor 0.5` |
| `--model_type` | Model type, either "origin" or "qnn" | "qnn" | `--model_type origin` |
| `--first_n_img` | Number of sequences to process | 1 | `--first_n_img 10` |
| `--ton_n_shap_list` | List of top n SHAP values | [1,2,4,8,16,32]| `--ton_n_shap_list "[1,2,4,8,16,32]"` |
## Transformer Testing

To run Transformer-specific testing with customizable parameters, use the following command:

```bash
python dnnct_transformer_multi.py --first_n_img 100
```

### Available Options

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--model_name` | Name of the Transformer model to test | "transformer_fashion_mnist_two_mha" | `--model_name custom_transformer` |
| `--num_process` | Number of parallel processes | 5 | `--num_process 8` |
| `--timeout` | Timeout for each test in seconds | 3600 | `--timeout 7200` |
| `--delta_factor` | Factor for adjusting test sensitivity | 0.75 | `--delta_factor 0.5` |
| `--model_type` | Model type, either "origin" or "qnn" | "qnn" | `--model_type origin` |
| `--first_n_img` | Number of images/sequences to process | 5 | `--first_n_img 10` |
| `--ton_n_shap_list` | List of top n SHAP values | [1,2,4,8]| `--ton_n_shap_list "[1,2,4,8]"` |

- `--model_name`: Specifies the name of the Transformer model to test. The default is set to "transformer_fashion_mnist_two_mha", but you can also use other models like "transformer_fashion_mnist". Ensure this matches your saved model file name.

## Evaluation

We conducted preliminary evaluations on CNN and LSTM models to demonstrate the effectiveness of our ternary simplification approach in concolic testing.

### CNN Model Evaluation

```bash
python dnnct_cnn_multi.py  --model_name mnist_sep_act_m6_9628 --num_process 5 --timeout 100 --first_n_img 100 --ton_n_shap_list [1,2,3,4,5,6,7,8]
```

- Dataset: 100 MNIST images
- Pixels modified: Top 1-8 influential pixels (based on Deep SHAP)
- Timeout: 100 seconds per image
- Comparison: Original CNN vs. TNN_delta (threshold-based) vs. TNN_sign (sign-based)

Results for 2, 4, and 8 pixel modifications:

| Model     | Avg. Path Constraints | Resolved Constraints | Iteration Index | Test Inputs Generated |
|-----------|----------------------:|---------------------:|----------------:|----------------------:|
| TNN_delta | 1520.07 - 4222.27     | 143.14 - 789.01      | 1.13 - 12.55    | 19.97 - 34.88         |
| TNN_sign  | 938.96 - 1817.72      | 33.2 - 168.21        | 1.00 - 2.07     | 5.01 - 8.54           |
| CNN       | 799.3 - 1271.96       | 10.97 - 39.35        | 1.00 - 1.01     | 2.41 - 4.87           |

TNN_delta significantly outperformed both TNN_sign and the original CNN in all metrics, especially in complex scenarios with more pixels modified.


### LSTM Model Evaluation

```bash
python dnnct_rnn_multi.py  --model_name imdb_LSTM_08509 --num_process 5 --timeout 7200 --first_n_img 50 --ton_n_shap_list [1,2,4,8,16,32]
```

- Model: Adapted from TestRnn, featuring an LSTM layer followed by a dense layer for binary classification
- Dataset: IMDB (movie reviews for sentiment classification)
- Sequences modified: Top 1, 2, 4, 8, 16, and 32 highest SHAP values
- Timeout: 7200 seconds for unresolved cases
- Comparison: Original LSTM vs. LSTM_Δ∗ (ternary variant)
- Samples: 50

Results:

| Pixels | Model      | Generated Constraints | SAT Solutions | Timeout (s) | Solved Constraints | Iteration Index | Adversarial Inputs |
|--------|------------|----------------------:|---------------:|------------:|-------------------:|----------------:|-------------------:|
| 1      | LSTM       | 926.9                 | 6.03           | 6201.42     | 820.1              | 1.71            | 0                  |
|        | LSTM_Δ∗    | 272.39                | 0.59           | 85.83       | 272.39             | 2.27            | 0                  |
| 4      | LSTM       | 1072.3                | 1.13           | 7200        | 704.12             | 1               | 0                  |
|        | LSTM_Δ∗    | 7627.97               | 15.92          | 3023.12     | 5639.82            | 8.07            | 0                  |
| 32     | LSTM       | 1063.71               | 0              | 7200        | 0                  | 1               | 0                  |
|        | LSTM_Δ∗    | 10550                 | 1.12           | 6983.6      | 218.95             | 1               | 2                  |

LSTM_Δ∗ significantly outperformed the original LSTM, especially in:
- Generating more constraints and SAT solutions
- Reducing timeout rates (e.g., from 93% to 13% for single sequence data points)
- Producing adversarial inputs for complex cases (16 and 32 pixels)

### Transformer Model Evaluation

```bash
python dnnct_transformer_multi.py  --model_name transformer_fashion_mnist --num_process 5 --timeout 1000 --first_n_img 100 --ton_n_shap_list [1,2,4,8]
```

- Architecture: Single layer of MultiHeadAttention followed by a Dense layer
- Dataset: MNIST
- Pixels modified: Top 1, 2, 4, and 8 highest SHAP values
- Timeout: 1000 seconds for unresolved cases
- Comparison: Original Transformer vs. Transformer_Δ∗
- Samples: 100

Results:

| Pixels | Model           | Generated Constraints | SAT Solutions | Timeout (s) | Solved Constraints | Iteration Index | Adversarial Inputs |
|--------|-----------------|----------------------:|---------------:|------------:|-------------------:|----------------:|-------------------:|
| 1      | Transformer     | 6779.02               | 10.26          | 443.61      | 391.96             | 1.43            | 81                 |
|        | Transformer_Δ∗  | 6268.29               | 8.68           | 440.52      | 448.88             | 1.55            | 74                 |
| 8      | Transformer     | 1581.3                | 0.24           | 1053.27     | 1.76               | 1               | 1                  |
|        | Transformer_Δ∗  | 2990.63               | 0.53           | 1009.18     | 2.37               | 1               | 14                 |

Transformer_Δ∗ showed improvements over the original Transformer, particularly in:
- Generating more SAT solutions for complex cases (4 and 8 pixels)
- Producing more adversarial inputs, especially for higher pixel counts

### Enhanced Sparsification Strategy 

We evaluated different sparsification levels on both LSTM and Transformer models to assess the effectiveness of our ternary simplification approach in enhancing concolic testing capabilities.

#### LSTM Model

We tested the following sparsification levels: 2/3Δ∗, Δ∗, 2Δ∗, 3Δ∗, 4Δ∗

```bash
python dnnct_rnn_multi.py  --model_name imdb_LSTM_08509 --num_process 5 --timeout 7200 --delta_factor  0.5 or 0.75 or 1.5 or 2.25 or 3 --first_n_img 10 --ton_n_shap_list [1,2,4,8,16,32]
```

- Samples: 10
- Sequences modified: Top 1, 2, 4, 8, 16, and 32 highest SHAP values
- Timeout: 7200 seconds
- --delta_factor = 0.5, 0.75, 1.5, 2.25, 3

Key findings:
- Lower Δ∗ values (e.g., 2/3Δ∗) led to more timeouts for high pixel counts
- Medium values (2Δ∗, 3Δ∗) balanced computational efficiency and constraint-solving capability
- High values (4Δ∗) resulted in over-simplification, reducing the model's effectiveness in generating adversarial examples

Optimal pruning intensity for LSTM was found to be between Δ∗ and 3Δ∗, providing a good balance between computational efficiency and the ability to handle complex data in adversarial settings.

#### Transformer Model

We tested the following sparsification levels: Original Transformer, Δ∗, 2Δ∗, 3Δ∗

```bash
python dnnct_transformer_multi.py  --model_name transformer_fashion_mnist_two_mha --num_process 5 --timeout 3600 --delta_factor  0.75 or 1.5 or 2.25 --first_n_img 20 --ton_n_shap_list [1,2,4,8]
```
- Samples: 20
- Sequences modified: Top 1, 2, 4, and 8 highest SHAP values
- Timeout: 3600 seconds
- --delta_factor = 0.75, 1.5, 2.25

Key findings:
- Original Transformer had high timeout rates, especially for high pixel counts
- Δ∗ reduced timeout rates significantly
- 2Δ∗ provided optimal balance, eliminating timeouts for low pixel counts while maintaining adversarial output capability
- 3Δ∗ showed signs of over-simplification, rendering the model ineffective in producing adversarial examples

Optimal pruning intensity for Transformer was found to be between Δ∗ and 2Δ∗, effectively preventing computational timeouts in high-pixel scenarios while maintaining the capability to process complex data.

These results demonstrate that our ternary simplification approach effectively enhances the capability of concolic testing on both LSTM and Transformer architectures, allowing for more efficient exploration of execution paths and generation of adversarial inputs. The optimal pruning intensity varies between model types, emphasizing the importance of tailored simplification strategies for different neural network architectures.




