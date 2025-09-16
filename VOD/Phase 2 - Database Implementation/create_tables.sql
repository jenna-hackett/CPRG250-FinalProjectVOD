DROP TABLE IF EXISTS RENTALS CASCADE;
DROP TABLE IF EXISTS CREDITCARDS CASCADE;
DROP TABLE IF EXISTS WISHLIST CASCADE;
DROP TABLE IF EXISTS MOVIE_ADVISORIES CASCADE;
DROP TABLE IF EXISTS ADVISORIES CASCADE;
DROP TABLE IF EXISTS ACTOR_ROLES CASCADE;
DROP TABLE IF EXISTS MOVIE_CATEGORIES CASCADE;
DROP TABLE IF EXISTS CATEGORIES CASCADE;
DROP TABLE IF EXISTS MOVIES CASCADE;
DROP TABLE IF EXISTS DIRECTORS CASCADE;
DROP TABLE IF EXISTS ACTORS CASCADE;
DROP TABLE IF EXISTS CUSTOMERS CASCADE;
 
CREATE TABLE DIRECTORS (
    director_id INT PRIMARY KEY,
    director_first_name VARCHAR(100) NOT NULL,
    director_last_name VARCHAR(100) NOT NULL
);
 
CREATE TABLE ACTORS (
    actor_id INT PRIMARY KEY,
    actor_first_name VARCHAR(100) NOT NULL,
    actor_last_name VARCHAR(100) NOT NULL
);
 
CREATE TABLE CATEGORIES (
    category_name VARCHAR(50) PRIMARY KEY
);
 
CREATE TABLE ADVISORIES (
    advisory_id SERIAL PRIMARY KEY,
    advisory_description TEXT NOT NULL CHECK (
        advisory_description IN (
            'Coarse Language', 'Language May Offend', 'Violence', 'Frightening Scenes',
            'Brutal Violence', 'Gory Scenes', 'Sexual Violence', 'Nudity',
            'Sexually Suggestive Scenes', 'Sexual Content', 'Explicit Sexual Content'
        )
    )
);
 
CREATE TABLE CUSTOMERS (
    customer_id INT PRIMARY KEY,
    customer_first_name VARCHAR(100) NOT NULL,
    customer_last_name VARCHAR(100) NOT NULL,
    customer_street VARCHAR(100) NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_province VARCHAR(2) NOT NULL CHECK (
        customer_province IN ('AB', 'BC', 'ON', 'SK', 'MB', 'NB', 'NL', 'NS', 'PE', 'QC', 'YT', 'NT', 'NU')
    ),
    customer_postal_code VARCHAR(6) NOT NULL CHECK (
        customer_postal_code ~ '^[A-Z][0-9][A-Z][0-9][A-Z][0-9]$'
    ),
    customer_email VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(12) NOT NULL CHECK (
        customer_phone ~ '^\d{3}-\d{3}-\d{4}$'
    )
);
 
CREATE TABLE MOVIES (
    movie_id INT PRIMARY KEY,
    director_id INT NOT NULL REFERENCES DIRECTORS(director_id),
    movie_title VARCHAR(50) NOT NULL,
    sd_price DECIMAL(10, 2) NOT NULL,
    hd_price DECIMAL(10, 2) NOT NULL,
    movie_duration INT NOT NULL,
    movie_rating VARCHAR(4) CHECK (
        movie_rating IN ('G', 'PG', '14A', '18A', 'R')
    )
);
 
CREATE TABLE MOVIE_CATEGORIES (
    movie_id INT NOT NULL REFERENCES MOVIES(movie_id),
    category_name VARCHAR(50) REFERENCES CATEGORIES(category_name),
    PRIMARY KEY (movie_id, category_name)
);
 
CREATE TABLE ACTOR_ROLES (
    movie_id INT NOT NULL REFERENCES MOVIES(movie_id),
    actor_id INT NOT NULL REFERENCES ACTORS(actor_id),
    actor_role TEXT NOT NULL,
    PRIMARY KEY (movie_id, actor_id)
);
 
CREATE TABLE MOVIE_ADVISORIES (
    movie_id INT NOT NULL REFERENCES MOVIES(movie_id),
    advisory_id INT NOT NULL REFERENCES ADVISORIES(advisory_id),
    PRIMARY KEY (movie_id, advisory_id)
);
 
CREATE TABLE WISHLIST (
    customer_id INT NOT NULL REFERENCES CUSTOMERS(customer_id),
    movie_id INT NOT NULL REFERENCES MOVIES(movie_id),
    date_added DATE NOT NULL,
    PRIMARY KEY (customer_id, movie_id)
);
 
CREATE TABLE CREDITCARDS (
    customer_id INT NOT NULL REFERENCES CUSTOMERS(customer_id),
    creditcard_number VARCHAR(16) NOT NULL,
    creditcard_type VARCHAR(2) NOT NULL CHECK (
        creditcard_type IN ('AX', 'VS', 'MC')
    ),
    PRIMARY KEY (customer_id)
);
 
 
CREATE TABLE RENTALS (
    rental_id INT PRIMARY KEY,
    movie_id INT NOT NULL REFERENCES MOVIES(movie_id),
    customer_id INT NOT NULL REFERENCES CUSTOMERS(customer_id),
    rental_start_date DATE NOT NULL,
    rental_watch_date DATE,
    rental_expiry_date DATE,
    rental_return_date DATE,
    customer_rating INT NOT NULL CHECK (
        customer_rating BETWEEN 1 AND 5
    ),
    CHECK (rental_watch_date >= rental_start_date),
    CHECK (rental_expiry_date >= rental_watch_date)
);