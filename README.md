# Crunchbase API
A full-featured API (application programming interface) library allowing downloading and presenting organization and people data from Crunchbase.  
## Quick Start
```
import cbapi

cbapi.set_key(<YOUR_RAPIDAPI_KEY>)
org = cbapi.get_org(name="Apple Inc.")
ppl = cbapi.get_org(name="Tim Cook")
```

## Installation
install `cbapi` using `pip`:
```
pip install git+https://github.com/Suri-Sun/cbapi.git
```

## Requirements
- pandas
- numpy
- requests

Feel free to drop any feedbacks you have.
