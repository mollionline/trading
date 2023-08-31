### Trading

### 1. Clone project    
    git clone

### 2. Create virtual environment for python
    python3 -m venv venv

### 3. Activate virtual environment    
    source venv/bin/activate (bash)
    .\venv\Scripts\activate (shell)

### 4. Install requirements    
    pip install -r requirements.txt

### 5. Now you can run app in local with venv
    uvicorn main:app --reload --workers 1 --port 8000 

### 6. Run pre-commit in local directory     
    pre-commit run 

### 7. Run project with docker-compose
    docker-compose up -d --build

### 8. API Docs with swagger go to
    localhost:8000/docs

### 9. Send request with data like 
    {
        "candlestick_intl_per_minutes": 120,
        "ema_interval": 21
    }

### 10. After send request with request body you will get response.csv file in uploads dir
    uploads/response.csv

### 11. For visualize data run
    python3 visualize.py