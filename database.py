from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)


def load_courses_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT course_name, course_code, language, aims, content, degree, ECTS, school, tests, block, lecturers FROM r_courses"))
    courses = []
    columns = result.keys()
    for row in result:
      result_dict = {column: value for column, value in zip(columns, row)}
      courses.append(result_dict)
    return courses


def load_carousel_courses_from_db(student_number):
  with engine.connect() as conn:
      query = text("""
          SELECT c.*, rf.rating 
          FROM r_courses c
          LEFT JOIN r_favorites4 rf
          ON c.course_code = rf.course_code AND rf.student_number = :student_number
      """)

      result = conn.execute(query, {"student_number": student_number})

      carousel_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          carousel_courses.append(result_dict)

      return carousel_courses







def add_test_to_db(request, student_number, course_code, favorite_value):
  with engine.connect() as conn:
      existing_record = conn.execute(
          text("SELECT * FROM r_favorites4 WHERE course_code = :course_code AND student_number = :student_number"),
          {"course_code": course_code, "student_number": student_number}
      ).fetchone()

      course_info_id = conn.execute(
          text("SELECT id FROM r_courses WHERE course_code = :course_code"),
          {"course_code": course_code}
      ).fetchone()

      if course_info_id:
          course_info_id = course_info_id[0]
      else:
          course_info_id = None

      print(f"Retrieved id for course_code={course_code}: id={course_info_id}")

      if existing_record:
          query = text("UPDATE r_favorites4 SET rating = :rating, id = :id WHERE course_code = :course_code AND student_number = :student_number")
      else:
          query = text("INSERT INTO r_favorites4 (course_code, student_number, rating, id) VALUES (:course_code, :student_number, :rating, :id)")

      conn.execute(query, {"course_code": course_code, "student_number": student_number, "rating": favorite_value, "id": course_info_id})


def load_favorite_courses_from_db(student_number):
    with engine.connect() as conn:
      query = text(""" 
          SELECT rf.*, c.course_code, c.course_name, c.content
          FROM r_courses c
          LEFT JOIN r_favorites4 rf
          ON c.course_code = rf.course_code AND rf.student_number =:student_number
          WHERE rf.rating = 'on' 
      """)

      result = conn.execute(query, {"student_number": student_number})

      favorite_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          favorite_courses.append(result_dict)
      return favorite_courses

def load_viewed_courses_from_db(student_number):
  with engine.connect() as conn:
      query = text("""
          SELECT r_courses.course_code, r_courses.course_name, r_courses.content
          FROM r_views
          INNER JOIN r_courses ON r_views.course_code = r_courses.course_code
          WHERE r_views.student_number = :student_number
      """)

      result = conn.execute(query, {"student_number": student_number})

      viewed_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          viewed_courses.append(result_dict)
      return viewed_courses

def load_ratings_and_details_for_viewed_courses(student_number):
  with engine.connect() as conn:
      query = text("""
          SELECT r_views.course_code, r_favorites4.rating, r_courses.course_name, r_courses.content
          FROM r_views
          LEFT JOIN r_favorites4 ON r_views.student_number = r_favorites4.student_number
                                  AND r_views.course_code = r_favorites4.course_code
          INNER JOIN r_courses ON r_views.course_code = r_courses.course_code
          WHERE r_views.student_number = :student_number
      """)

      result = conn.execute(query, {"student_number": student_number})

      ratings_and_details_for_viewed_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          ratings_and_details_for_viewed_courses.append(result_dict)
      return ratings_and_details_for_viewed_courses


def add_login_to_db(student_number, level, education):
  with engine.connect() as conn:
      conn.execute(
          text("INSERT INTO r_users (student_number, level, education) VALUES (:student_number, :level, :education)"),
          {"student_number": student_number, "level": level, "education": education}
      )


def add_interests_to_db(data):
  with engine.connect() as conn:
      query = text("INSERT INTO r_users (management, data, law, businesses, psychology, economics, statistics, finance, philosophy, sociology, entrepreneurship, marketing, accounting, econometrics, media, ethics, programming, health, society, technology, communication, history, culture, language, machine_learning, supply_chain, organizations, mathematics, sustainability, consumers, digital, governance, cognitive_science, artificial_intelligence, deep_learning, religion, globalization, behavior, theology, spirituality, criminality) "
                   "VALUES (:management, :data, :law, :businesses, :psychology, :economics, :statistics, :finance, :philosophy, :sociology, :entrepreneurship, :marketing, :accounting, :econometrics, :media, :ethics, :programming, :health, :society, :technology, :communication, :history, :culture, :language, :machine_learning, :supply_chain, :organizations, :mathematics, :sustainability, :consumers, :digital, :governance, :cognitive_science, :artificial_intelligence, :deep_learning, :religion, :globalization, :behavior, :theology, :spirituality, :criminality)")


      params = {
            'management': data.get('management'),
            'data':data.get('data'),
            'law': data.get('law'),
            'businesses': data.get('businesses'),
            'psychology': data.get('psychology'),
            'economics': data.get('economics'),
            'statistics': data.get('statistics'),
            'finance': data.get('finance'),
            'philosophy': data.get('philosophy'),
            'sociology': data.get('sociology'),
            'entrepreneurship': data.get('entrepreneurship'),
            'marketing': data.get('marketing'),
            'accounting': data.get('accounting'),
            'econometrics': data.get('econometrics'),
            'media': data.get('media'),
            'ethics': data.get('ethics'),
            'programming': data.get('programming'),
            'health': data.get('health'),
            'society': data.get('society'),
            'technology': data.get('technology'),
            'communication': data.get('communication'),
            'history': data.get('history'),
            'culture': data.get('culture'),
            'language': data.get('language'),
            'machine_learning': data.get('machine_learning'),
            'supply_chain': data.get('supply_chain'),
            'organizations': data.get('organizations'),
            'mathematics': data.get('mathematics'),
            'sustainability': data.get('sustainability'),
            'consumers': data.get('consumers'),
            'digital': data.get('digital'),
            'governance': data.get('governance'),
            'cognitive_science': data.get('cognitive_science'),
            'artificial_intelligence': data.get('artificial_intelligence'),
            'deep_learning': data.get('deep_learning'),
            'religion': data.get('religion'),
            'globalization': data.get('globalization'),
            'behavior': data.get('behavior'),
            'theology': data.get('theology'),
            'spirituality': data.get('spirituality'),
            'criminality': data.get('criminality')
                                        
        }


      conn.execute(query, params)


def update_interests(student_number, data):
  with engine.connect() as conn:
      query = text(
          "UPDATE r_users SET "
          "management = :management, "
          "data = :data, "
          "law = :law, "
          "businesses = :businesses, "
          "psychology = :psychology, "
          "economics = :economics, "
          "statistics = :statistics, "
          "finance = :finance, "
          "philosophy = :philosophy, "
          "sociology = :sociology, "
          "entrepreneurship = :entrepreneurship, "
          "marketing = :marketing, "
          "accounting = :accounting, "
          "econometrics = :econometrics, "
          "media = :media, "
          "ethics = :ethics, "
          "programming = :programming, "
          "health = :health, "
          "society = :society, "
          "technology = :technology, "
          "communication = :communication, "
          "history = :history, "
          "culture = :culture, "
          "language = :language, "
          "machine_learning = :machine_learning, "
          "supply_chain = :supply_chain, "
          "organizations = :organizations,"
          "mathematics = :mathematics, "
          "sustainability = :sustainability, "
          "consumers = :consumers, "
          "digital = :digital, "
          "governance = :governance, "
          "cognitive_science = :cognitive_science, "
          "artificial_intelligence = :artificial_intelligence, "
          "deep_learning = :deep_learning, "
          "religion = :religion, "
          "globalization = :globalization, "
          "behavior = :behavior, "
          "theology = :theology, "
          "spirituality = :spirituality, "
          "criminality = :criminality "
          "WHERE student_number = :student_number "
          )

      params = {
          'management': data.get('management'),
          'data':data.get('data'),
          'law': data.get('law'),
          'businesses': data.get('businesses'),
          'psychology': data.get('psychology'),
          'economics': data.get('economics'),
          'statistics': data.get('statistics'),
          'finance': data.get('finance'),
          'philosophy': data.get('philosophy'),
          'sociology': data.get('sociology'),
          'entrepreneurship': data.get('entrepreneurship'),
          'marketing': data.get('marketing'),
          'accounting': data.get('accounting'),
          'econometrics': data.get('econometrics'),
          'media': data.get('media'),
          'ethics': data.get('ethics'),
          'programming': data.get('programming'),
          'health': data.get('health'),
          'society': data.get('society'),
          'technology': data.get('technology'),
          'communication': data.get('communication'),
          'history': data.get('history'),
          'culture': data.get('culture'),
          'language': data.get('language'),
          'machine_learning': data.get('machine_learning'),
          'supply_chain': data.get('supply_chain'),
          'organizations': data.get('organizations'),
          'mathematics': data.get('mathematics'),
          'sustainability': data.get('sustainability'),
          'consumers': data.get('consumers'),
          'digital': data.get('digital'),
          'governance': data.get('governance'),
          'cognitive_science': data.get('cognitive_science'),
          'artificial_intelligence': data.get('artificial_intelligence'),
          'deep_learning': data.get('deep_learning'),
          'religion': data.get('religion'),
          'globalization': data.get('globalization'),
          'behavior': data.get('behavior'),
          'theology': data.get('theology'),
          'spirituality': data.get('spirituality'),
          'criminality': data.get('criminality'),
          'student_number': student_number
      }

      conn.execute(query, params)

def add_views_to_db(student_number, course_code, timestamp, id):
  with engine.connect() as conn:

      course_info_id = conn.execute(
          text("SELECT id FROM r_courses WHERE course_code = :course_code"),
          {"course_code": course_code}
      ).fetchone()

      if course_info_id:
          course_info_id = course_info_id[0]
      else:
          course_info_id = None


      existing_record = conn.execute(
          text("SELECT id FROM r_views WHERE student_number = :student_number AND id = :id"),
          {"student_number": student_number, "id": course_info_id}
      ).fetchone()

      if not existing_record:

          query = text("INSERT INTO r_views (course_code, student_number, timestamp, id) VALUES (:course_code, :student_number, :timestamp, :id)")
          conn.execute(query, {"course_code": course_code, "student_number": student_number, "timestamp": timestamp, "id": course_info_id})

def search_courses_from_db(query):
  with engine.connect() as conn:
      result = conn.execute(
               text("SELECT * FROM r_courses WHERE course_name LIKE :query OR course_code LIKE :query OR aims LIKE :query OR content LIKE :query"),
               {"query": "%" + query + "%"}
           )
      courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          courses.append(result_dict)
      return courses