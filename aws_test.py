import json

import boto3

session = boto3.Session(profile_name='caio-aws')
s3 = session.client('s3')

json_data = {
    'teste': 'sadadwd',
    'teste2': 'asdasd'
}
# s3.Object('monica-ia', 'constants.json').put(Body=json.dumps(json_data))

constants_json = s3.get_object(Bucket='monica-ia', Key='constants.json').put(json.dumps(json_data))
constants = constants_json['Body'].read().decode('utf-8')

print("printing s3_clientdata")
print(constants)
print(type(constants))


s3clientlist=json.loads(constants)
print("json loaded data")
print(s3clientlist)
print(type(s3clientlist))

#print(s3clientlist[0]['clientName'])

loclientdict=next(item for item in s3clientlist if item["clientID"] == "22oi5qjafaflklkjklajlf")
print(loclientdict)
group=loclientdict.get('group')
print(group)