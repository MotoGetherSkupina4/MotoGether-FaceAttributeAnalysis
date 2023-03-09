from pymongo import MongoClient
import bson.binary, io, os
from PIL import Image
from deepface import DeepFace
import random
import shutil


###################################################
# WEIGHTS
###################################################

CUSTOM_WEIGHTS = {
    "age": {
        "type": "percentage", "value": 1,
    },
    "gender": {
        "type": "percentage", "value": 0.2,
    },
    "race": {
        "type": "numerical", "value": 40,
    },
    "name": {
        "type": "numerical", "value": 10,
    },
    "surname": {
        "type": "numerical", "value": 30,
    },
    "emotion_angry": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_disgust": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_fear": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_happy": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_sad": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_surprise": {
        "type": "percentage", "value": 0.1,
    },
    "emotion_neutral": {
        "type": "percentage", "value": 0.1,
    },
}



###################################################
# User class
###################################################

class User:
    def __init__(self, _id, name, surname):
        self._id = _id
        self.name = name
        self.surname = surname
    
    def addFacialAnalysis(self, facial_analysis):
        self.age = facial_analysis['age']
        self.gender = round(facial_analysis['gender']['Man'], 2)
        self.race = facial_analysis['dominant_race']
        self.emotion_angry = round(facial_analysis['emotion']['angry'], 2)
        self.emotion_disgust = round(facial_analysis['emotion']['disgust'], 2)
        self.emotion_fear = round(facial_analysis['emotion']['fear'], 2)
        self.emotion_happy = round(facial_analysis['emotion']['happy'], 2)
        self.emotion_sad = round(facial_analysis['emotion']['sad'], 2)
        self.emotion_surprise = round(facial_analysis['emotion']['surprise'], 2)
        self.emotion_neutral = round(facial_analysis['emotion']['neutral'], 2)

    def __repr__(self):
        if hasattr(self, 'age'):
            return f'{self.name} {self.surname} -> gender: {self.gender}, age: {self.age}, gender: {self.gender}, race: {self.race}, \n\t Emotions: {self.emotion_angry}, {self.emotion_disgust}, {self.emotion_fear}, {self.emotion_happy}, {self.emotion_sad}, {self.emotion_surprise}, {self.emotion_neutral}'
        else:
            return f'{self.name} {self.surname}'
        


###################################################
# Friends class
###################################################

class Friends:
    def __init__(self, me, users):
        self.my_friends = []
        self.me = me
        self.my_id = me._id
        for user in users:
            if self.my_id == user._id:
                continue
            score = 0
            for key in CUSTOM_WEIGHTS:
                if hasattr(user, key) and hasattr(me, key):
                    if CUSTOM_WEIGHTS[key]['type'] == 'percentage':
                        score += CUSTOM_WEIGHTS[key]['value'] * abs(getattr(me, key) - getattr(user, key))
                    elif CUSTOM_WEIGHTS[key]['type'] == 'numerical' and getattr(me, key) == getattr(user, key):
                        score += CUSTOM_WEIGHTS[key]['value']
            self.my_friends.append({
                '_id': user._id,
                'score': score
            })
    def friendList(self):
        sorted_list = sorted(
            self.my_friends,
            key=lambda x: (x['score'], random.random()), 
            reverse=True
        )
        return sorted_list[:SUGGESTED_FRIENDS]



###################################################
# Other const variables
###################################################

SUGGESTED_FRIENDS = 5



###################################################
# Database connection
###################################################

client=MongoClient()
# client = MongoClient("mongodb+srv://admin:iQJWIWRFjAgKgeTT@cluster0.zlyharb.mongodb.net/test")
# mydb = client["motogether"]
# mycol = mydb["tests"]
client = MongoClient("mongodb+srv://alex:xlV5f2i4Dopswu7i@cluster0.ars4n.mongodb.net/test")
mydb = client["test"]
mycol = mydb["users"]

mydoc = mycol.find({})



###################################################
# Temporary folder creating
###################################################

image_export_directory = './tmp/'
if not os.path.exists(image_export_directory):
    os.makedirs(image_export_directory)
    print("Directory created successfully")
else:
    print("Directory already exists")



###################################################
# Find friends
###################################################

mydoc = mycol.find()
userData = []

for user in mydoc:
    userData.append(User(user['_id'], user['name'], user['surname']))
    if user and 'avatar' in user:
        print("[{}]: User has avatar image!".format(user['username']))
        image_data = bson.binary.Binary(user['avatar'])
        img = Image.open(io.BytesIO(image_data))
        image_file_path = image_export_directory + 'user_' + str(user['_id']) + '.jpg'
        img.save(image_file_path)
        try:
            demography = DeepFace.analyze(image_file_path)[0]
            userData[-1].addFacialAnalysis(demography)
        except:
            print("[{}]: User image doesn't contains a face".format(user['username']))
    else:
        print("[{}]: User doens't have avatar image".format(user['username']))



###################################################
# Show results and save to database
###################################################

for user in userData:
    friends = Friends(user, userData)
    possible_friends = [obj['_id'] for obj in friends.friendList()]
    result = mycol.update_one(
        {'_id': user._id},
        {'$set': {'possible_friends': possible_friends}}
    )



###################################################
# Remove tmp folder
###################################################

shutil.rmtree(image_export_directory)

if not os.path.exists(image_export_directory):
    print('Temporary folder removed successfully.')
else:
    print('Error: temporary folder still exists.')