# Scale Models & Logical Clocks 

Victor Goncalves & Emeka Ezike

[Engineering Notebook](https://docs.google.com/document/d/1eg1a8mlqwVK3dF0FOg15WaMUkcBJ691Vb1yDbK8lv_g/edit?usp=sharing)



## Installation

1. Simply clone this repository
2. Make sure the latest version of python is installed
3. No other steps are required as this project only relies on default python libraries

## Usage

### Method 1:
Run three machines with random clock rates by runing the command `python app.py`.

### Method 2:
Conversely, you can run each machine in its own seperate terminal by running `python machine.py :id` where id is an integer value of 1, 2, or 3. Note that you will need to run three terminals with each terminal having its own unique id for this to be successful.

Regardless of the method, the machines with ids 1, 2, and 3 will run on ports 50050, 50051, and 50052 of localhost, respectively. Peer to peer connections are formed between the three machines. Then, messages will be send and received between in the spec by the definition of the assignment for 60 seconds. After that time, the machines all terminate.
