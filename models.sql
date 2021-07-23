  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR NOT NULL,
      email VARCHAR NOT NULL,
      password VARCHAR NOT NULL,
      date_of_birth VARCHAR NOT NULL,
      created_at DATE,
      favouritegenre INTEGER,
  );

  CREATE TABLE reviews (
      id SERIAL PRIMARY KEY,
      movie_id INTEGER,
      user_id INTEGER REFERENCES users,
      rating INTEGER,
      review VARCHAR
  );

    CREATE TABLE genres (
      genre_id PRIMARY KEY,
      name VARCHAR
  );

  CREATE TABLE results (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users,
      genre1 INTEGER REFERENCES genres,
      genre2 INTEGER REFERENCES genres,
      genre3 INTEGER REFERENCES genres,
      decade VARCHAR,
      language VARCHAR

  );

CREATE TABLE watchedmovies (
      id SERIAL PRIMARY KEY,
      movie_id INTEGER,
      user_id INTEGER REFERENCES users
  );