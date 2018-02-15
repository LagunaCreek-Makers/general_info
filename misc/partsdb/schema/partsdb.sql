-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema partsdatabase
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema partsdatabase
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `partsdatabase` DEFAULT CHARACTER SET utf8 ;
USE `partsdatabase` ;

-- -----------------------------------------------------
-- Table `partsdatabase`.`asset_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`asset_type` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `type_UNIQUE` (`type` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`category` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NOT NULL,
  `parent_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`manufacturer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`manufacturer` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `manufacturer` VARCHAR(45) NOT NULL,
  `homepage_url` VARCHAR(256) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `manufacturer_UNIQUE` (`manufacturer` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`package_classification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`package_classification` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `classification` VARCHAR(45) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`packaging`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`packaging` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `packaging` VARCHAR(45) NOT NULL,
  `classification_id` INT(11) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `num_pins` SMALLINT(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `packaging_UNIQUE` (`packaging` ASC),
  INDEX `fk_packaging_classification_id_idx` (`classification_id` ASC),
  CONSTRAINT `fk_packaging_classification_id`
    FOREIGN KEY (`classification_id`)
    REFERENCES `partsdatabase`.`package_classification` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`storage_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`storage_location` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `storage_location` VARCHAR(45) NOT NULL,
  `comment` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `storage_location_UNIQUE` (`storage_location` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`supplier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`supplier` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `url` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`part`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`part` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `category_id` INT(11) NOT NULL,
  `mpn` VARCHAR(45) NOT NULL,
  `manufacturer_id` INT(11) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `short_description` VARCHAR(255) NULL DEFAULT NULL,
  `storage_id` INT(11) NOT NULL,
  `comments` TEXT NULL DEFAULT NULL,
  `packaging_id` INT(11) NULL DEFAULT NULL,
  `stock_level` SMALLINT(6) NULL DEFAULT NULL,
  `supplier_id` INT(11) NULL DEFAULT NULL,
  `price` FLOAT NULL DEFAULT NULL,
  `entry_created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `entry_modified` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_part_manufacturer_id_idx` (`manufacturer_id` ASC),
  INDEX `fk_part_category_id_idx` (`category_id` ASC),
  INDEX `fk_part_storage_id_idx` (`storage_id` ASC),
  INDEX `fk_part_supplier_id_idx` (`supplier_id` ASC),
  INDEX `fk_part_packaging_id_idx` (`packaging_id` ASC),
  CONSTRAINT `fk_part_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `partsdatabase`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_part_manufacturer_id`
    FOREIGN KEY (`manufacturer_id`)
    REFERENCES `partsdatabase`.`manufacturer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_part_packaging_id`
    FOREIGN KEY (`packaging_id`)
    REFERENCES `partsdatabase`.`packaging` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_part_storage_id`
    FOREIGN KEY (`storage_id`)
    REFERENCES `partsdatabase`.`storage_location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_part_supplier_id`
    FOREIGN KEY (`supplier_id`)
    REFERENCES `partsdatabase`.`supplier` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`part_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`part_asset` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `asset_type_id` INT(11) NOT NULL,
  `part_id` INT(11) NOT NULL,
  `asset` MEDIUMBLOB NULL DEFAULT NULL,
  `metadata` TEXT NULL DEFAULT NULL,
  `comment` TEXT NULL DEFAULT NULL,
  `attribution` TEXT NULL DEFAULT NULL,
  `url` VARCHAR(255) NULL DEFAULT NULL,
  `source` VARCHAR(255) NULL DEFAULT NULL,
  `subtype` VARCHAR(255) NULL DEFAULT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `size` INT(11) NOT NULL,
  `md5` VARCHAR(16) NOT NULL,
  `entry_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `entry_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_asset_part_id_idx` (`part_id` ASC),
  INDEX `fk_asset_asset_type_id_idx` (`asset_type_id` ASC),
  UNIQUE INDEX `md5_UNIQUE` (`md5` ASC),
  CONSTRAINT `fk_asset_asset_type_id`
    FOREIGN KEY (`asset_type_id`)
    REFERENCES `partsdatabase`.`asset_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_asset_part_id`
    FOREIGN KEY (`part_id`)
    REFERENCES `partsdatabase`.`part` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`category_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`category_asset` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `asset` MEDIUMBLOB NOT NULL,
  `metadata` TEXT NULL DEFAULT NULL,
  `asset_type_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `size` INT NOT NULL,
  `md5` VARCHAR(16) NOT NULL,
  `entry_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `entry_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_category_asset_type_id_idx` (`asset_type_id` ASC),
  UNIQUE INDEX `md5_UNIQUE` (`md5` ASC),
  INDEX `fk_category_asset_category_id_idx` (`category_id` ASC),
  CONSTRAINT `fk_category_asset_type_id`
    FOREIGN KEY (`asset_type_id`)
    REFERENCES `partsdatabase`.`asset_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_asset_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `partsdatabase`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`order_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`order_asset` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `asset` MEDIUMBLOB NOT NULL,
  `metadata` TEXT NULL DEFAULT NULL,
  `asset_type_id` INT(11) NOT NULL,
  `order_number` VARCHAR(45) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `size` INT NOT NULL,
  `md5` VARCHAR(16) NOT NULL,
  `entry_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `entry_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `md5_UNIQUE` (`md5` ASC),
  INDEX `fk_order_asset_asset_id_idx` (`asset_type_id` ASC),
  CONSTRAINT `fk_order_asset_asset_id`
    FOREIGN KEY (`asset_type_id`)
    REFERENCES `partsdatabase`.`asset_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`orders` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `order_number` VARCHAR(45) NULL DEFAULT NULL,
  `part_id` INT(11) NOT NULL,
  `supplier_id` INT(11) NOT NULL,
  `quantity` INT(11) NOT NULL,
  `price` FLOAT NULL DEFAULT NULL,
  `order_asset_id` INT NULL,
  `comment` TEXT NULL DEFAULT NULL,
  `entry_created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_part_id_idx` (`part_id` ASC),
  INDEX `fk_orders_supplier_idx` (`supplier_id` ASC),
  INDEX `fk_order_order_asset_id_idx` (`order_asset_id` ASC),
  CONSTRAINT `fk_orders_part_id`
    FOREIGN KEY (`part_id`)
    REFERENCES `partsdatabase`.`part` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_supplier`
    FOREIGN KEY (`supplier_id`)
    REFERENCES `partsdatabase`.`supplier` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_order_asset_id`
    FOREIGN KEY (`order_asset_id`)
    REFERENCES `partsdatabase`.`order_asset` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`unit_of_measurement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`unit_of_measurement` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `abbreviation` VARCHAR(45) NULL DEFAULT NULL,
  `symbol` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `partsdatabase`.`part_parameter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `partsdatabase`.`part_parameter` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `part_id` INT(11) NOT NULL,
  `parameter` VARCHAR(45) NOT NULL,
  `value` VARCHAR(45) NOT NULL,
  `min` VARCHAR(45) NULL DEFAULT NULL,
  `max` VARCHAR(45) NULL DEFAULT NULL,
  `unit_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_part_parameter_part_id_idx` (`part_id` ASC),
  INDEX `fk_part_unitofmeasurement_id_idx` (`unit_id` ASC),
  CONSTRAINT `fk_part_parameter_part_id`
    FOREIGN KEY (`part_id`)
    REFERENCES `partsdatabase`.`part` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_part_unitofmeasurement_id`
    FOREIGN KEY (`unit_id`)
    REFERENCES `partsdatabase`.`unit_of_measurement` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
