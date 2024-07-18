from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta

from django.db.models import Q


# 01. Character Classes ----------------------------------------------------------------

class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


# 02. Chat App ----------------------------------------------------------------

class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)


class Message(models.Model):
    sender = models.ForeignKey(
        'UserProfile',
        related_name='sent_messages',
        on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        'UserProfile',
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self) -> None:
        self.is_read = True
        self.save()

    def reply_to_message(self, reply_content: str):
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )
        new_message.save()
        return new_message

    def forward_message(self, receiver: UserProfile):
        new_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )
        new_message.save()
        return new_message


# 03. Student Information ----------------------------------------------------------------
class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value) -> int:

        try:
            value = int(value)
        except ValueError:
            raise ValueError("Invalid input for student ID")

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        super().to_python(value)

        return value


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


# 04. Credit Card Masking ----------------------------------------------------------------
class MaskedCreditCardField(models.CharField):
    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")
        super().to_python(value)
        return f"****-****-****-{value[12:16]}"


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField(max_length=20)


# 05. Hotel Reservation System ----------------------------------------------------------------

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def reservation_period(self) -> int:
        reservation_period = self.end_date - self.start_date
        return reservation_period.days

    def calculate_total_cost(self):
        total_cost = self.room.price_per_night * self.reservation_period()
        return round(total_cost, 2)

    @property
    def is_available(self):
        reservation = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date
        )
        return not reservation.exists()

    def clean(self):

        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")


class RegularReservation(BaseReservation):

    def save(self, *args, **kwargs):
        super().clean()
        super().save(*args, **kwargs)
        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):

    def save(self, *args, **kwargs):
        super().clean()
        super().save(*args, **kwargs)
        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)

        if SpecialReservation.objects.filter(
            room=self.room,
            end_date__gte=self.end_date,
            start_date__lte=new_end_date
        ).exists():
            raise ValidationError(
                "Error during extending reservation"
            )

        self.end_date = new_end_date
        self.save()
        return f"Extended reservation for room {self.room.number} with {days} days"

