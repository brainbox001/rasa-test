# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# print("Firebase Admin SDK initialized successfully!")

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

CORRECT_PASSWORD = "1234"


class ActionResetPin(Action):
    def name(self):
        return "action_reset_pin"

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_message("Pin has been reset. Please enter a new pin.")
        return [SlotSet("pin", None), SlotSet("pin_verified", False)]
    

class ActionResetRechargeForm(Action):
    def name(self):
        return "action_reset_recharge_form"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("amount", None),
            SlotSet("network", None),
            SlotSet("phone_number", None),
        ]
    

class ValidateRechargePinForm(FormValidationAction):
    """Custom action to validate recharge pin form input."""

    def name(self) -> Text:
        return "validate_recharge_pin_form"

    def validate_pin(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if slot_value == CORRECT_PASSWORD:
            dispatcher.utter_message(text="Pin accepted.")
            return {"pin": slot_value, "pin_verified": True, "pin_attempts": 0}

        # optional retry tracking
        attempts = tracker.get_slot("pin_attempts") or 0
        attempts += 1

        if attempts >= 3:
            dispatcher.utter_message(text="Too many failed attempts. Try again later.")
            return {
                "pin": None,
                "pin_attempts": 0,
                "requested_slot": None,
                "active_loop": None
            }
        
        elif attempts > 0:
            dispatcher.utter_message("Incorrect pin. Try again.")
            return {"pin": None, "pin_attempts": attempts}
    
# class Action(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
