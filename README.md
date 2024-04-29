# amberdata-derivatives

amberdata-derivatives is a Python library to access the [Amberdata Derivatives API](https://docs.amberdata.io/reference/information).

---

**Documentation**: https://docs.amberdata.io/reference/information

---

## Install

```bash
pip install amberdata-derivatives
```

## Demo

```python
from amberdata_derivatives import Amberdata

amberdata_client = Amberdata(api_key="ENTER YOUR AD API KEY HERE")
amberdata_client.get_term_structure(currency='BTC', exchange='deribit')
```
