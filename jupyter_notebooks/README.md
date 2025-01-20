# Jupyter Notebooks for Amberdata Derivatives SDK

## Installation

Install your virtual environment, then you can install the Jupyter kernel for the virtual environment with this command:
```bash
python -m venv .venv
ipython kernel install --user --name=venv
```

To un-install it:
```
jupyter-kernelspec uninstall venv
```

## Notebooks

| Notebook                                         | Description                                   |
|--------------------------------------------------|-----------------------------------------------|
| [Implied Volatility](implied_volatility.ipynb)   | Various charts related to Implied Volatility  |
| [Open Interest](open_interest.ipynb)             | Various charts related to Open Interest       |
| [Options Flow](options_flow.ipynb)               | Various charts related to Options Flow        |
| [Realized Volatility](realized_volatility.ipynb) | Various charts related to Realized Volatility |
