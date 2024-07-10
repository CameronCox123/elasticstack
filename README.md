# This repo contains information reguarding elasticsearch and the elasticstack when running on your local machine
In order to properly utilize the resources provided here you'll need to download elasticsearch, logstash, and kibana.
You can find these online at the elasticsearch website. 

Elasticsearch: https://www.elastic.co/elasticsearch

Kibana: https://www.elastic.co/kibana

Logstash: https://www.elastic.co/logstash

Additionally, you may want to download curl, a cli tool, which interacts with the elasticstack: https://curl.se/windows/
```
WARNING!!!
THIS DOCUMENT IS INTENDED FOR WINDOWS, COMMANDS HAVE ONLY BEEN TESTED ON WINDOWS COMMAND PROMPT, BE AWARE
```

# To upload a log to elasticsearch via logstash:
  - create a file in your logstash\config folder named logstash.conf
  - configure logstash.conf
  - open the terminal
  - ```cd C:/path/to/logstash/bin```
  - ```logstash -f C:\path\to\logstash\config\logstash.conf```  <- _Make sure you use backslashes, forwardslashes can be seen as 'end line' characters_

 **Depending on what you want to upload, you will have to configure your logstash.conf file differently. There is an example logstash.conf file located in this repo which is designed for Azure DevOps build logs.**

# Curl Commands to interact with Elasticsearch

## Before you run any curl commands:
  Make sure you are in the proper folder in your terminal
  ```cd C:/path/to/curl```
  Make sure elasticsearch is up and running. You can navigate 
  ```cd C:/path/to/elasticsearch/bin```
  and run
  ```elasticsearch.bat```

  **Depending on your system setup, in order to interact with elasticsearch you will need to configure the .yml file. Go to elasticsearch/config/elasticsearch.yml and change the ```xpack.security.enabled``` to ```false```**

  

* ### To create a new index in your local elasticsearch session:
	```curl -XPUT http://localhost:9200/[index-name-here]?pretty"``` <- _if necessary you can remove the ?pretty, it's only here for formatting_
* ### To delete an index:
	```curl -XDELETE http://localhost:9200/[index-name-here]?pretty```
* ### To view all of your indecies:
	```curl -XGET http://localhost:9200/_cat/indices```
* ### To view the contents of the whole index: 
	```curl -XGET "http://localhost:9200/[index-name-here]/_search?size=1000&pretty"```<- _size value is number of documents displayed_
* ### To upload a single document using curl, first make sure your file is in a json format and only has one json object, then call:
	```curl -XPOST http://localhost:9200/[index-name-here]/_doc?pretty -H "Content-Type: application/json" -d @C:/path/to/file.json```
```
WARNING!!!
UPLOADING DOCUMENTS WITH CURL IS VERY INCONSISTENT, IT'S HIGHLY RECCOMENDED THAT YOU USE THE LOGSTASH METHOD LOCATED ABOVE. IF YOU NEED TO USE THE CURL METHOD, MAKE SURE IT'S IN A JSON FORMAT. FOR AZURE DEVOPS BUILD LOGS THERE IS A PROVIDED FORMATTING PROGRAM NAMED bulk-conversion.py IN THIS REPO THAT WILL CHANGE TAKE THE LOGS AND FORMAT THEM FOR .JSON
```

You don't need to create a new index before uploading a document. It'll do it for you.
To upload multiple documents, format it like so in example file.json:

{"index": {"_index": "temp-index", "_id": "1"}}
{"log_entry": "2024-06-10T20:13:00.7932357Z ##[section]Starting: Job"}
{"index": {"_index": "temp-index", "_id": "2"}}
{"log_entry": "2024-06-10T20:13:01.0040784Z ##[section]Starting: Initialize job"}
{"index": {"_index": "temp-index", "_id": "3"}}

  Then call:
	curl -XPOST http://localhost:9200/[index-name-here]/_bulk?pretty --data-binary @C:/path/to/file.json -H "Content-Type: application/json"

### To search each document in an index, replace [field 1] and [field 2] (make sure to remove the brackets but keep all other formatting) and replace them with your search terms
	curl -XGET "http://localhost:9200/[index-name-here]/_search?pretty" -H "Content-Type: application/json" -d"{\"query\":{\"match\":{\"[field 1]\":\"[field 2]\"}}}"
	
	Example return:       
       {
        "_index" : "bulk-index",
        "_id" : "43",
        "_score" : 4.0176864,
        "_source" : {
          "log_entry" : "2024-06-10T20:13:04.1486660Z Finished checking job knob settings."
        }

To use curl to upload the log files:
	Download the log file from a completed build on Dev-ops
	Get the BIG log file that contains everything 
	Run through text-to-json conversion
