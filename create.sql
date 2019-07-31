USE newgram;

CREATE TABLE uploads (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    description VARCHAR (128) NOT NULL DEFAULT "",
    upload_date INT UNSIGNED NOT NULL DEFAULT unix_timestamp(),

    image BLOB NOT NULL,

    uploader INT UNSIGNED,

    CONSTRAINT uploader_cx
    FOREIGN KEY uploader_fk (uploader)
    REFERENCES users (id)
    ON DELETE SET NULL,

    PRIMARY KEY (id)
);

CREATE TABLE users (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    username VARCHAR (32) UNIQUE NOT NULL,
    bio VARCHAR (256) NOT NULL DEFAULT "",
    email VARCHAR (128) NOT NULL,
--    verified TINYINT NOT NULL DEFAULT 0,
    password_hash VARCHAR (93) NOT NULL,

    PRIMARY KEY (id)
);