DROP TABLE IF EXISTS plugin_mailman;

-- Update service for all projects
UPDATE service
SET link = REPLACE(link, '/plugins/mailman/', '/mail/')
WHERE short_name = 'mail';
