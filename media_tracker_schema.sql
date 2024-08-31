-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema media_tracker_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `media_tracker_schema` ;

-- -----------------------------------------------------
-- Schema media_tracker_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `media_tracker_schema` DEFAULT CHARACTER SET utf8 ;
USE `media_tracker_schema` ;

-- -----------------------------------------------------
-- Table `media_tracker_schema`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `media_tracker_schema`.`users` ;

CREATE TABLE IF NOT EXISTS `media_tracker_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `media_tracker_schema`.`movies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `media_tracker_schema`.`movies` ;

CREATE TABLE IF NOT EXISTS `media_tracker_schema`.`movies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `release_date` DATE NOT NULL,
  `director` VARCHAR(60) NOT NULL,
  `details` VARCHAR(1000) NOT NULL,
  `owner_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_movies_users_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_movies_users`
    FOREIGN KEY (`owner_id`)
    REFERENCES `media_tracker_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `media_tracker_schema`.`favorite_movies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `media_tracker_schema`.`favorite_movies` ;

CREATE TABLE IF NOT EXISTS `media_tracker_schema`.`favorite_movies` (
  `movie_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`movie_id`, `user_id`),
  INDEX `fk_movies_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_movies_has_users_movies1_idx` (`movie_id` ASC) VISIBLE,
  CONSTRAINT `fk_movies_has_users_movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `media_tracker_schema`.`movies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `media_tracker_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `media_tracker_schema`.`movie_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `media_tracker_schema`.`movie_comments` ;

CREATE TABLE IF NOT EXISTS `media_tracker_schema`.`movie_comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `users_id` INT NOT NULL,
  `movie_id` INT NOT NULL,
  `comment` VARCHAR(500) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  INDEX `fk_movie_comments_users1_idx` (`users_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  INDEX `fk_movie_comments_movies1_idx` (`movie_id` ASC) VISIBLE,
  CONSTRAINT `fk_movie_comments_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `media_tracker_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_comments_movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `media_tracker_schema`.`movies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
