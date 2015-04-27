from google.appengine.ext.webapp import template
import webapp2
import os

import thecoach


class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))


class APIHandler(webapp2.RequestHandler):
  def MissingParameter(self):
    return {
      'stat': 'fail',
      'error': 0,
      'message': 'Missing Parameter'
    }
  
  def UnknownMethod(self):
    return {
      'stat': 'fail',
      'error': 1,
      'message': 'Unknown Method'
    }
  
  def UnknownError(self, err):
    return {
      'stat': 'fail',
      'error': 2,
      'message': 'Unknown Error: %s' % str(err)
    }
  
  def Success(self, data={}):
    data['stat'] = 'ok'
    return data
  
  def Compile(self, data={}):
    from json import dumps
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(dumps(data))
  
  def get(self):
    method = self.request.get('method')
    
    if method == 'cures.add':
      text = str(self.request.get('text'))
      symptoms = str(self.request.get('symptoms')).split(',')
      
      if text == '' or symptoms == '':
        return self.Compile(self.MissingParameter())
      
      try:
        thecoach.addCure(text, symptoms)
        return self.Compile(self.Success())
      except BaseException as e:
        return self.Compile(self.UnknownError(e))
      
    elif method == 'cures.get':
      symptoms = str(self.request.get('symptoms')).split(',')
      page = int(self.request.get('page'))
      results_per_page = int(self.request.get('results_per_page'))
      
      if symptoms == '' or page == '' or results_per_page == '':
        return self.Compile(self.MissingParameter())
      
      try:
        results = thecoach.getCures(symptoms, page, results_per_page)
        return self.Compile(self.Success({
          'cures': results
        }))
      except BaseException as e:
        return self.Compile(self.UnknownError(e))
    
    elif method == 'cure.like':
      key = str(self.request.get('key'))
      
      if key == '':
        return self.Compile(self.MissingParameter())
      
      try:
        thecoach.likeCure(key)
        return self.Compile(self.Success())
      except BaseException as e:
        return self.Compile(self.UnknownError(e))
    
    else:
      return self.Compile(self.UnknownMethod())


app = webapp2.WSGIApplication([
                ('/api/?', APIHandler),
                ('/.*', MainHandler)
              ], debug=True)