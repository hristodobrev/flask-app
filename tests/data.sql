INSERT INTO user (username, password)
VALUES
    ('test', 'pbkdf2:sha256:260000$UaaAXX0AVFux3maL$5045edf299fe18ee4aabea2e52b165b682f4afe27eaa5a1ea332a858bafb1f3d'),
    ('other', 'pbkdf2:sha256:260000$cZJzZfzzCOIxTmw7$b6272d4adfac196cd38b162dfbf3cd5e09daa6fad39d924240676aa0e604e54e');

INSERT INTO post (title, body, author_id, created)
VALUES
    ('test title', 'test' || x'0a' || 'body', 1, '2022-12-17 16:45:21');