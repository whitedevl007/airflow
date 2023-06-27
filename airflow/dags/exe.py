CREATE EXTERNAL TABLE hbase_table (
  `rowkey` STRING,
  `Address` STRING,
  `Age` STRING,
  `Certificates` STRING,
  `City` STRING,
  `CountryCode` STRING,
  `DOB` STRING,
  `EducationArea` STRING,
  `EducationEndDate` STRING,
  `EducationInstitution` STRING,
  `EducationScore` STRING,
  `EducationStartDate` STRING,
  `EducationStudyType` STRING,
  `Email` STRING,
  `Name` STRING,
  `Phone` STRING,
  `PostalCode` STRING,
  `Projects` STRING,
  `Softskills` STRING,
  `Techskills` STRING,
  `WorkEndDate` STRING,
  `WorkName` STRING,
  `WorkPosition` STRING,
  `WorkStartDate` STRING
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
  "hbase.columns.mapping" = ":key,column_family:Address,column_family:Age,column_family:Certificates,column_family:City,column_family:CountryCode,column_family:DOB,column_family:EducationArea,column_family:EducationEndDate,column_family:EducationInstitution,column_family:EducationScore,column_family:EducationStartDate,column_family:EducationStudyType,column_family:Email,column_family:Name,column_family:Phone,column_family:PostalCode,column_family:Projects,column_family:Softskills,column_family:Techskills,column_family:WorkEndDate,column_family:WorkName,column_family:WorkPosition,column_family:WorkStartDate"
)
TBLPROPERTIES (
  "hbase.table.name" = "personal",
  "hbase.mapred.output.outputtable" = "personal"
);
