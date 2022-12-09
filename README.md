<p align=center>
<a href="https://www.sap.com">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/SAP_2011_logo.svg/2560px-SAP_2011_logo.svg.png" alt="Logo" width="500" height="200">
</a>
</p>
<hr>
<h3 align="center">Pingdom checker is a small program that interacts with the Pingdom API.<br>
It is a task from my SAP interview and it can be used to add and remove checks from Pingdom<br>
and you can monitor the uptime status of websites through the database.
</h3>
<br><br><br>
<h3>To use it you need to create an account in Pingdom, generate an authentication token and put it in "main.py":</h3>

```python
    # SET API CONFIGURATION, PROVIDE YOUR OWN AUTHENTICATION TOKEN
    url = 'https://api.pingdom.com/api/3.1/checks'
    auth_token = 'put_your_auth_token_here'
```

<h3>The data is stored in sqlite3 database.</h3>
