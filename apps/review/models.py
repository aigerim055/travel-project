from django.db import models
from django.contrib.auth import get_user_model

from apps.business.models import Guide
from apps.tour.models import ConcreteTour



User = get_user_model()


RATING_CHOISES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )


class GuideRating(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    guide = models.ForeignKey(
        to=Guide,
        on_delete=models.CASCADE,
        related_name='rating_guide'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOISES)


class TourRating(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    tour = models.ForeignKey(
        to=ConcreteTour,
        on_delete=models.CASCADE,
        related_name='rating_tour'    
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOISES)


class TourComment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    tour = models.ForeignKey(
        to=ConcreteTour,
        on_delete=models.CASCADE,
        related_name='comment_tour'
    )
    image = models.ImageField(upload_to='media/comment_image', blank=True)
    comment = models.CharField(max_length=150)


class TourFavorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    tour = models.ForeignKey(
        to=ConcreteTour,
        on_delete=models.CASCADE,
        related_name='favorite_tour'
    )


class TourLike(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    tour = models.ForeignKey(
        to=ConcreteTour,
        on_delete=models.CASCADE,
        related_name='like_tour'
    )

    def __str__(self) -> str:
        return f'liked by {self.user.username}'