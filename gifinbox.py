import os
import webapp2
import json
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):
        # open current json file
        with open("gifs.json") as json_file:
            json_data = json.load(json_file)
        # current array of gifs
        gifs = json_data["gifs"]
        labels = json_data["labels"]
        # zip into one array of objects for template
        lst = [{'gif': t[0], 'label': t[1]} for t in zip(gifs, labels)]
        # output
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {'lst': lst}))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)