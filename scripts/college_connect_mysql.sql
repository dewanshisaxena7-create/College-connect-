-- College Connect Custom MySQL Dump
CREATE DATABASE IF NOT EXISTS college_connect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE college_connect;

CREATE TABLE IF NOT EXISTS `core_teacher` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `teacher_id` varchar(100) NOT NULL UNIQUE,
  `password` varchar(255) DEFAULT NULL,
  `is_first_login` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `core_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `roll_number` varchar(50) NOT NULL UNIQUE,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `core_classschedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(100) NOT NULL,
  `room_number` varchar(50) NOT NULL,
  `day` varchar(10) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `core_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `schedule_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`schedule_id`) REFERENCES `core_classschedule` (`id`) ON DELETE CASCADE
);

-- Inserting Teachers
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Kirti Mathu', 'kir.thu', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Ramesh Thakur', 'ram.kur', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Shaligram Prajapat', 'sha.pat', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Yasmin Shaikh', 'yas.ikh', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Rahul Singhai', 'rah.hai', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Jugendra Dongre', 'jug.gre', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Manju Suchdeo', 'man.deo', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Poonam Mangwani', 'poo.ani', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Vivek Shrivastava', 'viv.ava', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Basant Namdeo', 'bas.deo', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Nitin Nagar', 'nit.gar', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Rupesh Sendre', 'rup.dre', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Shraddha Soni', 'shr.oni', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Kirti Vijayvargiya', 'kir.iya', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Rajesh Verma', 'raj.rma', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Pradeep K. Jatav', 'pra.tav', NULL, 1);
INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('Shailvi Verma', 'sha.rma', NULL, 1);

-- Inserting Students
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-01', 'AASTHA MATHANIYA', 'pbkdf2_sha256$720000$9cc70ca9f885ae5cba824b53$2e7Exj/1DmHl7PHPUB/d/JtBxE0TL1NegCEk3gex96E=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-02', 'AAYUSH CHOURASIA', 'pbkdf2_sha256$720000$a76297ac5bccee808dd7f8df$jqjyhbdACHwU7j6Igfqqpsh5GV29/eiL4zTWZ3tG8vQ=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-03', 'AAYUSH SURYAWANSHI', 'pbkdf2_sha256$720000$18866d9a1024c90a0f7e2976$I1ydFq9rg+MbCdNvdwRhiV/HCPNuMdQ0uArSb5mJRDE=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-04', 'AAYUSHI RATHORE', 'pbkdf2_sha256$720000$b22186325227a45a4cd35eae$0K8DKvJF4tKjTf1dZRAJwEzKyfshiH1RhZyq2vbYUic=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-05', 'ABDUL REHMAN MANSOORI', 'pbkdf2_sha256$720000$aa8e8d28f5fd5fbdc5a32f6d$GskVEa6qjZltVl174c4kBIb4ivz1N/aHC0T3ANVYPpc=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-06', 'ABHISHEK YADAV', 'pbkdf2_sha256$720000$128277a7b20bfa5cfbd79b16$kjq8BUQhG4qrpG7nw35tJ2NLOo2ETNqVNPLPmIJf5+0=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-07', 'AKSHAT THAKUR', 'pbkdf2_sha256$720000$e94dc33f2fd8c39defd9a737$qhNT5s2apciX+cHw5857X6tVvlhv+Gr9OiOPD4V8z5E=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-08', 'AKSHATA RAMESH GHODCHAR', 'pbkdf2_sha256$720000$6b1803f69843dfc89bf15343$uJUI4DIJmQzyOdb/FpBVw6Z/mjATdYKHBoB6GZKBE5k=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-09', 'AKSHAY JAIN', 'pbkdf2_sha256$720000$a1aa10715c160d5e94c83d6b$6tWqNPPL6vfvAifqyXEuFAyGC/BBNb00aw+zMPXfhI4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-10', 'ANIKA BABAR', 'pbkdf2_sha256$720000$579485e40ea352b6b28c334a$kSx5XUz3AO4+r0Hodj6YR7lKq3hjda5B7r8DmFr6PVE=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-11', 'ANSHITA SONI', 'pbkdf2_sha256$720000$11b4b6a5d631e8301106c3da$NjTTNiQGnZe9k3LcXepdRAU8O13J75fc3n0rT/h7f88=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-12', 'ANUSHKA SHARMA', 'pbkdf2_sha256$720000$401e51a16216ab3eccbfe39a$ujmPU4fJ/n21yc2lvEqzEhwW8t88wcn9SKZlem39kuA=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-13', 'ASHWIN SUPATH', 'pbkdf2_sha256$720000$e2f77ce09a07b11a29869570$guHu+x2hkffJhbhxSL9fi3rnUTUs24n5XgoL7L8xK7E=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-14', 'ATHARV CHINCHE', 'pbkdf2_sha256$720000$987c36a75980b05cd8febae2$3AkLAOm4/PuNDEks7YOrDIAT688nrdKVkcFpSeUk7Fk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-15', 'ATHARVA CHAUHAN', 'pbkdf2_sha256$720000$5231400fa1c9c284f9457688$Zkp4Iqi9UW4qFO5ynXJOcetUY7AiweQNhlZL29id4b8=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-16', 'AYUSH JAISWAL', 'pbkdf2_sha256$720000$778f4a33e439ce52463a3181$BltH3xt04pKE993vQ/RZN0Klo4RaoSDHpGw7PgGREgg=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-17', 'AYUSH SINDHIYA', 'pbkdf2_sha256$720000$78d2555cf0ec9c5bdd317efa$UydEJYxH2lTevF9TC6dC7iPCU8jHcegcOxs0qRwoKJo=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-18', 'BISHAL KUMAR', 'pbkdf2_sha256$720000$adf339f1988cab53a8878e8c$5D+ma9oCPePeG6UikmpT/E0ENez3hCnhOTy5KS6e8z4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-19', 'CHINDAN KUSHWAHA', 'pbkdf2_sha256$720000$ce0a51767ac5fd5c4ee56707$vvB3aOIySSRIpWxj/hwgyprOaUMqJyK/d3aXWZiefI8=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-20', 'DEEPSHIKHA VISHWAKARMA', 'pbkdf2_sha256$720000$5fc38dcce2e7bc82a20ef1ef$08lObR6qqCRVU23f9/oLVIhObNHNbTizQQXX26vsJjk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-21', 'DEV KUMAR JAIN', 'pbkdf2_sha256$720000$b765a388d6d7f37e4fd01c6f$3Y2i+kgSNKjnT7XQQWuVD+Tq2W+JH1RI6+ifTow2qK4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-22', 'DEV PANDEY', 'pbkdf2_sha256$720000$2da10dbbad11afa4e2228f7a$cmcChy2MFJ3mFTHg9iZ0X/PphfSOGxdZ6Pp7KlS8p/g=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-23', 'DEVANSHI KARVE', 'pbkdf2_sha256$720000$5ca9408f04759ce746b4cc9e$3M4v9brdkvy8xLkC3Y+sYGbjmut/RGJSq6emymSShFs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-24', 'DEVANSHI SAXENA', 'pbkdf2_sha256$720000$7f7ca159420d115751b5da2d$3MgDujKEPyFTFTOSILvoTyLxALqCwn1q79eqB4Ib1q4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-25', 'DEVASHISH PATEL', 'pbkdf2_sha256$720000$6c4e85bb3278bab3dfa0dbe6$P7Lk+8JWfRebAlK/dZPIW92cj2/vx7zBQQbvCfRzhSk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-26', 'DHAIRYA JOSHI', 'pbkdf2_sha256$720000$3484130296ac48b6f04a8a27$49lRi4vIOy7o80w6xo4DD36R37SvXgjUWbwEl1AG8ow=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-27', 'DISHA CHAWLA', 'pbkdf2_sha256$720000$583ef12fe67e786c8212442d$tC0zjgvbAyMzcQIA6+clok9imgwldiyjFaip1Zni1nI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-28', 'DISHAN SHEIKH', 'pbkdf2_sha256$720000$5f9b295376def13431caba3a$L5Tn9xZJLlcCEgtIZAluKT/kDbPaj2ir5hHhSupCUXE=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-29', 'DIVYA SHARMA', 'pbkdf2_sha256$720000$9c9e4aebc784967bc95c54dc$EbVlvgodpMo4gw8rMVR/hOzZ2UDfAxgAHuasjdg5nl0=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-30', 'DIVYANSH AREKAR', 'pbkdf2_sha256$720000$a91a598e0ad1c1c9de4249ee$gkx5jIQLZwB8rsh42ihTxTdAV78LBt1ChFKpTas4ADE=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-31', 'DIVYANSH VERMA', 'pbkdf2_sha256$720000$3fa79d4147dd4ddc5aadc938$mv6mGocfINpD8ugea2Gi6v/lajYFH2wW4L6VkowkA4Y=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-32', 'DIVYESH SINGH GEHLOT', 'pbkdf2_sha256$720000$b5dfaa24816c080c93c28909$LRfU4b6f+MGTfNrrX2COE0kHePGZuIt+i1UQD3B49Ok=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-33', 'HANSIKA GURJAR', 'pbkdf2_sha256$720000$5c67a3dbbd901b0c6c6afe3d$Rk9t/koF6EfsxIqfbpzO7u3uT+Dmhu+oTBWgrK55QT4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-34', 'HARSH DEV SINGH THAKUR', 'pbkdf2_sha256$720000$724c68ac432ca15f26713df9$ab0tsbNRARzLMeJGYp7dglnjC6I2/BgtY1G+MLSfbSs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-35', 'HARSHIT HARDIYA', 'pbkdf2_sha256$720000$ace60e36857024b5ed50b141$nSmSrUgAR5tTTfsAs4ldgv4VIg7IqJCpKpgSjUCDdug=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-36', 'HARSHIT SONEL', 'pbkdf2_sha256$720000$a9c50d7c44812c95f2926b22$HjcMgvkiJJOhlkxd5BOHOEsm7XkYZIxSifdXEKvQa+U=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-37', 'HARSHITA SOHNER', 'pbkdf2_sha256$720000$e70d160bed865fcfc226d82a$zYxrjOk+Ofmmbl5cn4A+81rxfbPzOda+3LQYrlC3Y0o=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-38', 'HIMANSHU KANAS', 'pbkdf2_sha256$720000$69ed2fbc16855754b5873a65$SXNkOMVFgUuC01NVteSvyQ7jZApuySYELIP43U+khUQ=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-39', 'HITESH GUPTA', 'pbkdf2_sha256$720000$37cf7c2f0ab96cf28f1821c5$2+N8myO63yyxWVRuO7m5HLtq1jfUhAzu/X42ZW435qQ=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-40', 'ISHA KHAN', 'pbkdf2_sha256$720000$b3a9e73e26b5c4f3f6c343a6$ZvZqqHHEve9ThCZA9PMN9llWleYLgqZcWGT2J6sGpJ8=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-41', 'ISHA VEERWANI', 'pbkdf2_sha256$720000$2a9b417cde0a0b4fdb2b0b1f$rCvGkVwoFpGiYt7YOXOhh/LVAoinLSFNfC49GDghFsI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-42', 'ISHITA AGRAWAL', 'pbkdf2_sha256$720000$f77d1709118695471ad31cfc$U97mVEXmo2xHgKPSmLF8KU+MPlhFl+tCZQRFizVPMuc=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-43', 'JAGRATI TRIPATHI', 'pbkdf2_sha256$720000$c5d75ae63b9155069b351337$dVKSCBPRf8HUGAmvvkwbDzCWJVlJseKBZZBzFQKyg/o=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-44', 'JALAJ MEHTA', 'pbkdf2_sha256$720000$d09c81032936a73c8f97e80a$SzCvaOgk4hDDQO/Ys5gMF+bjnKmCQXOOB9hJPVsKI+U=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-45', 'JAYESH SOLANKI', 'pbkdf2_sha256$720000$dcbfff511822cbef6ce075c5$v0UZB75GwFHWH0VDeGq131qldh5HJZaHMONB7xTdjeM=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-46', 'JEET VERMA', 'pbkdf2_sha256$720000$e8417d81cd58b3c043f2868f$x7pv+wZguVNvQkhkzsimgAXFIuwMRo3VvSqsJFZB/DI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-47', 'KALPANA PATIDAR', 'pbkdf2_sha256$720000$d40e5a4e67db54b0eba0a66a$iiEQBcA5M7I9Ih8az9F0+CqrWNk3+pwNaaulvrquoaw=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-48', 'KARTIK GURJAR', 'pbkdf2_sha256$720000$b2a64e890059a52b0a3d701a$d9pG8Z3JSnlWoeRhVXEpW8eHgi0ml2+zwo4ljJYXZKs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-49', 'KASHISH NANKANI', 'pbkdf2_sha256$720000$827ccdb5e2415d2097c04d63$OIa0EpTSeb+64rvN88ELqKD4eTLyDWtI6+hvcuBfSXo=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-50', 'KESHAV SHARMA', 'pbkdf2_sha256$720000$d4ad5b4815071e185b8e63d3$GnPC/aavIm+dmVVQeFK4bRQ/w8ETzFfGFpJDj8Cbr+M=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K22-73', 'SANDEEP YADAV', 'pbkdf2_sha256$720000$feec11bf33f7dd1169224106$C3dSdTVn+RGNFcKYlh70OLuzwoYuQzjdm0icP/EYZMM=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K22-87', 'SNEHA SALVE', 'pbkdf2_sha256$720000$c996363b3ac935403007f3e3$B+S/1yX8MsI+HA9V8bGgx7tTAN5VEe7+yEP4YqwQ2Ak=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-51', 'KHUSHI DIXIT', 'pbkdf2_sha256$720000$c7ece02f41644b5f02180c82$fde2wwcodV7M+GiZQ7eY02TDuUBiZhpsXovy6YoCbqM=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-52', 'KRISHNKANT UPADHYAY', 'pbkdf2_sha256$720000$f163087d6d0f67b7eb9559f9$wNh0TZb6IsXxlOyI5zdSM/cGKhsGRwku80MoSXaKT+w=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-54', 'LALIT SOLANKI', 'pbkdf2_sha256$720000$af1d150f0dabeca6d5e1831a$fNDhF8aHamKg9kE6E1w3Bi5Sqqhfr9SvF6hvM7IypqM=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-55', 'MAHAK LODHI', 'pbkdf2_sha256$720000$529543d45c5266b82e8595e1$31RdwjO3nhJ+3l9jIG9VItJ1MXKySzQ+rbHL8uP1zoY=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-56', 'MAHIMA CHHABRA', 'pbkdf2_sha256$720000$274a02ac6ed8d8a451e929ef$iQA8D+bXUVD3br4w94fT5+3hc/gxzhcZCQlqJLP6dvY=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-57', 'MANAS PATHAK', 'pbkdf2_sha256$720000$cf819404807cc534d099298a$kLSD2mUGXh4v/ViseEiaSIAjtA5heKPHFd2jWJrm2qI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-58', 'MANTHAN SHARMA', 'pbkdf2_sha256$720000$4b7019f5c1902a7c1857b4d7$9Isn168nkyuOKf3uKouScXdSo23abCDG532mvIUD3Ek=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-60', 'NACHIKETA NAYAK', 'pbkdf2_sha256$720000$2a4d4963abc62b7ce033e326$NEUNPtMMQKc+l8Pdr2XQSx8yVzfMPBMuB5BST+r9yhA=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-61', 'NAINA RAGHUWANSHI', 'pbkdf2_sha256$720000$f6a8c5c3fc04ad450ec4e392$x657x6QrQiGO3xjr5WRFRf03v5XhZpGm7CHmFg+dBdg=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-62', 'NANDANI RATHORE', 'pbkdf2_sha256$720000$60dcacbd35929db050070d8a$zX4xFL4s7YnAWDBxWhdjyrmxCtQHq4GbkRp7zEyupro=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-63', 'NIKHIL PATEL', 'pbkdf2_sha256$720000$e56167064d48c8a7e2b1ba43$+THk5P7E5TNh3Iw3G7I9z3Bb31aglFitIqAJFKrtt+0=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-64', 'PARANJAY SHARMA', 'pbkdf2_sha256$720000$fb41bfd45b2a526ddb309f70$Fw9maeK6nboPpKBD5o661rpIRJK1Em8ZlSROtDmu9zk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-65', 'PRAGATI SIKARWAR', 'pbkdf2_sha256$720000$e9371f2072471160e481aea1$bHFNbHds1kECu+P5V+f6o3/dmq14AL5PiYnLWeyglWs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-66', 'PRAKHAR PANCHOLI', 'pbkdf2_sha256$720000$4469587de36c823265a19fde$UHOwxBJjfQKNRO/vlh+X1zHRKsIFWsr/esf8wJkEor4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-67', 'PRANEETA PATIDAR', 'pbkdf2_sha256$720000$9f9139638fa567f9fd1f68d2$irvOT+wsEx3n43VCJ73g0NMGnGZ+yL+MMhEfRIvVFOY=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-68', 'PRANJAL YADAV', 'pbkdf2_sha256$720000$4ace435aac029d59edfbb2c7$MFG2vIU9EUsYs9u046dMxGxzGYaOGiN3ozGN46KUfWk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-69', 'PRITAM SINGH RATHORE', 'pbkdf2_sha256$720000$64a5da0bb6ba5b3ccd8cbc4e$pHnwbnR+516t7a0ZJLJrmlgxWJBmye6hh5Hjt1YGHbw=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-70', 'PRIYANKA GOSWAMI', 'pbkdf2_sha256$720000$35ee7bc24ed7c2ad7443f009$3Q5eQtPk9jdUdq+AMf3Lnu+fUKzDwM6E/8TmXVCOSMY=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-71', 'RAJ GOUR', 'pbkdf2_sha256$720000$5d270051febebe7f6cc8ebea$rcpQGqXymDRl7qWVzWguseTxGybobefof17giZyxrB4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-72', 'RISHABH DULGAJ', 'pbkdf2_sha256$720000$1415549b045f8cdbefec678f$q8Bqv2CJ1P3G/3TBxEJvhPN1G/Upuy9wVxJRw6jKJIs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-73', 'ROHAN LAKHAN', 'pbkdf2_sha256$720000$55fc112d750cc9a4836074ef$Bx2jabqE4qu5ZRCSAZ/DJKGa3GsV50mSdxaiJmT3r80=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-74', 'RUDRA JAGGI', 'pbkdf2_sha256$720000$e5bc1b70fa10c5c902832db3$FbcdLnA5cudX3SkY/Sj+c8RgrSXyzxkkSA+wDisHPKs=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-75', 'RUDRA SADAWARTE', 'pbkdf2_sha256$720000$faf1bfbb12f27ec746ff8724$++XdQdrj9IQtBcNfx0UH6Xr/rM5saVrR1ZIX4hYx+tA=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-76', 'RUNNU PATIDAR', 'pbkdf2_sha256$720000$d59d21053efba064569736a4$vwx3c0cMjvStbSAI7mmGIb83gOnvXGWUMptEyeTzlVU=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-79', 'SAMBHAV SHARMA', 'pbkdf2_sha256$720000$29384ee935864573b3a1290f$EFWeWyUVTXhGtwag8ILajDkbiqno0r7jH5LHIVU7CnU=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-80', 'SHANTANU PALIWAL', 'pbkdf2_sha256$720000$771a21acb78e97741e616d06$NAe/JzJfvzhhMPPvvJ/oOSdLdToz6nbTHvCSzN9XElw=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-81', 'SHIVKANT PATEL', 'pbkdf2_sha256$720000$1d9cb6c74cc6e7e328dbe1e6$f7JC+MAC7pZzuYMh56B32eatWP3VYpWEfbsRPztzMhA=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-82', 'SHREYA PATIDAR', 'pbkdf2_sha256$720000$96048836d43676e6d9f9e5c1$++5Rv+A+mY2Lz8y0VE8Ett7ivhl5RJY5ck8Ro6OJ//E=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-83', 'SHREYANSH SHIVHARE', 'pbkdf2_sha256$720000$75a4fe6374eb84b324790ad2$pYr3E0hXPlpKL0wGRWz4g3IASU8IdlMVPCkqiZg4kEA=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-84', 'SHREYAS NAMDEO', 'pbkdf2_sha256$720000$bc73a018c408e88f726fb42c$rzAWwnvzWJtwF7Q90VbTW9syiJrNIldb3XFty1oqLE4=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-85', 'SHRIJAL KUMAR JAISWAL', 'pbkdf2_sha256$720000$137be50a775af766d65cd2a0$EryfA5bPNKsvUy4MBQQCyJ8VCK9ykxcZZRl7NxecUtc=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-86', 'SIDDHANT JAIN', 'pbkdf2_sha256$720000$4b0898e6c5c130213110093c$ReF93IZcduB+aXlowutBzUFtauwnhZFa83WBBPPBEpg=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-87', 'SNEHA SOLANKI', 'pbkdf2_sha256$720000$6afa014d4cf80e64a2bb4f82$/IQ85dZVfoHjbnuQ+R3ngfMixgSJJdDrl5nz5+cz1Vo=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-88', 'SUMIT YOGI', 'pbkdf2_sha256$720000$f178dde00b7262f160cc60d0$mGEQtSWylM9W4oV1SFdZn5hpoRdA0hYWMGqRrXd2100=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-89', 'SURUCHI KUMARI', 'pbkdf2_sha256$720000$7013320c0e320ee72e09b6cc$EUZWWVFUrRTXKzxLDeUl6aR47AlwOvW4/CS9mK/MYLI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-90', 'SUSHMEET KAUR SALUJA', 'pbkdf2_sha256$720000$47e18602843462fada929cb2$44oh4KlcYwtJuCHoC00rq1874YkXLZpPkWymCBqCKbg=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-91', 'SWASTIK SHINDE', 'pbkdf2_sha256$720000$5be345d8962f10ff7660cb26$u9vGfhn+o3S3miRIUmfXJY1y2FvqC89xejAlyYYs3Qc=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-92', 'TANISH SETHIYA', 'pbkdf2_sha256$720000$013e0484350b255a815b0696$k1m/iXBtqSPO53PrF6N18Ip8GPdb2n4LbZCzSXZmCzk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-93', 'TANISHA NAGWANI', 'pbkdf2_sha256$720000$962230d7e63acb6a181b785f$TRz7pmuOeTfM56Ol3EZwT6HJ9f4cimZo8PBAvAoA0Ys=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-94', 'TANUSHKA KAMLE', 'pbkdf2_sha256$720000$02553d0a6f3981f5e7c6f70a$MLb09lqwk86xE7eYk2eacvh4CYFt3p/8+29dY+QscwU=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-95', 'TASNEEM SAFDARI', 'pbkdf2_sha256$720000$51b782b97bc4f39d261925ad$VTUYdM5pFkGCUGf0TQRL2558r7ZZw7y1GV9ipVXAZgw=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-96', 'TUSHAR KHARADE', 'pbkdf2_sha256$720000$1d78d3d94fe9a95aec7d3e1b$ks9dSfSNGzzFP20fYZxHcAn2tlprKFmZqK7SdFADDWM=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-97', 'TUSHAR PAWAR', 'pbkdf2_sha256$720000$107907d249db5d9a71873233$w0t0V3JxyFR2ZvMIxblI299xWHvbnTq2WWPtPN/S8M8=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-98', 'UTKARSH DUBEY', 'pbkdf2_sha256$720000$cb84a2ea187cab0303926ea3$iUt3Vb9hPcNHyLCH0Ell9z+KevmteesGZYLFaVVWc0E=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-99', 'VINISHA WAGH', 'pbkdf2_sha256$720000$aeb59a7694898c5215f49729$SQ+jdMfuNYh/AyBsMdFaJteJzYONJBDdPlBRhHoYOiI=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-100', 'YASH GURJAR', 'pbkdf2_sha256$720000$e8db4ca61b7535795d74a6be$Vlv60SYcdAiGHY/Bz+/qemNMTaCy8hVduEDVMtI/n9A=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-101', 'YASH KUMAR CHOUREY', 'pbkdf2_sha256$720000$6e1a388453299ea62573eed8$r7zS1Xsr70IkfJ2VB8OzjyT2n3M3sYeE0yw0UUi+kBk=');
INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('IC-2K23-102', 'NEHA BHADKARE', 'pbkdf2_sha256$720000$ba061f9dbce6fdcc131b2eaf$rpW3AR8FPQ0nXZVMkFNSj8W4TJtJz8ioFS1tEEdkKVA=');
