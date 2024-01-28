### A DNS Server

I am using python3.11

A SHITTY DNS Server which resolves the user dns query made using the standard library only.

**Note:** Avoid installing the packages listed in `requirements.txt`, as they are related to development (e.g., `pylint` and `mypy`).

### Usuage
1. Run the server with resolving server
```python
python src/main.py --resolver 8.8.8.8:53
```

2. Make a request to the server
```python
dig @127.0.0.1 -p 5353 google.com
```

**This SHIT is not for production but you can try it as you primary DNS server you just have to modify `src/main.py` to bind the connection to port `53` instead of `5353` and you are good to you**

I haven't checked this shit for multiple questions and stuff, maybe will do that later, but as of now it works like a charm.
