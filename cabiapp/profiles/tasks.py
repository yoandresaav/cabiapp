from cabiapp.celery import app

@app.task
def prueba_suma(x, y):
    return x + y