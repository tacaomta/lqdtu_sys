from django.db import models

class PublicationRaw(models.Model):
    title = models.TextField()
    year = models.IntegerField()
    source_title = models.TextField(null=True)
    cited_by = models.IntegerField(default=0)
    doi = models.CharField(max_length=255, null=True)
    authors = models.TextField()
    affiliations = models.TextField()
    abstract = models.TextField()
    author_keywords = models.TextField(null=True)
    index_keywords = models.TextField(null=True)
    publisher = models.TextField(null=True)
    document_type = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    citations = models.TextField()

    # 👇 QUAN TRỌNG
    raw_json = models.JSONField()   # lưu full record

    created_at = models.DateTimeField(auto_now_add=True)



class DimField(models.Model):
    name = models.CharField(max_length=255)

class FactPublication(models.Model):
    title = models.TextField()
    year = models.IntegerField()
    cited_by = models.IntegerField()

    first_author_lqd = models.BooleanField()
    corresponding_lqd = models.BooleanField()

    field = models.ForeignKey(DimField, on_delete=models.SET_NULL, null=True)

class DimCountry(models.Model):
    name = models.CharField(max_length=100)

class DimJournal(models.Model):
    name = models.CharField(max_length=200)

class DimUniversity(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(DimCountry, on_delete=models.SET_NULL, null=True)

class DimAuthor(models.Model):
    name = models.CharField(max_length=255)
    is_lqd = models.BooleanField(default=False)
    university = models.ForeignKey(DimUniversity, on_delete=models.SET_NULL, null=True)

class PublicationAuthor(models.Model):
    publication = models.ForeignKey(FactPublication, on_delete=models.CASCADE)
    author = models.ForeignKey(DimAuthor, on_delete=models.CASCADE)

    author_order = models.IntegerField()
    is_corresponding = models.BooleanField(default=False)


