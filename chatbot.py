# Name :- Rishav Gupta
# University Roll No :- 2013450

from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pandas as pd


# Importing the dataset
dataset = pd.read_csv('student_dataset.csv', sep=',', encoding='utf8')


r_reg=dataset['RegNo']
r_name=dataset['Name']
r_sex=dataset['Sex']
r_age=dataset['Age']
r_marks=dataset['Marks']
r_mob=dataset['MobNo']


bot = ChatBot(
    'Example Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.50
        }
    ]
)

lowest_name = ''
lowest_regno = ''
topper_name = ''
topper_regno = ''
no_of_failures = 0
failures = ''
no_of_people_90 = 0

for i in range(0,len(r_reg)):
    if r_marks[i] == min(r_marks):
        lowest_name = r_name[i]
        lowest_regno = r_reg[i]
        
    if r_marks[i] == max(r_marks):
        topper_name = r_name[i]
        topper_regno = r_reg[i]
    
    if r_marks[i] < 40:
        no_of_failures = no_of_failures + 1
        failures = failures + ', '+ r_name[i] +' (' +str(r_reg[i]) +')'
        
    if r_marks[i] >= 90:
        no_of_people_90 = no_of_people_90 + 1

    
trainer = ListTrainer(bot)
for i in range(0,len(r_reg)):
    trainer.train([
        'Give me details of {}'.format(r_reg[i]),
        'Details are : Name: {} Sex: {} Age: {} Mob: {}'.format(r_name[i],r_sex[i],r_age[i],r_mob[i])
    ])
    trainer.train([
        'Give me details of {}'.format(r_name[i]),
        'Details are : Reg No.: {} Sex: {} Age: {} Mob: {}'.format(r_reg[i],r_sex[i],r_age[i],r_mob[i])
    ])
    trainer.train([
        'What is the marks of {}'.format(r_name[i]),
        'Marks : {}'.format(r_marks[i])
    ])
    trainer.train([
        'What is the age of {}'.format(r_name[i]),
        'Age : {}'.format(r_age[i])
    ])
    trainer.train([
        'What is the mobile no of {}'.format(r_name[i]),
        'Mobile No. : {}'.format(r_mob[i])
    ])
    
trainer.train([
    'what is the class average?',
    'The class average is {}'.format(sum(r_marks)/len(r_marks))
])
trainer.train([
    'what is the lowest marks?',
    'The Lowest marks is {}'.format(min(r_marks))
])
trainer.train([
    'what is the highest marks?',
    'The highest marks is {}'.format(max(r_marks))
    ])
trainer.train([
    'how many failures?',
    'These many guys got below 40 {}'.format(no_of_failures)
    ])
    
corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

chatbot = Flask(__name__)

@chatbot.route('/')
def home():
    return render_template("home.html")

@chatbot.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))

if __name__ == "__main__":
    chatbot.run(debug=True)

