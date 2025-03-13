from django.core.exceptions import ValidationError
from django.db import models
from .user import TeamMember, TeamProfile

class Question(models.Model):
    """
    Model to store questions for the quiz.
    """
    
    title = models.CharField(max_length=300)
    number = models.IntegerField(unique=True, null=False, blank=False)
    description = models.TextField()

    samples = models.JSONField(null=True, blank=True) # The key is the sample input, the value is the ouput
    tests = models.JSONField(null=True, blank=True) # The key is the test input, the value is the output

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        samples = self.samples
        if samples is not None:
            if not isinstance(samples, dict):
                raise ValidationError("Samples must be a dictionary.")
            if len(samples) != 3:
                raise ValidationError("The number of sample inputs has to be 3.")
        if self.tests is not None:
            if not isinstance(self.tests, dict):
                raise ValidationError("Tests must be a dictionary.")
            if len(self.tests) != 4:
                raise ValidationError("The number of test inputs has to be 4.")
            
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['number']

class Answer(models.Model):
    """
    Model to store answer sent by participants.
    """
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_code = models.TextField()
    is_correct_answer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    time_submitted = models.DateTimeField(auto_now_add=True)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='answers')
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, related_name='answers')
    
    test_results = models.JSONField(null=True, blank=True) # The key is the test input, the value is the output

    def __str__(self):
        return f"{self.question.number} - {self.team_member.team.team_name} - {self.time_submitted}"