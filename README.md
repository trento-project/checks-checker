# Wanda Checks Checker

A script to check [Wanda](https://github.com/trento-project/wanda) checks. 

Currently it only checks the URLs in the remediation section of the checks for validity: 
- Can the URL be retrieved
- If a fragment/anchor is used: does the anchor exist in the document

## Usage

Optional: Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

Make sure the required modules are available:
```
pip3 install -r requirements.txt
```

Call the `checks-checker` script with a filename or filenames of check files as parameters, e.g.

```
checks-checker ../wanda/priv/catalog/*.yaml
```
or
```
checks-checker DA114A.yaml 61451E.yaml 816815.yaml
```

The script returns an exit code of 1 if there were errors encountered


### Container Image

The container image can be used as follows:
```
docker run -it --rm -v "${PWD}":/checks ghcr.io/trento-project/checks-checker priv/catalog/*.yaml
```

Or alternatively, you can use environment variables to specify check files and parameters
```
docker run -it --rm -v "${PWD}":/checks -e CHECKFILES="priv/catalog/*.yaml" ghcr.io/trento-project/checks-checker 
```
