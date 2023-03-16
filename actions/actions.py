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
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset, Form, SlotSet, FollowupAction, Restarted
import os
import pandas as pd
import sys
import numpy as np
from fuzzywuzzy import fuzz

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


# Path to the custom scripts folder
sys.path.append(os.path.join(os.getcwd(), 'custom_scripts'))
from exceltodict import read_excel, return_matching_names, return_matching_names_from_dept

def fuzzy_match_keywords(keywords, input_str, threshold=70):
    """
    Performs a fuzzy match of keywords in a list against an input string,
    and returns a list of matching keywords that meet a specified threshold.

    Parameters:
        keywords (list): A list of keywords to match against.
        input_str (str): The input string to match against the keywords.
        threshold (int): The minimum fuzzy match score required to consider a match.
                          Default is 70.

    Returns:
        List of matching keywords that meet the specified threshold.
    """
    matches = []
    for keyword in keywords:
        match_score = fuzz.partial_ratio(input_str.lower(), keyword.lower())
        if match_score >= threshold:
            matches.append(keyword)
    return matches


file_path = 'data/listado.xlsx'


class retreiveFacultyDetails(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_return_general_info_person"
        # Can you give me all the details about JORGE
    
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
                    return [SlotSet("slot_person_names", return_matched_names), FollowupAction('action_choose_person_name')]
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

class retreiveDeptDetails(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_return_department_info_person"
        # Can you give me all the details about JORGE
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
           
            print("Inside retreiveDeptDetails")
            personName = next(tracker.get_latest_entity_values("person_names"), None)
            print(f'person_names entity value: {personName}')
            # get the names name from the slot
            slot_name = tracker.get_slot('slot_person_names')
            print(f'slot_name entity value: {slot_name}')

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
                        name= df[df.columns[0]].values[indexes][0]
                        department= df[df.columns[1]].values[indexes][0]
                        office_num = df[df.columns[2]].values[indexes][0]
                        print(department)
                        print(office_num)
                  
                        dispatcher.utter_message(name +' belongs to the department of : ' + str(department))
                        return []

                elif bool(len(indexes) > 1):
                    dispatcher.utter_message('I have found more than one person with the name ' + personName)
                    return [SlotSet("slot_person_names", return_matched_names), FollowupAction('action_choose_person_name')]
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

class retreiveOfficeDetails(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_return_office_info_person"
        # Can you give me all the details about JORGE
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
           
            print("Inside retreiveOfficeDetails")
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
                   
                        office_num = df[df.columns[2]].values[indexes][0]
                        print(office_num)
                  
                        dispatcher.utter_message(personName +' sits in the office number: ' + str(office_num))
                        return []

                elif bool(len(indexes) > 1):
                    dispatcher.utter_message('I have found more than one person with the name ' + personName)
                    return [SlotSet("slot_person_names", return_matched_names), FollowupAction('action_choose_person_name')]
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


class choosePersonNameFromMultipleOptions(Action):
    def name(self) -> Text:
        return "action_choose_person_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the names list set by action one
        names = tracker.get_slot("slot_person_names")
        print('choosePersonNameFromMultipleOptions')

        # Get the latest user message
        latest_message = tracker.latest_message
        # print('latest_message', latest_message)
        last_intent = latest_message['intent']['name']
        print('last intent is: ', last_intent)

        # Get the intent that triggered the follow-up action
        # triggering_intent = latest_message.intent.get("name")
        # print('triggering_intent', triggering_intent)

        # create a list of buttons with the names as options
        buttons = []
        for name in names:
            #buttons.append({"title": name, "payload": '/action_return_department_info_person{"person_names": "'+name+'"}'})
            
            #buttons.append({"title": name, "payload": '/ask_department_details_person{{"name":"'+name+'"}}'})
            #buttons.append({"title": name, "payload": '/'+last_intent})
            buttons.append({"title": name, "payload": name})
            # buttons.append({"title": name, "payload": '/'+last_intent+' {"slot_person_names": "'+name+'"}'})

        # display the buttons to the user
        message = "Please choose the name of the person you want to get information of:"
        dispatcher.utter_message(text=message, buttons=buttons)

        selected_name = tracker.get_slot("slot_person_names")
        print('selected_name', selected_name)

        return []


class retreiveNamesBasedOnDepartment(Action):
    #1. Define the name of the action. This will be used in the stories , domain and in the endpoint.yml
    def name(self) -> Text:
        return "action_get_names_from_dept"
        # Can you give me all the details about JORGE
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
           
            print("Inside retreiveNamesBasedOnDepartment")
            departmentName = next(tracker.get_latest_entity_values("department_names"), None)
            print(f'departmentName entity value: {departmentName}')
  

            if(departmentName is None):
                dispatcher.utter_message("I couldn't recognize who you department you are looking for. Can you please try again?")
                return []

            try:
                df = read_excel(file_path = file_path)
                departments = list(set(df[df.columns[1]].values.astype(str)))
                # print('departments', departments)

                return_matched_names = fuzzy_match_keywords(departments, departmentName)
                print('return_matched_names', return_matched_names)

                print(departmentName in df[df.columns[1]].values  == True)

                # if bool(len(indexes) == 1): #check if the person name is present in the excel sheet on first column
                #     # return index where personName is present in return_matched_names numpy array
                #         name= df[df.columns[0]].values[indexes][0]
                #         department= df[df.columns[1]].values[indexes][0]
                #         office_num = df[df.columns[2]].values[indexes][0]
                #         print(department)
                #         print(office_num)
                  
                #         dispatcher.utter_message(name +' belongs to the department of : ' + str(department))
                #         return []

                # elif bool(len(indexes) > 1):
                #     dispatcher.utter_message('I have found more than one person with the name ' + personName)
                #     return [SlotSet("slot_person_names", return_matched_names), FollowupAction('action_choose_person_name')]
                # else:
                #     raise Exception('Person not found in database')
    
            except Exception as e:
                print('error while retreiving names from dept: ',e)
                dispatcher.utter_message("I'm sorry, there was an error while fetching from my records!")
                return []
       
        except Exception as e:
            print('error while retreiving names from dept',e)
            dispatcher.utter_message("I'm sorry, I am facing trouble fetching information right now. Please try after sometime!")
            return ['']
