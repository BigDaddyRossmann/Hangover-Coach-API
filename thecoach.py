from google.appengine.ext import ndb


class Cure(ndb.Model):
  """
  ' For Lookup
  """
  symptoms = ndb.StringProperty  (indexed=True, repeated=True)
  datetime = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
  
  """
  ' Cure Data
  """
  likes    = ndb.IntegerProperty (indexed=True)
  text     = ndb.TextProperty    (indexed=True)
  
  def getKey(self):
    return self.key.urlsafe()
  
  def toDict(self):
    return {
      'text': self.text,
      'likes': self.likes,
      'key': self.getKey()
    }


def addCure(text, symptoms):
  cure = Cure()
  
  cure.symptoms = symptoms
  cure.likes = 0
  cure.text = text
  
  cure.put()
  
  return cure.toDict()


def getCuresBySymptom(symptom, page=0, results_per_page=20):
  query = Cure.query(Cure.symptoms == symptom).order(-Cure.likes)
  cures = query.fetch(results_per_page, offset=results_per_page*page)
  return [cure.toDict() for cure in cures]

def getCures(symptoms=[], page=0, results_per_page=20):
  return dict((symptom, getCuresBySymptom(symptom, page=page, results_per_page=results_per_page)) for symptom in symptoms)


def likeCure(key):
  cure = ndb.Key(urlsafe=key).get()
  
  if cure == None:
    return False
  
  cure.likes += 1
  cure.put()
  
  return True