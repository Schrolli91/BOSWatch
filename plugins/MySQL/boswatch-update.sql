USE boswatch;

-- rename old columns including little error-prevention
ALTER IGNORE TABLE `bos_pocsag` change `funktion` `function` INT(1);
ALTER IGNORE TABLE `bos_pocsag` change `funktionChar` `functionChar` TEXT(1);
