from confluent_kafka import Producer
import json

def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                if "=" in line:
                    parameter, value = line.strip().split('=', 1)
                    conf[parameter] = value.strip()
        return conf
    


props = read_ccloud_config("client.properties")

producer = Producer(props)
topic = "Test"


data={
  "Personal_info": {
      "name": "John mathew",
	"Age":"34",
	"DOB": "19-11-1989",
      "email": "john@gmail.com",
      "phone": "(91)7869569810"
	},

   "location": {
      "address": "21734 broadway st",
      "postalCode": "CA 94115",
      "city": "Delhi",
      "countryCode": "IN"
    },

   "education":{
	"area": "Software Development",
      "studyType": "Bachelor",
      "institution": "University",
      "startDate": "04-06-2009",
      "endDate": "03-05-2013",
      "score": "4.0"
       },

   "skills":{

       "Softskills":[{
             "Englishspeaking":"50%",
		 "Englishwriting":"70%",
		 "Leadership":"90%"
			}],

	"Techskills":[{"python":"3"},
			  {"Hadoop":"5"},
			  {"HTML":"2"},
			  {"Nodejs":"4"},
			  {"Angular":"3"}
			]
		},

    "interests": ["Reading","Travelling"],

    "work": {
       "name": "Company",
       "position": "Developer",
       "startDate": "13-05-2014",
       "endDate": "20-05-2020"
       },
 
   "certificates": [{
      "name": "Experiencecertificate",
      "date": "06-07-2020",
      "issuer": "Company"
      }],
  
  "projects": [{
    	"name": "Project",
    	"description": "Description…",
    	"role": "Team Lead"
	}]
      
}


value = json.dumps(data).encode('utf-8')  # Convert data to JSON string and encode as bytes
producer.produce(topic, value=value)
producer.flush()  # Wait for the message to be delivered
print("Message produced successfully")
