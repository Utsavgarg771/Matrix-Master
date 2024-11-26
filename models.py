from django.db import models

from django.contrib.auth.models import User

class MatrixHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matrix_input = models.TextField()  # Store the input matrix as text
    matrix_output = models.TextField()  # Store the output or solution
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of {self.user.username} at {self.created_at}"

# Create your models here.
