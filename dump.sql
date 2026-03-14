PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	id INTEGER NOT NULL, 
	tg_id BIGINT, 
	balance VARCHAR(15) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE ai_types (
	id INTEGER NOT NULL, 
	name VARCHAR(25) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO ai_types VALUES(1,'YandexGPT_text');
INSERT INTO ai_types VALUES(2,'YandexGPT_Image');
CREATE TABLE ai_models (
	id INTEGER NOT NULL, 
	name VARCHAR(25) NOT NULL, 
	ai_type INTEGER NOT NULL, 
	price VARCHAR(25) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ai_type) REFERENCES ai_types (id)
);
INSERT INTO ai_models VALUES(1,'yandexgpt',1,'0.0006');
INSERT INTO ai_models VALUES(2,'yandexgpt-lite',1,'0.0001');
INSERT INTO ai_models VALUES(3,'yandex-art',2,'2.2');
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	user INTEGER NOT NULL, 
	amount VARCHAR(15) NOT NULL, 
	created_at DATETIME NOT NULL, 
	"order" VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user) REFERENCES users (id)
);
COMMIT;
