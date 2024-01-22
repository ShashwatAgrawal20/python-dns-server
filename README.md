### A DNS Server

I am using python3.11

### Usuage
1. Run the server
```python
python src/main.py
```

2. Make a request to the server
```python
dig @127.0.0.1 -p 5353 google.com +qid=69
```
