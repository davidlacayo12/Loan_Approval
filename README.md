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

## Serving -> NEED TO UPDATE THIS

Run either:
`python -m src.sample_model` or `serve-model`
and navigate to: 
http://127.0.0.1:8000/docs
for development.

For Docker:
- Build: `docker build -t backend .`
- Run: `docker run -p 8000:8000 backend`
- Open: [http://localhost:8000/docs](http://localhost:8000/docs)

## Frontend

`cd loan-ui`
`npm install`
`npm run dev`


## Putting it All Together

```bash

npm init -y
npm install --save-dev concurrently
npm install @headlessui/react @heroicons/react
npm install recharts

```

There should be node-modules at the root/ and root/frontend/ folders. Then run:

`npm run dev`
