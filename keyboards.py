from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove


def main_options_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "Welfare Events", callback_data='welfare_events')],
        [InlineKeyboardButton("Provide Feedback", callback_data='feedback')],
        [InlineKeyboardButton("Account Settings", callback_data='settings')]
    ]
    return InlineKeyboardMarkup(keyboard)


def house_keyboard():
    keyboard = [
        [KeyboardButton("Aquila")],
        [KeyboardButton("Draco")],
        [KeyboardButton("Ursa")],
        [KeyboardButton("Leo")],
        [KeyboardButton("Noctua")]
    ]
    return ReplyKeyboardMarkup(keyboard)


def welfare_keyboard():
    keyboard = [
        [InlineKeyboardButton("Current Welfare Sign Up",
                              callback_data='current_welfare')],
        [InlineKeyboardButton("Future Welfare Events",
                              callback_data='future_welfare')],
        [InlineKeyboardButton("Back",
                              callback_data='back_home')],
    ]
    return InlineKeyboardMarkup(keyboard)


def feedback_keyboard():
    keyboard = [
        [InlineKeyboardButton("General Feedback",
                              callback_data='general_feedback')],
        [InlineKeyboardButton("Feedback for Event",
                              callback_data='event_feedback')],
        [InlineKeyboardButton("Back",
                              callback_data='back_home')],
    ]
    return InlineKeyboardMarkup(keyboard)


def settings_keyboard():
    keyboard = [
        [InlineKeyboardButton("On/Off Motivational Quotes",
                              callback_data='quotes_switch')],
        [InlineKeyboardButton("Back",
                              callback_data='back_home')],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_keyboard():

    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(keyboard)


def current_events_keyboard(events_array):
    # events_array: array of String
    keyboard = []
    counter = 0
    for event in events_array:
        keyboard.append([InlineKeyboardButton(
            event, callback_data="current_event"+str(counter))])
        counter += 1

    keyboard.append([InlineKeyboardButton(
        "Back", callback_data="welfare_events")])
    return InlineKeyboardMarkup(keyboard)


def future_events_keyboard(events_array):
    # events_array: array of String
    keyboard = []
    counter = 0
    for event in events_array:
        keyboard.append([InlineKeyboardButton(
            event, callback_data=("future_event"+str(counter)))])
        counter += 1

    keyboard.append([InlineKeyboardButton(
        "Back", callback_data="welfare_events")])
    return InlineKeyboardMarkup(keyboard)


def timings_keyboard(timings):
    # 15 min time interval default
    ## timings: [mintime, maxtime]
    keyboard = []
    mintime = timings[0]
    maxtime = timings[1]
    while mintime < maxtime:
        array = []
        # convert all 60 to 00hrs
        if (mintime % 100 == 60):
            mintime += 40
        if (mintime == maxtime):
            break

        while (mintime % 100 != 60):
            array.append(InlineKeyboardButton(
                str(mintime), callback_data=str(mintime)))
            mintime += 15

        keyboard.append(array)

    keyboard.append([InlineKeyboardButton(
        "Back", callback_data="current_welfare")])

    return InlineKeyboardMarkup(keyboard)


def feedback_events_keyboard(events_array):
    # events_array: array of String
    keyboard = []
    counter = 0

    for event in events_array:
        keyboard.append([InlineKeyboardButton(
            event, callback_data="fevents"+str(counter))])
        counter += 1

    keyboard.append([InlineKeyboardButton(
        "Back", callback_data="feedback")])
    return InlineKeyboardMarkup(keyboard)
