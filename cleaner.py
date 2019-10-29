import os
import random
import math

from bs4 import BeautifulSoup


"""
	Converts duarouter route files to trip files.
	Content:
	- Read duarouter xml route files
	- Creates shuffled lists of routes
	- Saves it as trips
"""
class Cleaner:


	"""
		Init method to configure parameters
		Please edit it
	"""
	def __init__(self):
		
		# Path to the duarouter files
		self.path = 'duaroutertrips/'

		# Output trips quantity
		self.quantity = 2300

		# Quantity of distinct files
		self.file_quantity = 20

		# Depart interval
		self.depart_interval = 1

		# Prename of the file
		self.pre_name = 'chicago'


	"""
		Read a single xml file
	"""
	def read_files(self, file):

		f = open('{0}/{1}'.format(self.path, file))

		data = f.read()
		soup = BeautifulSoup(data, "xml")

		f.close()

		return soup


	"""
		List all files from a folder
	"""
	def read_folder(self):

		files = {}

		for file in os.listdir(self.path):
			files[file] = self.read_files(file)

		return files


	"""
		Get only the attributes needed
	"""
	def get_attributes(self, routes):

		route_coords = []

		# Travel through attributes
		for route in routes.findAll('vehicle'):

			coords = route.find('route')
			coords_list = coords['edges'].split(' ')
			map(str, coords_list)
			
			# Arrived
			route_coords.append((coords_list[0], coords_list[-1]))
			
		return route_coords

	"""
		Filter every route getting only the start and the end
	"""
	def filter_routes(self, files):

		filtered_routes = {}

		for day in files:
			filtered_routes[day] = self.get_attributes(files[day])

		return filtered_routes


	"""
		Obtain a determined quantity of the routes shuffled
		This follows the division into 3 subgroups, and then shuffle
		each subgroup
	"""
	def shuffle_and_choose(self, filtered):
		
		shuffled = {}

		for day in filtered:

			route_quantity = len(filtered[day])
			group_size = math.floor(route_quantity // 3)
			group_quantity = math.floor(self.quantity // 3)

			chosen = []

			for i in range(3):
				choice = random.choices(filtered[day][i*group_size:group_size*(i+1)], k=group_quantity)
				chosen.extend(choice)

			shuffled[day] = chosen

		return shuffled

	"""
		Create every trip file
	"""
	def trip_street(self, output, i):
		
		if not os.path.exists('trips'):
			os.makedirs('trips')

		for day in output:

			file_name = day.split('.')[0]

			if not os.path.exists('trips/' + file_name):
				os.makedirs('trips/' + file_name)

			f = open('trips/{0}/{1}_{2}.trips.xml'.format(file_name, self.pre_name, i), "w")
			
			f.write('<?xml version="1.0"?>\n')
			f.write('<trips>\n')

			depart = 0

			for indx, trip in enumerate(output[day]):

				if indx % self.depart_interval == 0:
					depart += 1
				
				f.write('<trip id="{0}" depart="{1}" from="{2}" to="{3}" />\n'.format(indx, depart, trip[0], trip[1]))

			f.write('</trips>')

			f.close()


	"""
		Main function that calls everything else
	"""
	def main(self):

		print('Lets read it first')
		files = self.read_folder()
	
		print('It is getting filtered')	
		filtered = self.filter_routes(files)

		for i in range(self.file_quantity):

			print('Lets change the order a little bit')
			to_the_streets = self.shuffle_and_choose(filtered)

			print('Done, out with it')
			self.trip_street(to_the_streets, i)



if __name__ == '__main__':
	cleaner = Cleaner()
	cleaner.main()