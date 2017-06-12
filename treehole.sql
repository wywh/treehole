DROP DATABASE IF EXISTS `treehole`;
CREATE DATABASE `treehole` COLLATE utf8_general_ci;;

use `treehole`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` bigint(20) NOT NULL,
  `isAdmin` tinyint(3) NOT NULL DEFAULT '0',
  `isBlocked` tinyint(3) NOT NULL DEFAULT '0',
  `isForwardTarget` tinyint(3) NOT NULL DEFAULT '0',
  `messageCycleTS` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `lastMessage` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `messagesInCycle` tinyint(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;