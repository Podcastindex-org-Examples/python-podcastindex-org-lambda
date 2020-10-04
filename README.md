Lambda wrapper around podcastindex.org APIs

You can run this via a Lambda or via `python lamda_function.py`

To use this implementation, make sure you create a `config.py` with your API implemenation

ex:

```python
api_key = 'YOUR API KEY HERE'
api_secret = 'YOUR API SECRET HERE'
```

To deploy this package to your lambda, run the `./package.sh` script and upload the resulting `function.zip`

