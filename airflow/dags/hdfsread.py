import time
import json
import happybase
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Load JSON into Hive Table") \
    .config("hive.metastore.uris", "thrift://localhost:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Connect to HBase
connection = happybase.Connection('localhost', port=9090)

def process_streaming_data(df, epochid):

    # Iterate over the rows in the DataFrame
    for row in df.rdd.collect():
        json_data = json.loads(row.value)  # Convert the JSON string to a dictionary
        row = json_data # Extract the 'resume' part from the dictionary
      
        # Get the fields from the row
        personal_info = row["Personal_info"]
        location = row["location"]
        education = row["education"]
        skills = row["skills"]
        work = row["work"]
        certificates = row["certificates"]
        projects = row["projects"]

        try:
            # Specify the table name
            table_name = "personal"
            table_personal = connection.table(table_name)

            # Generate a unique row key based on timestamp
            row_key = str(personal_info["email"])

            # Create the data dictionary for the row
            data_personal = {
                row_key.encode(): {
                    b'column_family:Name': personal_info["Name"],
                    b'column_family:Age': personal_info["Age"],
                    b'column_family:DOB': personal_info["DOB"],
                    b'column_family:Email': personal_info["email"],
                    b'column_family:Phone': personal_info["phone"],
                    b'column_family:Address': location["address"],
                    b'column_family:PostalCode': location["postalCode"],
                    b'column_family:City': location["city"],
                    b'column_family:CountryCode': location["countryCode"],
                    b'column_family:EducationArea': education["area"],
                    b'column_family:EducationStudyType': education["studyType"],
                    b'column_family:EducationInstitution': education["institution"],
                    b'column_family:EducationStartDate': education["startDate"],
                    b'column_family:EducationEndDate': education["endDate"],
                    b'column_family:EducationScore': education["score"],
                    b'column_family:Softskills': json.dumps(skills["Softskills"]),
                    b'column_family:Techskills': json.dumps(skills["Techskills"]),
                    b'column_family:WorkName': work["name"],
                    b'column_family:WorkPosition': work["position"],
                    b'column_family:WorkStartDate': work["startDate"],
                    b'column_family:WorkEndDate': work["endDate"],
                    b'column_family:Certificates': json.dumps(certificates),
                    b'column_family:Projects': json.dumps(projects)
                }
            }
         
            # Insert data into the personal table
            table_personal.put(row_key.encode(), data_personal[row_key.encode()])
            # Print the processed row
            print(f"Processed row: {row_key}")


        except Exception as e:
            print(f"Error processing row: {row_key}")
            print(str(e))
            BrokenPipeError
            pass
            KeyError
            pass

# Create a streaming DataFrame by monitoring the directory
streaming_personal = spark.readStream.format("text").load("hdfs://localhost:9000/usercontextata/**/*.json")

# Apply the processing function to the streaming DataFrame
streaming_query_per = streaming_personal.writeStream.foreachBatch(process_streaming_data).start()

# Wait for the streaming query to terminate
streaming_query_per.awaitTermination()
