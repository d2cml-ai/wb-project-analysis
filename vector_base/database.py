import pandas as pd 
from .query_consult import Query


class DataConsult:
	def __init__(self, query, path_data = './data/projects_data.csv'):
		db_ = pd.read_csv(path_data)
		self.query = query
		data = query.data_context
		self.cross_data = self.cross_db(db_)
	def cross_db(self, db, columns = ['projectid', 'repnb', 'pdfurl', 'txturl', 'project_components']):
		data_context = self.query.data_context
		db = db[columns]
		db_cross = data_context.merge(db, on='pdfurl', how='left')
		db_cross = db_cross.drop(columns = ['content'])
		return db_corss[columns]
	