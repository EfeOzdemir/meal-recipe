DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS saved_recipe;
DROP TABLE IF EXISTS recipe_ingredient;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE ingredient (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE recipe (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    cre_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
) ENGINE=InnoDB;

CREATE TABLE saved_recipe (
    recipe_id INT NOT NULL,
    user_id INT NOT NULL,
    cre_date TIMESTAMP NOT NULL,
    PRIMARY KEY (recipe_id, user_id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)  
) ENGINE=InnoDB;

CREATE TABLE recipe_ingredient (
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient (id)  
) ENGINE=InnoDB;

CREATE TABLE likes (
    recipe_id INT NOT NULL,
    user_id INT NOT NULL,
    cre_date TIMESTAMP NOT NULL,
    PRIMARY KEY (recipe_id, user_id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)  
) ENGINE=InnoDB;

CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    cre_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)  
) ENGINE=InnoDB;

INSERT INTO category (name) VALUES ('test');
INSERT INTO category (name) VALUES ('test2');