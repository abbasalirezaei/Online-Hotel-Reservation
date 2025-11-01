from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_home(self):
        self.client.get("/")