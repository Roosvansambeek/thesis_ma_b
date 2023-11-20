


from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine, Column, String
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sqlalchemy import create_engine, text



db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)



Base = declarative_base()

class Cinfo(Base):
  __tablename__ = 'r_courses'  

  content = Column(String, primary_key=True)
  course_code = Column(String, primary_key=True)
  course_name = Column(String, primary_key=True)
  degree= Column(String, primary_key=True)

Session = sessionmaker(bind=engine)
session = Session() 

# Fetch data from the r_views table
course_contents = session.query(Cinfo.content, Cinfo.course_code, Cinfo.course_name, Cinfo.degree).all()

course_contents_df = pd.DataFrame(course_contents, columns=['course_content', 'course_code', 'course_title', 'degree'])


# Create indices
indices = pd.Series(course_contents_df.index, index=course_contents_df['course_code']).drop_duplicates()


course_contents = [row[0] for row in course_contents]
count_vectorizer = CountVectorizer(stop_words='english')
course_content_matrix = count_vectorizer.fit_transform(course_contents)


session.close()

def get_course_recommendations_int_BOW(student_number):

  Base = declarative_base()

  class Cint(Base):
      __tablename__ = 'r_users'  

      student_number = Column(String, primary_key=True)
      management = Column(String)
      data = Column(String)
      law = Column(String)
      businesses = Column(String)
      psychology = Column(String)
      economics = Column(String)
      statistics = Column(String)
      finance = Column(String)
      philosophy = Column(String)
      sociology = Column(String)
      entrepreneurship = Column(String)
      marketing = Column(String)
      accounting = Column(String)
      econometrics = Column(String)
      media = Column(String)
      ethics = Column(String)
      programming = Column(String)
      health = Column(String)
      society = Column(String)
      technology = Column(String)
      communication = Column(String)
      history = Column(String)
      culture = Column(String)
      language = Column(String)
      machine_learning = Column(String)
      supply_chain = Column(String)
      organizations = Column(String)
      mathematics = Column(String)
      sustainability = Column(String)
      consumers = Column(String)
      digital = Column(String)
      governance = Column(String)
      cognitive_science = Column(String)
      artificial_intelligence = Column(String)
      deep_learning = Column(String)
      religion = Column(String)
      globalization = Column(String)
      behavior = Column(String)
      theology = Column(String)
      spirituality = Column(String)
      criminality = Column(String)

  Session = sessionmaker(bind=engine)
  session = Session()

  

  # Fetch data from the r_users table
  course_interests = session.query(Cint.student_number, Cint.management, Cint.data, Cint.law, Cint.businesses, Cint.psychology, Cint.economics, Cint.statistics, Cint.finance, Cint.philosophy, Cint.sociology, Cint.entrepreneurship, Cint.marketing, Cint.accounting, Cint.econometrics, Cint.media, Cint.ethics, Cint.programming, Cint.health, Cint.society, Cint.technology, Cint.communication, Cint.history, Cint.culture, Cint.language, Cint.machine_learning, Cint.supply_chain, Cint.organizations, Cint.mathematics, Cint.sustainability, Cint.consumers, Cint.digital, Cint.governance, Cint.cognitive_science, Cint.artificial_intelligence, Cint.deep_learning, Cint.religion, Cint.globalization, Cint.behavior, Cint.theology, Cint.spirituality, Cint.criminality).all()

  session.close()

  user_interests_list = [
      {'student_number': student_number, 'user_interests': {'management': 1 if management == 'on' else 0, 'data': 1 if data == 'on' else 0, 'law': 1 if law == 'on' else 0, 'businesses': 1 if businesses == 'on' else 0, 'psychology': 1 if psychology == 'on' else 0, 'economics': 1 if economics == 'on' else 0, 'statistics': 1 if statistics == 'on' else 0, 'finance': 1 if finance == 'on' else 0, 'philosophy': 1 if philosophy == 'on' else 0, 'sociology': 1 if sociology == 'on' else 0, 'entrepreneurship': 1 if entrepreneurship == 'on' else 0, 'marketing': 1 if marketing == 'on' else 0, 'accounting': 1 if accounting == 'on' else 0, 'econometrics': 1 if econometrics == 'on' else 0, 'media': 1 if media == 'on' else 0, 'ethics': 1 if ethics == 'on' else 0, 'programming': 1 if programming == 'on' else 0, 'health': 1 if health == 'on' else 0, 'society': 1 if society == 'on' else 0, 'technology': 1 if technology == 'on' else 0, 'communication': 1 if communication == 'on' else 0, 'history': 1 if history == 'on' else 0, 'culture': 1 if culture == 'on' else 0, 'language': 1 if language == 'on' else 0, 'machine_learning': 1 if machine_learning == 'on' else 0, 'supply_chain': 1 if supply_chain == 'on' else 0, 'organizations': 1 if organizations == 'on' else 0, 'mathematics': 1 if mathematics == 'on' else 0, 'sustainability': 1 if sustainability == 'on' else 0, 'consumers': 1 if consumers == 'on' else 0, 'digital': 1 if digital == 'on' else 0, 'governance': 1 if governance == 'on' else 0, 'cognitive_science': 1 if cognitive_science == 'on' else 0, 'artificial_intelligence': 1 if artificial_intelligence == 'on' else 0, 'deep_learning': 1 if deep_learning == 'on' else 0, 'religion': 1 if religion == 'on' else 0, 'globalization': 1 if globalization == 'on' else 0, 'behavior': 1 if behavior == 'on' else 0, 'theology': 1 if theology == 'on' else 0, 'spirituality': 1 if spirituality == 'on' else 0, 'criminality': 1 if criminality == 'on' else 0}} 
      for student_number, management, data, law, businesses, psychology, economics, statistics, finance, philosophy, sociology, entrepreneurship, marketing, accounting, econometrics, media, ethics, programming, health, society, technology, communication, history, culture, language, machine_learning, supply_chain, organizations, mathematics, sustainability, consumers, digital, governance, cognitive_science, artificial_intelligence, deep_learning, religion, globalization, behavior, theology, spirituality, criminality in course_interests
  ]


  user_interest_vector = None

  # Find the user_interest_vector for the specified student_number
  for user_interest in user_interests_list:
    interests = user_interest['user_interests']

    # Split multi-word interests into individual words and assign value 1
    interests_with_single_words = {}
    for interest, value in interests.items():
        if '_' in interest:
            words = interest.split('_')
            for word in words:
                interests_with_single_words[word] = value
        else:
            interests_with_single_words[interest] = value

    user_interest_vector = [interests_with_single_words.get(interest, 0) for interest in count_vectorizer.get_feature_names_out()]

    similarities = cosine_similarity([user_interest_vector], course_content_matrix)

    # Rest of your code remains the same
    # ...


    course_indices = similarities.argsort()[0][::-1]


    top_n = 50
    recommended_courses = course_contents_df.iloc[course_indices[:top_n]]


    student_recommendations = {
        "student_number": student_number,
        "recommended_courses": [
            {
                "course_code": course["course_code"],
                "course_content": course["course_content"],
                "course_title": course["course_title"],
                "degree": course["degree"],
                "similarity_score": similarities[0, index]
            }
            for index, course in recommended_courses.iterrows()
        ]
    }


   
  return student_recommendations




def get_ratings_from_database(student_number):
  with engine.connect() as conn:
      query = text("SELECT course_code, rating FROM r_favorites4 WHERE student_number = :student_number")
      result = conn.execute(query, {"student_number": student_number})

     
      ratings = {row.course_code: row.rating for row in result}
  return ratings



def get_degree_from_database(student_number):
  with engine.connect() as conn:
      query = text("SELECT level FROM r_users WHERE student_number = :student_number")
      result = conn.execute(query, {"student_number": student_number})

      
      levels = [row.level for row in result]

  return levels



def get_recommendations_with_ratings_BOW(student_number):
  recommendations = get_course_recommendations_int_BOW(student_number) 
  rated_courses = get_ratings_from_database(student_number) 

  for recommendation_set in recommendations['recommended_courses']:
      course_code = recommendation_set['course_code']
      if course_code in rated_courses:
          recommendation_set['rating'] = rated_courses[course_code]
          print(f"Course {course_code} is marked as {rated_courses[course_code]}")
      else:
          recommendation_set['rating'] = 'off'

  return recommendations



def get_recommendations_level_BOW(student_number):
  recommendations = get_recommendations_with_ratings_BOW(student_number)
  degree = get_degree_from_database(student_number)


  student_degree = degree[0] if degree else None

  if student_degree:

      filtered_recommendations = {
          "student_number": student_number,
          "recommended_courses": [
              recommendation_set for recommendation_set in recommendations['recommended_courses']
              if recommendation_set['degree'].lower() == student_degree.lower()
          ]
      }
      return filtered_recommendations
  else:
      return {"student_number": student_number, "recommended_courses": []}






