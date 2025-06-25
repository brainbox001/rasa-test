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
        
class ValidateRechargeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recharge_form"

    def validate_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate and convert amount slot value."""
    
        cleaned_value_str = str(slot_value).lower().strip()

        amount = None

        # Handle 'k' notation (e.g., 1k -> 1000, 2.5k -> 2500) 

        if cleaned_value_str.endswith('k'):
            try:
                numeric_part_str = cleaned_value_str[:-1]
                amount = float(numeric_part_str) * 1000
            except ValueError:
                dispatcher.utter_message(text="I couldn't understand the 'k' amount. Please enter a valid number or use standard 'k' notation (e.g., '1k', '2.5k').")
                return {"amount": None}

        # Handle currency symbols #
        elif cleaned_value_str.startswith(('#')): # Check for any of the prefixes
        
            amount_str_without_symbol = cleaned_value_str[1:]

            try:
                amount = float(amount_str_without_symbol)
            except ValueError:
                dispatcher.utter_message(text="I couldn't process that amount format. Please enter a valid number (e.g., 500, #500).")
                return {"amount": None}

        # Handle pure numbers (e.g., "500", "2000")
        else:
            try:
                amount = float(cleaned_value_str)
            except ValueError:
                dispatcher.utter_message(text="That's not a valid amount. Please enter a number (e.g., 500, 1000, 2k, #500).")
                return {"amount": None}


        # 5. Final validation (e.g., positive value)
        if amount is not None and amount > 0:
            return {"amount": amount}
        else:
            dispatcher.utter_message(text="The recharge amount must be a positive number. Please try again.")
            return {"amount": None}
    
# class Action(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
