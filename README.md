# test_task__payment_service
This program was developed as a test task. It implements various payment methods on the site.
## Installation
1. Create venv `python3 -m venv env`
2. Its activate `source env/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Init db `flask db init`
5. First migrate `flask db migrate -m "Initial migration"`
6. Upgrade migration `flask db upgrade`
7. Create test data
```
flask shell
>>> from app.fake import currency
>>> currency()
```
And if you want to create test data on payments
```
>>> payments()
```