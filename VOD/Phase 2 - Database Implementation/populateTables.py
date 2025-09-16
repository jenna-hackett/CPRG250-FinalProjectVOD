import psycopg2
from faker import Faker
import random
import re
from datetime import datetime, timedelta
 
fake = Faker()
 
def execute_many(sql, data, db_config):
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        with conn.cursor() as cur:
            cur.executemany(sql, data)
        conn.commit()
    except Exception as e:
        print(f"Error executing batch insert: {e}")
    finally:
        if conn:
            conn.close()
 
def generate_postal_code():
    # Canadian postal code format: A1A1A1
    letters = 'ABCEGHJKLMNPRSTVXY'
    while True:
        pc = f"{random.choice(letters)}{random.randint(0,9)}{random.choice(letters)}{random.randint(0,9)}{random.choice(letters)}{random.randint(0,9)}"
        if re.match(r'^[A-Z][0-9][A-Z][0-9][A-Z][0-9]$', pc):
            return pc
 
def generate_phone():
    return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
 
def populate_categories(db_config):
    categories = [
        'Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Animation', 'Romance', 'Documentary',
        'Thriller', 'Fantasy', 'Mystery', 'Crime', 'Adventure', 'Family', 'Biography',
        'Musical', 'War', 'History', 'Western', 'Sport', 'Short', 'Film-Noir',
        'Talk-Show', 'News', 'Reality-TV', 'Game-Show', 'Music', 'Stand-Up', 
        'Concert', 'Kids'
    ]
    sql = "INSERT INTO categories (category_name) VALUES (%s)"
    data = [(c,) for c in categories]
    execute_many(sql, data, db_config)
    print("Inserted categories")
 
def populate_advisories(db_config):
    advisories = [
        'Coarse Language', 'Language May Offend', 'Violence', 'Frightening Scenes',
        'Brutal Violence', 'Gory Scenes', 'Sexual Violence', 'Nudity',
        'Sexually Suggestive Scenes', 'Sexual Content', 'Explicit Sexual Content'
    ]
    sql = "INSERT INTO advisories (advisory_description) VALUES (%s)"
    data = [(a,) for a in advisories]
    execute_many(sql, data, db_config)
    print("Inserted advisories")
 
def populate_directors(db_config, n=10):
    sql = "INSERT INTO directors (director_id, director_first_name, director_last_name) VALUES (%s, %s, %s)"
    data = [(i, fake.first_name(), fake.last_name()) for i in range(1, n+1)]
    execute_many(sql, data, db_config)
    print(f"Inserted {n} directors")
 
def populate_actors(db_config, n=10):
    sql = "INSERT INTO actors (actor_id, actor_first_name, actor_last_name) VALUES (%s, %s, %s)"
    data = [(i, fake.first_name(), fake.last_name()) for i in range(1, n+1)]
    execute_many(sql, data, db_config)
    print(f"Inserted {n} actors")
 
def populate_customers(db_config, n=10):
    provinces = ['AB', 'BC', 'ON', 'SK', 'MB', 'NB', 'NL', 'NS', 'PE', 'QC', 'YT', 'NT', 'NU']
    sql = """INSERT INTO customers 
    (customer_id, customer_first_name, customer_last_name, customer_street, customer_city, 
     customer_province, customer_postal_code, customer_email, customer_phone) 
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    data = []
    for i in range(1, n+1):
        data.append((
            i,
            fake.first_name(),
            fake.last_name(),
            fake.street_address(),
            fake.city(),
            random.choice(provinces),
            generate_postal_code(),
            fake.email(),
            generate_phone()
        ))
    execute_many(sql, data, db_config)
    print(f"Inserted {n} customers")
 
def populate_movies(db_config, n=10, max_director_id=10):
    ratings = ['G', 'PG', '14A', '18A', 'R']
    sql = """INSERT INTO movies 
        (movie_id, director_id, movie_title, sd_price, hd_price, movie_duration, movie_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    data = []
    for i in range(1, n+1):
        director_id = random.randint(1, max_director_id)
        title = fake.sentence(nb_words=3).rstrip('.')
        sd_price = round(random.uniform(1.99, 19.99), 2)
        hd_price = round(random.uniform(sd_price, 19.99), 2)
        duration = random.randint(80, 180)
        rating = random.choice(ratings)
        data.append((i, director_id, title, sd_price, hd_price, duration, rating))
    execute_many(sql, data, db_config)
    print(f"Inserted {n} movies")
 
def populate_movie_categories(db_config, movie_count=10):
    sql = "INSERT INTO movie_categories (movie_id, category_name) VALUES (%s, %s)"
    categories = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Animation', 'Romance', 'Documentary']
    data = []
    for movie_id in range(1, movie_count+1):
        cats = random.sample(categories, random.randint(1, 3))
        for cat in cats:
            data.append((movie_id, cat))
    execute_many(sql, data, db_config)
    print("Inserted movie_categories")
 
def populate_actor_roles(db_config, num_actor_roles=1000, movie_count=1000, actor_count=1000):
    sql = "INSERT INTO actor_roles (movie_id, actor_id, actor_role) VALUES (%s, %s, %s)"
    data = []
    # Use a set to track unique movie-actor pairs
    existing_pairs = set()

    for _ in range(num_actor_roles):
        while True:
            movie_id = random.randint(1, movie_count)
            actor_id = random.randint(1, actor_count)
            pair = (movie_id, actor_id)

            if pair not in existing_pairs:
                existing_pairs.add(pair)
                role = fake.job()
                data.append((movie_id, actor_id, role))
                break  # Exit the while loop once a unique pair is found

    execute_many(sql, data, db_config)
    print(f"Inserted {len(data)} unique actor_roles")
 
def populate_movie_advisories(db_config, movie_count=10):
    # First get advisory IDs from DB (assuming serial PK)
    conn = psycopg2.connect(**db_config)
    advisory_ids = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT advisory_id FROM advisories")
            advisory_ids = [row[0] for row in cur.fetchall()]
    finally:
        conn.close()
    sql = "INSERT INTO movie_advisories (movie_id, advisory_id) VALUES (%s, %s)"
    data = []
    for movie_id in range(1, movie_count+1):
        advs = random.sample(advisory_ids, random.randint(0, 3))
        for adv_id in advs:
            data.append((movie_id, adv_id))
    execute_many(sql, data, db_config)
    print("Inserted movie_advisories")
 
def populate_wishlist(db_config, num_wishlist=1000, customer_count=1000, movie_count=1000):
    sql = "INSERT INTO wishlist (customer_id, movie_id, date_added) VALUES (%s, %s, %s)"
    data = []
    # Use a set to track unique customer-movie pairs
    existing_pairs = set()

    for _ in range(num_wishlist):
        while True:
            customer_id = random.randint(1, customer_count)
            movie_id = random.randint(1, movie_count)
            pair = (customer_id, movie_id)

            if pair not in existing_pairs:
                existing_pairs.add(pair)
                date_added = fake.date_between(start_date='-1y', end_date='today')
                data.append((customer_id, movie_id, date_added))
                break  # Exit the while loop once a unique pair is found

    execute_many(sql, data, db_config)
    print(f"Inserted {len(data)} unique wishlist entries")
 
def populate_credit_cards(db_config, customer_count):
    sql = "INSERT INTO creditcards (customer_id, creditcard_number, creditcard_type) VALUES (%s, %s, %s)"
    card_types = ['AX', 'VS', 'MC']
    data = []
    for customer_id in range(1, customer_count+1):
        cc_number = fake.credit_card_number(card_type=None).replace('-', '')[:16]
        cc_type = random.choice(card_types)
        data.append((customer_id, cc_number, cc_type))
    execute_many(sql, data, db_config)
    print("Inserted credit cards")
 
def populate_rentals(db_config, rental_count=15, movie_count=10, customer_count=10):
    sql = """INSERT INTO rentals
    (rental_id, movie_id, customer_id, rental_start_date, rental_watch_date, rental_expiry_date, rental_return_date, customer_rating)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    data = []
    # Use a set to track unique rental IDs
    existing_rental_ids = set()
    for _ in range(rental_count):
        while True:
            rental_id = random.randint(1, rental_count)
            if rental_id not in existing_rental_ids:
                existing_rental_ids.add(rental_id)
                movie_id = random.randint(1, movie_count)
                customer_id = random.randint(1, customer_count)
                rental_start_date = fake.date_between(start_date='-1y', end_date='today')
                rental_watch_date = rental_start_date + timedelta(days=random.randint(0, 3))
                rental_expiry_date = rental_watch_date + timedelta(days=random.randint(1, 7))
                rental_return_date = rental_watch_date + timedelta(days=random.randint(0, 5))
                rating = random.randint(1, 5)
                data.append((rental_id, movie_id, customer_id, rental_start_date, rental_watch_date, rental_expiry_date, rental_return_date, rating))
                break
    execute_many(sql, data, db_config)
    print(f"Inserted {len(data)} rentals")
 
if __name__ == "__main__":
    db_config = {
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": 5432,
        "dbname": "vod_db"
    }

    # Updated row counts for each table
    num_directors = 1000
    num_actors = 1000
    num_customers = 1000
    num_movies = 1000
    num_actor_roles = 1000
    num_wishlist = 1000
    num_rentals = 5000 

    # Insert fixed lookup tables first
    populate_categories(db_config)
    populate_advisories(db_config)

    # Insert base entities with the new row counts
    populate_directors(db_config, n=num_directors)
    populate_actors(db_config, n=num_actors)
    populate_customers(db_config, n=num_customers)

    # Movies and related tables
    populate_movies(db_config, n=num_movies, max_director_id=num_directors)
    populate_movie_categories(db_config, movie_count=num_movies)
    
    # UPDATED: to use the new row count for actor_roles
    populate_actor_roles(db_config, num_actor_roles=num_actor_roles, movie_count=num_movies, actor_count=num_actors)
    
    populate_movie_advisories(db_config, movie_count=num_movies)

    # Customer related tables
    # UPDATED: to use the new row count for wishlist
    populate_wishlist(db_config, num_wishlist=num_wishlist, customer_count=num_customers, movie_count=num_movies)
    
    populate_credit_cards(db_config, customer_count=num_customers)
    populate_rentals(db_config, rental_count=num_rentals, movie_count=num_movies, customer_count=num_customers)