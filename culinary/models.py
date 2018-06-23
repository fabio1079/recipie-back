from enum import Enum

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class RecipeDifficultyChoices(Enum):
    EZ = "Easy"
    OK = "Ok"
    AV = "Average"
    HD = "Hard"
    MS = "Master Chief"


class Recipe(models.Model):
    user = models.ForeignKey(
        UserModel, related_name="recipes", on_delete=models.CASCADE)
    name = models.CharField(max_length=140, blank=False)
    time_needed = models.PositiveIntegerField(blank=False)
    picture = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.CharField(
        max_length=2,
        choices=[(tag.name, tag.value) for tag in RecipeDifficultyChoices],
        blank=False)

    def __str__(self):
        return self.name

    @staticmethod
    def validate_recipe_difficulty_choice(sender, instance, **kwargs):
        valid_difficulties = [tag.name for tag in RecipeDifficultyChoices]

        if instance.difficulty not in valid_difficulties:
            error = 'Recipe difficulty {} is not one of the permitted values: {}'  # noqa

            raise ValidationError(
                error.format(instance.difficulty, ', '.join(valid_difficulties))) # noqa


models.signals.pre_save.connect(
    Recipe.validate_recipe_difficulty_choice,
    sender=Recipe)


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="steps", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=False)
    picture = models.TextField(blank=True, null=True)


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="ingredients", on_delete=models.CASCADE)
    description = models.CharField(max_length=140, blank=False)
