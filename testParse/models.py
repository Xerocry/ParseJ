from django.db import models
from datetime import datetime

# Create your models here.

# class AuthManager(models.Manager):
from django.db.models import QuerySet, Expression


# class Coalesce(Expression):
#     template = 'COALESCE( %(expressions)s )'
#
#     def __init__(self, expressions, output_field, **extra):
#         super(Coalesce, self).__init__(output_field=output_field)
#         if len(expressions) < 2:
#           raise ValueError('expressions must have at least 2 elements')
#         for expression in expressions:
#           if not hasattr(expression, 'resolve_expression'):
#               raise TypeError('%r is not an Expression' % expression)
#         self.expressions = expressions
#         self.extra = extra
#
#     def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False):
#         c = self.copy()
#         c.is_summary = summarize
#         for pos, expression in enumerate(self.expressions):
#             c.expressions[pos] = expression.resolve_expression(query, allow_joins, reuse, summarize)
#         return c
#
#     def as_sql(self, compiler, connection):
#         sql_expressions, sql_params = [], []
#         for expression in self.expressions:
#             sql, params = compiler.compile(expression)
#             sql_expressions.append(sql)
#             sql_params.extend(params)
#         self.extra['expressions'] = ','.join(sql_expressions)
#         return self.template % self.extra, sql_params
#
#     def as_oracle(self, compiler, connection):
#         """
#         Example of vendor specific handling (Oracle in this case).
#         Let's make the function name lowercase.
#         """
#         self.template = 'coalesce( %(expressions)s )'
#         return self.as_sql(compiler, connection)
#
#     def get_source_expressions(self):
#         return self.expressions
#
#     def set_source_expressions(self, expressions):
#         self.expressions = expressions




class Article(models.Model):
    ArticleSource = models.CharField(max_length=200, null=True)  # scopus - wos - spin
    sourceType = models.CharField(max_length=200, null=True)
    pubDate = models.DateField(default=datetime.now, blank=True, null=True)
    language = models.CharField(max_length=200, null=True)
    isbn = models.CharField(max_length=200, null=True)
    pages = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=500, null=True)
    # Meta and String


class IdKeyVal(models.Model):
    article = models.ForeignKey(Article, related_name='ids', db_index=True)
    key = models.CharField(max_length=240, db_index=True)
    value = models.CharField(max_length=240, db_index=True)


class Authors(models.Model):
    article = models.ManyToManyField(Article, related_name='authors')
    scopusId = models.BigIntegerField(null=True, default=True)
    spinId = models.CharField(max_length=200, null=True)
    researcherid = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s - %s" % (self.article, self.name)