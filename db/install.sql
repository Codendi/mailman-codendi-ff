CREATE TABLE plugin_mailman (
  listname varchar(100) NOT NULL,
  address varchar(255) NOT NULL,
  hide varchar(255) NOT NULL default 'N',
  nomail varchar(255) NOT NULL default 'N',
  ack varchar(255) NOT NULL default 'Y',
  not_metoo varchar(255) NOT NULL default 'Y',
  digest varchar(255) NOT NULL default 'N',
  plain varchar(255) NOT NULL default 'N',
  `password` varchar(255) NOT NULL default '!',
  lang varchar(255) NOT NULL default 'en',
  `name` varchar(255) default NULL,
  one_last_digest varchar(255) NOT NULL default 'N',
  user_options bigint(20) NOT NULL default '0',
  delivery_status mediumint(9) NOT NULL default '0',
  topics_userinterest varchar(255) default NULL,
  delivery_status_timestamp timestamp NOT NULL default '0000-00-00 00:00:00',
  bi_cookie varchar(255) default NULL,
  bi_score double NOT NULL default '0',
  bi_noticesleft double NOT NULL default '0',
  bi_lastnotice date NOT NULL default '1901-01-01',
  bi_date date NOT NULL default '1901-01-01',
  PRIMARY KEY  (listname,address(200))
);

-- Create service for all projects (but disabled)
INSERT INTO service(group_id, label, description, short_name, link, is_active, is_used, scope, rank)
SELECT DISTINCT group_id , 'Mailman' , 'Mailman plugin' , 'plugin_mailman', CONCAT('/plugins/mailman/?group_id=', group_id), 1 , 0 , 'system',  81
FROM service
WHERE group_id NOT IN (SELECT group_id
    FROM service
    WHERE short_name
    LIKE 'plugin_mailman');

