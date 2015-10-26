ALTER TABLE `search_log`  ENGINE=MyISAM;
ALTER TABLE `search_log`  CHANGE COLUMN `count` `count` INT(10) UNSIGNED NOT NULL DEFAULT '1' AFTER `updated_date`;