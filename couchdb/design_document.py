from document import Document

class DesignDocument(Document):
	def __init__(self, database, doc_id, rev):
		super(DesignDocument, self).__init__(database, '_design/{0}'.format(doc_id), rev)

