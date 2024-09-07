# TimeLogger
*A command line time logging tool.*

[![Forks](https://img.shields.io/github/forks/rocketbro/TimeLogger)](https://github.com/rocketbro/TimeLogger/network/members) [![Contributors](https://img.shields.io/github/contributors/rocketbro/TimeLogger)](https://github.com/rocketbro/TimeLogger/graphs/contributors) [![Stars](https://img.shields.io/github/stars/rocketbro/TimeLogger)](https://github.com/rocketbro/TimeLogger/stargazers) [![Issues](https://img.shields.io/github/issues/rocketbro/TimeLogger)](https://github.com/rocketbro/TimeLogger/issues)
<br>
## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
<br>

## Description
TimeLogger is a command-line application designed for simple task tracking. It provides a minimalistic approach to logging tasks, avoiding the complexities of other task-tracking applications. I created TimeLogger to streamline my task logging process without distractions.

```
timelogger/
│
├── src/
│   └── timelogger/
│       ├── __init__.py
│       ├── main.py
│       ├── logger.py
│       ├── data_manager.py
│       └── utils.py
│
├── data/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── tests/
│   └── __init__.py
│
├── README.md
├── requirements.txt
└── setup.py
```

### Future Features
While TimeLogger is currently basic in functionality, future updates may include features such as task categorization, removing tasks from log file, and improved user interface. 
<br>

## Installation
To use TimeLogger, ensure you have the latest version of Python installed (version 3 and above) and follow these steps:

1. Clone the repository onto your local machine:  
`git clone https://github.com/rocketbro/TimeLogger.git`

2. Navigate into the directory where you cloned TimeLogger:
`cd <directory>`
<br>

## Usage
To use this package:

1. Navigate to the project root.
2. Run `pip install -e .` to install the package in editable mode.
3. Run the application using the `timelogger` command from anywhere in your system.