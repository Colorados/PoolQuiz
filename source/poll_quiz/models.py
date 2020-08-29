from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=50, null=False, blank=False, verbose_name='Вопрос')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return '{}. {}'.format(self.pk, self.question)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

class Choice(models.Model):
    option_txt = models.CharField(max_length=100, null=False, blank=False, verbose_name='Вариант ответа')
    poll = models.ForeignKey('poll_quiz.Poll', related_name='choices', on_delete=models.CASCADE, verbose_name='Опрос')

    def __str__(self):
        return '{}. {}'.format(self.pk, self.option_txt)

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'


