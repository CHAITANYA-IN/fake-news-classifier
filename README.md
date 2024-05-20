# Fake News DApp

## Prerequisites

- Python 3 should be installed on your system.
- matplotlib, numpy should be installed on your system

## Environment Setup

```sh
python3 -m venv p2p
source p2p/bin/activate
python3 -m pip install -r requirements.txt
```

## Command Syntax

The command to run the script follows this syntax:

## Running the Code

To run the Python script , use the following command :

```sh
python3 simulate.py [n_voters] [c1] [c2] [n]
```

Where:

- `[n_voters]` is number of voters.
- `[c1]` is fraction of honest voters trustworthy.
- `[c2]` is fraction of malicious voters.
- `[n]` is numbers of news to fact-check

## Usage

Replace the placeholders `[n_voters]`, `[c1]`, `[c2]`, and `[n]` with actual values as needed.

Example:

```sh
python3 simulate.py 100 0.9 0.1 1000
```

Here, simualation will create 100 voters with 90% of honest voters are trustworthy, 10% malicious.
It generates a graph representing Trustworthiness v/s Number of Users with respect to Trustworthiness.
