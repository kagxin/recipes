from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

class Artile(models.Model):

    title = models.CharField('标题', max_length=200, help_text='标题')
    subtitle = models.CharField('副标题', max_length=200)
    body = models.TextField('正文')
    create_time = models.DateTimeField('create_time', auto_now_add=True)

    class Meta:
        db_table = 'artile'
        verbose_name = u'artile'


class Commit(models.Model):

    title = models.CharField('title', max_length=200)
    text = models.TextField('text')
    atrtle = models.ForeignKey(Artile, related_name='commits', verbose_name='artile', help_text='artile', on_delete=models.CASCADE)
    create_time = models.DateTimeField('create_time', auto_now_add=True)

    class Meta:
        db_table = 'commit'
        verbose_name = 'commit'
