CREATE DATABASE job_applier;

USE job_applier;

CREATE TABLE sites (
    id int NOT NULL AUTO_INCREMENT,
    site_name VARCHAR(255),
    search_terms VARCHAR(255),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now() ON UPDATE now(),
    PRIMARY KEY (id)
);

CREATE TABLE jobs (
    id int NOT NULL AUTO_INCREMENT,
    site_id INT NOT NULL,
    job_title VARCHAR(255),
    url VARCHAR(255),
    third_party_application BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT now(),
    updated_at timestamp DEFAULT now() ON UPDATE now(),
    PRIMARY KEY (id),
    FOREIGN KEY (site_id) REFERENCES sites(id)
);