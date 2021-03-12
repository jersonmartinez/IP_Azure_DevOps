# IP_Azure_DevOps
This script gets the IP addresses of the Azure DevOps regions as a JSON.

### Instalation

> $ pip install -r requirements.txt

### Usage

```bash
python ScriptIPAzureDevOps.py
```

### Implementation

```python
IPsAzureDevOps(
    'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519', 
    'JSON', 
    'AzureDevOps.WestEurope',
    '' #Filename JSON
).getData()
```