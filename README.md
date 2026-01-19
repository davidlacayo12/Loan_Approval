# Sample Model: Train, Test, Deploy, Serve

## Overview

This project provides a sample machine learning workflow that includes:

- Training a model  
- Testing the model  
- Deploying the model  
- Serving predictions via an API

It uses Python with a virtual environment for dependency management and includes utilities for setup, cleaning, and linting.

---

## Prerequisites

- Windows 11 environment  
- Python 3.8+ installed  
- PowerShell (for running scripts)  
- VS Code (recommended)  

---

## Setup

Before running any scripts or commands, make sure to allow script execution in PowerShell for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then, run the setup script to create a virtual environment and install all dependencies:

```powershell
.\utils\setup.ps1
```

## Training Dataset

[Loan Approval Dataset](https://www.kaggle.com/datasets/anishdevedward/loan-approval-dataset/data)

## Serving

Run either:
`python -m backend.app` or 

`serve-model` if you have run `pip install -e .`

and navigate to: http://127.0.0.1:8000/docs

## Frontend

```shell
cd frontend
npm install
npm run dev
```


## Putting it All Together

```shell
npm init -y
npm install --save-dev concurrently
npm install @headlessui/react @heroicons/react
```

There should be node-modules at the root/ and root/frontend/ folders. Then run:

```shell
npm run dev
```
