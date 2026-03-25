CREATE TABLE klienty (
  nomer_zakaza INTEGER   NOT NULL ,
  id_produkcii INTEGER    ,
  familiya VARCHAR(50)    ,
  imya VARCHAR(50)    ,
  otchestvo VARCHAR(50)    ,
  adress VARCHAR(150)    ,
  gorod VARCHAR(50)    ,
  data_zakaza DATE      ,
PRIMARY KEY(nomer_zakaza));




CREATE TABLE mebel_garnityu (
  id_produkcii INTEGER   NOT NULL ,
  klienty_nomer_zakaza INTEGER   NOT NULL ,
  nazvanie VARCHAR(100)    ,
  tip_garnityra VARCHAR(20)    ,
  strana_proiz VARCHAR(50)    ,
  kolichestvo INTEGER    ,
  material VARCHAR(50)    ,
  obivka VARCHAR(50)    ,
  cena DECIMAL(10, 2)      ,
PRIMARY KEY(id_produkcii)  ,
  FOREIGN KEY(klienty_nomer_zakaza)
    REFERENCES klienty(nomer_zakaza));


CREATE INDEX mebel_garnityu_FKIndex1 ON mebel_garnityu (klienty_nomer_zakaza);


CREATE INDEX IFK_Rel_01 ON mebel_garnityu (klienty_nomer_zakaza);



