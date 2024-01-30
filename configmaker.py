import json

data={
      "path":"c:\\santhit\\",
      "images":"c:\\santhit\\images\\",
      "main_width":"",
      "main_height":"",
      "sub_width":"",
      "sub_height":"",
      "dbname":"santhitdb",
      "host" : 'localhost',
      "user":'root',
      "pass" :'root',
      "latest_backup":"",
      "backup_time":""
      }
file_path="c:\\santhit\config.json"
d_=json.dumps(data)
with open(file_path, 'w') as file:
    file.write(d_)
    print("Successfully created configuration file")
