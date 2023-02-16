# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


#This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import arrow
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import pandas as pd
import sys
import numpy as np


sys.path.append(os.path.dirname(os.path.realpath(__file__)))


# Path to the custom scripts folder
sys.path.append(os.path.join(os.getcwd(), 'custom_scripts'))
from exceltodict import read_excel, return_matching_names

file_path = 'data/listado.xlsx'



city_db = {
    "amsterdam": "Europe/Amsterdam",
    "seattle": "US/Pacific",
}


class ActionTellTime(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_tell_time"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = f"The time is {utc.format('HH:mm')} now. You can also give me a place"
            dispatcher.utter_message(msg)
            return []

        tz_string  = city_db.get(current_place.lower(), None)
        if not tz_string:
            msg = "I don't know the timezone of {}. Is it spelled correctly?".format(current_place)
            dispatcher.utter_message(msg)
            return []

        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(msg)
        return []

class LookupName(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_lookup_name"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #  CollectingDispatcher is a class that helps you send messages back to the user
        #  Tracker is a class that keeps track of the conversation. It can be used to access slots, the latest message, and intents and entities 
        #  3rd argument is a dictionary that contains the domain of the assistant
        message = tracker.latest_message.get("text")
        name = re.search(r"my name is (\w+)", message)
        if name:
            name = name.group(1)
        else:
            name = "there"
        
        greeting = "Hello, " + name + "!"
        dispatcher.utter_message(greeting)
        name = tracker.get_slot("name")
        greeting = "Hello, " + name + "!"
        dispatcher.utter_message(greeting)

class retreiveFacultyDetails(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_return_general_info_person"
        # Can you give me all the details about Jorge Lobo
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
           
            print("Inside retreiveFacultyDetails")
            personName = next(tracker.get_latest_entity_values("person_names"), None)
            print(f'person_names entity value: {personName}')

            if(personName is None):
                dispatcher.utter_message("I couldn't recognize who you are looking for. Can you please try with their full name?")
                return []

            try:
                df = read_excel(file_path = file_path)
                names = df[df.columns[0]].values.astype(str)
                indexes, return_matched_names = return_matching_names(personName, names)
                print(indexes)
                print(return_matched_names)

                # print(personName in df[df.columns[0]].values  == True)

                if bool(len(indexes) == 1): #check if the person name is present in the excel sheet on first column
                    # return index where personName is present in return_matched_names numpy array
                       
                        department= df[df.columns[1]].values[indexes][0]
                        office_num = df[df.columns[2]].values[indexes][0]
                        print(department)
                        print(office_num)
                  
                        dispatcher.utter_message('I have found the following details for you about ' + personName +'./n'
                        + 'Department: ' + str(department) + '/n' + 'Office Number: ' + str(office_num))
                        return []

                elif bool(len(indexes) > 1):
                    dispatcher.utter_message('I have found more than one person with the name ' + personName + '. Please be more specific.')
                    return []
                else:
                    raise Exception('Person not found in database')
    
            except Exception as e:
                print('error while reading excel: ',e)
                dispatcher.utter_message("I'm sorry, there was an error while fetching from my records!")
                return []
       
        except Exception as e:
            print('error while reading excel',e)
            dispatcher.utter_message("I'm sorry, I am facing trouble fetching information right now. Please try after sometime!")
            return ['']


        def validate_circuit(
                self,
                slot_value: Any,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: DomainDict,
            ) -> Dict[Text, Any]:
                """Validate circuit value."""
                # if the name is super short, it might be wrong
                print(f"Circuit name given = {slot_value} length = {len(slot_value)}")
                if len(slot_value) <= 3:
                    dispatcher.utter_message(text=f"That's a very short circuit name. I'm assuming you mis-spelled.")
                    return {"circuit": None}
                else:
                    print('Circuit: ' + slot_value)
                    return {"circuit": slot_value}