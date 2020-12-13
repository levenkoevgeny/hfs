from django.db import models
from social_profile.models import SocialProfile
from django.contrib.auth.models import User


class Chat(models.Model):
    PERSONAL = 1
    GROUP = 2

    TYPE_CHOICES = [
        (PERSONAL, 'Personal'),
        (GROUP, 'Group'),
    ]

    chat_name = models.CharField(max_length=255, verbose_name="Название чата")
    chat_type = models.IntegerField(verbose_name="Тип чата", choices=TYPE_CHOICES, default=PERSONAL)

    def __str__(self):
        return self.chat_name

    class Meta:
        ordering = ('chat_name',)
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class Message(models.Model):
    message_text = models.TextField(verbose_name="Текст сообщения")
    message_from = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, verbose_name="Сообщение от",
                                     related_name="Message_from")
    message_to = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, verbose_name="Сообщение к",
                                   related_name="Message_to")
    date_added = models.DateTimeField(verbose_name="Дата и время сообщения", auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="Название чата", blank=True, null=True)

    def __str__(self):
        return 'Сообщение - ' + self.message_text + ' от ' + self.message_from.last_name + ' к ' + \
               self.message_to.last_name + ' чат: ' + self.chat.chat_name

    @property
    def get_message_text(self):
        return self.message_text

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Clients(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    channels_name = models.TextField(verbose_name="Имя канала")

    def __str__(self):
        return self.channels_name

    class Meta:
        ordering = ('client',)
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'



