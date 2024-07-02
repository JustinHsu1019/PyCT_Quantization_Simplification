# PyCT


The main objective of PyCT is to produce as a minimum number of different input arguments to achieve as much coverage of the target function as possible by feeding the produced arguments one in an iteration. The currently supported input arguments can only be integers or strings. Other types of arguments may be supported in the future.


---


## Abstract


Concolic testing is a software testing technique for generating concrete inputs of programs to increase code coverage and has been developed for years. For programming languages such as C, JAVA, x86 binary code, and JavaScript, there are already plenty of available concolic testers. However, the concolic testers for Python are relatively less. Since Python is a popular programming language, we believe there is a strong need to develop a good one.


Among the existing testers for Python, PyExZ3 is the most well-known and advanced. However, we found some issues of PyExZ3: (1) it implements only a limited number of base types’ (e.g., integer, string) member functions and(2) it automatically downcasts concolic objects and discards related symbolic information as it encounters built-in types’ constructors.


Based on the concept of PyExZ3, we develop a new tool called PyCT to alleviate these two issues. PyCT supports a more complete set of member functions of data types including integer, string, and range. We also proposes a new method to upcast constants to concolic ones to prevent unnecessary downcasting. Our evaluation shows that with more member functions being supported, the coverage rate is raised to (80.20%) from (71.55%). It continues to go up to (85.68%) as constant upcasting is also implemented.


---


## Prerequisites


- [Python](https://www.python.org/downloads/) version == 3.8.5<br>
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
Type `$ git clone git@github.com:alan23273850/PyCT.git` or `$ git clone https://github.com/alan23273850/PyCT.git`<br>
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


## Quantization Testing
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

### Usage Example

```bash
python dnnct_transformer_multi.py --model_name transformer_fashion_mnist
 --num_process 5 --timeout 1000 --delta_factor 0.75 --model_type qnn --first_n_img 10
```

This command will:
- Use the "transformer_fashion_mnist" model
- Run 5 parallel processes
- Set a timeout of 1000 seconds
- Set the delta_factor to 0.75
- Use the Quantized Neural Network (QNNs) mode
- Process the first 10 images

## CNN Testing

To run CNN-specific testing with customizable parameters, use the following command:

```bash
python dnnct_cnn_multi.py [options]
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

## LSTM Testing

To run LSTM-specific testing with customizable parameters, use the following command:

```bash
python dnnct_rnn_multi.py [options]
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

## Transformer Testing

To run Transformer-specific testing with customizable parameters, use the following command:

```bash
python dnnct_transformer_multi.py [options]
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

- `--model_name`: Specifies the name of the Transformer model to test. The default is set to "transformer_fashion_mnist_two_mha", but you can also use other models like "transformer_fashion_mnist". Ensure this matches your saved model file name.
