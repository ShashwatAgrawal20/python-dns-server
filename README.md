### A DNS Server

**Note:- The `requirements.txt` is empty as there are no external dependencies yet.**

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
