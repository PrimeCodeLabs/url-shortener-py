from locust import HttpUser, task, between
from random import choice
from faker import Faker

fake = Faker()

class URLShortenerUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user wait time between tasks

    @task
    def shorten_url(self):
        original_url = fake.url()
        self.client.post("/shorten", json={"original_url": original_url})

    @task
    def redirect_url(self):
        self.client.get("/6h61zg")  # Replace with a valid short URL from your service
