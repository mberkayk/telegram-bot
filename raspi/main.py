#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gpiozero import OutputDevice
from time import sleep, asctime
import subprocess



logFile = open("/home/pi/telegrambot/log", 'w')
relay = OutputDevice(4, active_high=True)
idFile = open("/home/pi/telegrambot/user_id.txt", 'r')
user_id = int(idFile.read())
idFile.close()


def log(msg):
  logMsg = asctime() + " " + msg
  print(msg)
  logFile.write(logMsg + "\n")
  logFile.flush()


def checkId(i):
  if i == user_id:
    return True
  else:
    return False

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def relay_command(update: Update, context: CallbackContext) -> None:
  if not checkId(update.message.chat_id):
    return
  if relay.value == 0:
    relay.on()
    sleep(0.6)
    relay.off()
    update.message.reply_text("done")
  else:
    update.message.reply_text("relay is already on")


def shut_command(update: Update, context: CallbackContext) -> None:
  if not checkId(update.message.chat_id):
    return
  if relay.value == 0:
    relay.on()
    sleep(4)
    relay.off()
    update.message.reply_text("done")
  else:
    update.message.reply_text("relay is already on")


def echo(update: Update, context: CallbackContext) -> None:
  """Echo the user message."""
  update.message.reply_text(update.message.text)
  pass

def main():
  # Enable logging
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
  )
  logger = logging.getLogger(__name__)

  tokenFile = open("/home/pi/telegrambot/token.txt", 'r')
  TOKEN = tokenFile.read()
  tokenFile.close()
  while True:
    try:
      """Start the bot."""
      # Create the Updater and pass it your bot's token.
      updater = Updater(TOKEN)

      # Get the dispatcher to register handlers
      dispatcher = updater.dispatcher

      # on different commands - answer in Telegram
      dispatcher.add_handler(CommandHandler("relay", relay_command))
      dispatcher.add_handler(CommandHandler("shut", shut_command))

      # on noncommand i.e message - echo the message on Telegram
      dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

      # Start the Bot
      updater.start_polling()

      # Run the bot until you press Ctrl-C or the process receives SIGINT,
      # SIGTERM or SIGABRT. This should be used most of the time, since
      # start_polling() is non-blocking and will stop the bot gracefully.
      updater.idle()
    except Exception:
      log("Exception occurred in the main function")
      log("Sleeping for sixty seconds")
      sleep(60)
    log("Trying again!")
    
  logFile.close()

  
if __name__ == '__main__':
  main()