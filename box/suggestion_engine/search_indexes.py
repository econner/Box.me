import datetime
from haystack.indexes import *
from haystack import site
from suggestion_engine.models import Document

class DocumentIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    last_changed = DateTimeField(model_attr='last_changed')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Document.objects


site.register(Document, DocumentIndex)