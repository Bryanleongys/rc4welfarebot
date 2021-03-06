import keyboards
import initialization
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove

'''
Defining constants
'''

EVENT_ID = 0
EVENT_NAME = 1
START_DATE = 2
END_DATE = 3
COLLECTION_DATE = 4
START_TIME = 5
END_TIME = 6
EVENT_MESSAGE = 7

ECC_EVENT_ID = 0
CHOICE_HEADER = 1
CHOICE_NAME = 2

def prompt_welfare(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    print(chat_id)
    message_id = query.message.message_id

    text = "Please select the following options:"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.welfare_keyboard()
    )

    return ConversationHandler.END

def show_future_welfare(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    events = db.query_all_future_events()
    future_events = []
    for event in events:
        future_events.append(
            event[EVENT_NAME] + ", " + event[COLLECTION_DATE])

    text = "Below are the list of welfare in the future!"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.future_events_keyboard(future_events)
    )
    return ConversationHandler.END

def show_current_welfare(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    events = db.query_all_sign_up_events()
    context.user_data["events"] = events
    current_events = []
    for event in events:
        current_events.append(event[EVENT_NAME] + ", closes " + event[END_DATE])

    text = "Please select one of the options to sign up for welfare!"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.current_events_keyboard(current_events)
    )
    return 1


def show_timings(update, context, db):
    query = update.callback_query
    if (query.data == "return_back"):
        index = context.user_data["index"]
    else:
        index = int(query.data[7:])
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    ## initialize variables
    events = context.user_data["events"]
    context.user_data["event_name"] = events[index][EVENT_NAME]
    context.user_data["event_date"] = events[index][COLLECTION_DATE]
    item_bool = db.query_event_choice_exist(events[index][EVENT_NAME])
    context.user_data["item_bool"] = item_bool
    context.user_data["index"] = index
    timings = [events[index][START_TIME], events[index][END_TIME]]

    text = "Select time slot to sign up for " + \
        events[index][EVENT_NAME] + " on " + events[index][COLLECTION_DATE] + "."
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.timings_keyboard(timings, db, events[index][EVENT_NAME])
    )
    # print(items_bool_array[index] == '1')
    if (item_bool):
        return 2
    else:
        return 3


def show_item_events(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    timing = int(query.data[6:])
    context.user_data["timing"] = timing
    event_name = context.user_data["event_name"]

    arrayDatabase = db.query_events_choices(event_name)
    arrayOptions = []

    for row in arrayDatabase:
        arrayOptions.append(row[CHOICE_NAME])
        
    text = arrayDatabase[0][1]

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.event_items_keyboard(arrayOptions)
    )
    # update.message.reply_text(text, reply_markup=keyboards.event_items_keyboard())
    return 3


def confirm_timing(update, context, db):
    query = update.callback_query
    username = query.message.chat.username
    item_bool = context.user_data["item_bool"]

    if (item_bool):
        timing = context.user_data["timing"]
        item_chosen = query.data[6:]
        print(item_chosen)
    else:
        timing = int(query.data[6:])
        item_chosen = ""

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    event_name = context.user_data["event_name"]
    event_date = context.user_data["event_date"]
    full_name = db.query_user_name(chat_id)
    timing = str(timing)
    timing = timing[0:2] + ":" + timing[2:]

    db.insert_event_joined(event_name, full_name, chat_id, username, timing, item_chosen)
    db.query_all_events_joined()

    if item_chosen == "":
        text = "Confirmation Message: You have signed up for " + event_name + \
            " on " + str(event_date) + ", " + str(timing) + "hrs! You will receive another message through the bot if you have been successfully chosen for the welfare."
    else:
        text = "Confirmation Message: Thank you for signing up for " + event_name + ", "+ str(item_chosen) + "," +\
            " on " + str(event_date) + ", " + str(timing) + "hrs! You will receive another message through the bot if you have been successfully chosen for the welfare."
    text2 = "Welcome home. Feel free to access the features below!"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
    )
    context.bot.send_message(
        chat_id=chat_id,
        text=text2,
        reply_markup=keyboards.main_options_keyboard()
    )

    return ConversationHandler.END


def return_home(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    text = "Welcome home. Feel free to access the features below!"

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_options_keyboard(),
    )

    return ConversationHandler.END
