 # This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import UserUttered
from typing import Any, Text, Dict, List
import os
import math
import random
import smtplib
#from googlesearch import search
from serpapi import GoogleSearch

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import _csv
from csv import writer


#
# class ActionSearchStack(Action):
#
#     def name(self) -> Text:
#         return "action_search_stack"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         #question = tracker.latest_message
#
#         #dispatcher.utter_message(text="Could you please rephrase?")
#
#         question = tracker.latest_message['text']
#
#         #question = tracker.get_slot("first_question")
#         #dispatcher.utter_message(text="Hello World!")
#         print("latest Question is ",question)
#         return []
#
#
#
#
#
# class ActionDefaultFallbackQuestion(Action):
#     """Executes the fallback action and goes back to the previous state
#     of the dialogue"""
#
#     def name(self) -> Text:
#         return "ACTION_DEFAULT_FALLBACK_Question"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="my_custom_fallback_template")
#
#         UserUtteranceReverted()
#
#         question = tracker.latest_message['text']

        #question = tracker.get_slot("first_question")
        #dispatcher.utter_message(text="Hello World!")
        # print("latest Question is from custom  ",question)
        # # Revert user message which led to fallback.
        # return [UserUtteranceReverted()]

OTP = ""
verified = False
class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_mail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emailid = tracker.latest_message['text']
        digits = "0123456789"
        global OTP
        OTP =""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        otp = OTP + " is your OTP"
        msg = otp

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("sakar.salunke74@gmail.com", "wgcmjvqalwgaxznz")
        #emailid = input("Enter your email: ")
        s.sendmail('&&&&&&&&&&&', emailid, msg)
        dispatcher.utter_message(text=f" I have sent you OTP, please tell me,\nI'll remember your mail {emailid}!")
        return [SlotSet("mail", emailid)]


class ActionVerifyOTP(Action):

    def name(self) -> Text:
        return "action_verify_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userotp = tracker.latest_message['text']
        print("OTP is",OTP)
        global verified
        if userotp == OTP:
            print("Verified")
            verified = True
            dispatcher.utter_message(text=f" You are verified ")
        else:
            verified = False
            print("Please Check your OTP again")
            dispatcher.utter_message(text="Please check your OTP again")
            return [SlotSet("mail", None)]

        return []


class ActionSayMail(Action):

    def name(self) -> Text:
        return "action_say_mail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mail = tracker.get_slot("mail")
        if not mail:
            dispatcher.utter_message(text="I don't know your mail.")
        else:
            dispatcher.utter_message(text=f"Your email id is {mail}!")
        return []

class Actionsubscribe(Action):

    def name(self) -> Text:
        return "action_subscribe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #entities = tracker.latest_message['entities']
        #print("Entities", entities)
        email_phone = tracker.latest_message['text']
        #email_phone = str(entities[0]['value'])
        #name1 = "enter your name"
        #email = "enter your email"
        #phone = input("enter your phone number")
        #dispatcher.utter_message(text=name1)
        #name = input()
        #dispatcher.utter_message(text=email)
        #email = input()
        print(email_phone)
        details = email_phone.split(",")
        #details = [name, email]

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open('event.csv', 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(details)

            # Close the file object
            f_object.close()
        dispatcher.utter_message(text=f"You are Subscribed!")



class ActionKnowPerformance(Action):

    def name(self) -> Text:
        return "action_know_performance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mail = tracker.get_slot("mail")
        print(mail)
        if not mail:
            dispatcher.utter_message(text="I don't know your mail. Please tell me your email id")
        else:
            global verified
            if verified:    
                with open('Copy of Grades CS 101_ Spring 2021  03-07-2022 - Sheet0.csv',
                          'r') as file:
                    reader = list(_csv.reader(file))
                print("inside action")
                found_no = False
                total_Quiz1 = 10
                total_Quiz2 = 10
                total_lab1 = 10
                total_lab2 = 10

                for row in reader:
                    # Check for the user input
                    if mail in row[2]:
                        name = "Dear " + str(row[1]) + " " + str(row[0]) + "\n"
                        heading = "\n Your current progress as follows : \n"
                        Quiz1 = "\nQuiz1 : " + str(row[7]) + "/" + str(total_Quiz1) + "\n"
                        Quiz2 = "Quiz2 : " + str(row[8]) + "/" + str(total_Quiz2) + "\n"
                        lab1 = "lab1 : " + str(row[9]) + "/" + str(total_lab1) + "\n"
                        lab2 = "lab2 : " + str(row[10]) + "/" + str(total_lab2) + "\n"
                        rank = "your rank in the class till today is " + str(row[12]) + "\n"
                        mssg = name + heading + Quiz1 + Quiz2 + lab1 + lab2 + rank
                        dispatcher.utter_message(text=mssg)
                        found_no = True
                        break;
                if not found_no:
                    message1 = "Email Not found"
                    dispatcher.utter_message(text=message1)
            else:
                dispatcher.utter_message(text=f"You are not verified! \n Please verify yourself tell me your email")
        return []


class ActionSearchStack(Action):

    def name(self) -> Text:
        return "action_search_stack"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]] :

        # evt = UserUtteranceReverted()
        # evt2 = UserUttered(text='hiya')
        # text2 = tracker.last_executed_action_has(name='what')
        # text = tracker.latest_message['text']
        # print(text)
        # print(evt)
        # print(evt2)
        # print(text2)
        # dispatcher.utter_message(text=f"I'll remember your Qn {text}!")
        print("\033[92m Events\033[0m")
        mssg1 = "Ohh Sorry ! Let me search again "
        dispatcher.utter_message(text=mssg1)

        user = 1
        for event in reversed(tracker.events):
            if event['event'] == 'user':
                user += 1
                if user == 3:
                    #print(str(a) + '. ' + str(event))
                    print("=========================================")
                    print(event['event']+" "+event['text'])
                    question = event['text']
                    print("question is", question)
                    print("=========================================")
                    break

        #query = "List vs tuple difference"
        ##one solution
        # question = question.replace(" ", "+")
        # # Generating the url
        # # url = "https://google.com/search?q=weather+in+" + city
        # url = "https://stackoverflow.com/search?q=" + str(question)
        # url = str(url)
        # message = "Look what I found \n" + url
        # dispatcher.utter_message(text=message)
        # print(url)
        ###end of one solution
        # print("\033[92m Applied Events\033[0m")
        # a = 1
        # for event in reversed(tracker.applied_events()):
        #     if event['event'] == 'user':
        #         #print(str(a) + '. ' + str(event))
        #         print("================================================")
        #         print(event['event']+" "+event['text'])
        #         print("=========================================")
        #
        #     a += 1
        #     if a > 10:
        #         break
        #
        ##second solution

        params = {
            "api_key": "5156d3d432cf5fd37c4527b126a1e51b0f21df7deebb8fedecaa47bfc749161e",
            "engine": "google",
            "q": question,
            "location": "Austin, Texas, United States",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en"
        }

        search1 = GoogleSearch(params)
        results = search1.get_dict()
        print(results)

        mssg = results['answer_box']['title']

        # mssg = mssg + "\n More references \n "
        #
        # for j in search(question, tld="co.in", num=2, stop=2, pause=3):
        #     mssg = mssg + "\n j \n"
        #     print(j)
        print(mssg)
        dispatcher.utter_message(text=mssg)

        return []



