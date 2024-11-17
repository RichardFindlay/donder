from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from mountainsdir.models import mountain


most_pop_config = {	'scotland': ['munro', 'graham', 'corbett', 'marilyn', 'simm'], 
 					'england': ['wainwright', 'birkett', 'dodd', 'hewitt', 'marilyn', 'nuttall', 'simm'],
 					'ireland': ['vandeleur-Lynam', 'furth', 'hewitt', 'arderin', 'marilyn'],
 					'wales': ['hewitt', 'marilyn', 'nuttall', 'simm']
				}

# dynamic sitemaps
class MostPopularSitemap(Sitemap):
	changefreq = "weekly"
	priority = 1.0
	protocol = 'https'
     
	def items(self):

		# create urls for most popular configs
		most_pop_indexes = [f"/most-popular-{mountain_type}s-in-{country}?page={page_num}" for country, mountain_types in most_pop_config.items() for mountain_type in mountain_types for page_num in range(1, 100)]

		return most_pop_indexes
	
	def location(self, item):
		return item

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0
    protocol = 'https'
 
    def items(self):
        return ['home'] #returning static pages; home and contact us
 
    def location(self, item):
        return reverse(item) #returning the static pages URL; home and contact us

# static sitemaps
class IndexSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.8
	protocol = 'https'
    
	def items(self):     
		# number of mountains in directory
		mountain_items = 1000
		num_items_per_page = 6
        
		num_of_pages = int(mountain_items / num_items_per_page)

		index_pages = [f'/?page={x}' for x in range(2, num_of_pages)] # /?page=200

		return index_pages 
 
	def location(self, item):
		return item


