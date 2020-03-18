from telegram.ext import (Updater, ConversationHandler, CommandHandler, MessageHandler, Filters)
import logging
import datetime
import requests


# TODO: Point it to the correct address
API_ENDPOINT = "http://localhost:8000/api/food"
# NOTIFICATION_API_ENDPOINT = "http://localhost:8000/api/notify"
SET_EXPIRY_API_ENDPOINT = "http://localhost:8000/api/set-expiry"
# API_KEY = "XXXXXXXXXXXXXXXXX"

#start logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#dummy array
itemsArray = [{'name': 'potato', 'expiry_date': '31/10/3020'}, {'name': 'leek', 'expiry_date': '26/03/2020'}]

#declare constants
CHECK = 1


def start(update, context):
	update.message.reply_text("Hello")

def getAllItems(update, context):
	# fetchItems
	response = requests.get(API_ENDPOINT)
	if response.status_code == 200:
		itemsArray = response.json()

	message = '\n'.join(['{} expires on {}'.format(item['name'], item['expiry_date']) for item in itemsArray])
	update.message.reply_text(message)

#manually entering expiry convo
def setExpiry(update, context):
	logger.info('ask expiry')
	update.message.reply_text("Enter expiry date in the format dd/mm/yyyy.\nTo assign an estimated date instead, enter /estimate.\nTo cancel, enter /cancel")
	return CHECK

def enterCheck(update, context):
	logger.info('checking date')

	#anticipate split error
	try:
		day,month,year = update.message.text.split("/")
	except ValueError:
		update.message.reply_text("Enter expiry date in the format dd/mm/yyyy")
		return CHECK

	#check if day month year had 2 int each
	if (len(day)!=2 or (len(month)!=2) or len(year)!= 4):
		update.message.reply_text("Enter expiry date in the format dd/mm/yyyy")
		return CHECK

	#check if valid date
	try:
	    date = datetime.date(int(year),int(month),int(day))
	except ValueError:
		update.message.reply_text("Invalid date, please try again")
		return CHECK
	
	#check if date is in the future
	if datetime.date.today() > date:
		update.message.reply_text("Date is in the past, please try a new date")
		return CHECK

	# dateString = '{day}-{month}-{year}'.format(day=date.day, month=date.month, year=date.year)
	update.message.reply_text("Enter success! Date set is " + str(date.day) + '/' + str(date.month) + '/' + str(date.year))
	# update.message.reply_text("Enter success! Date set is " + dateString)

	# send it back to database
	requests.get(SET_EXPIRY_API_ENDPOINT, params={'date': date})

	return ConversationHandler.END

def estimate(update, context):
	#estimate the date based on picture
	logger.info('estimate')
	update.message.reply_text("The estimated date has been set for ____.")
	return ConversationHandler.END

def cancel(update, context):
	#estimate the date based on picture
	update.message.reply_text("Cancelled, no expiry date saved")
	return ConversationHandler.END


def listCommands(update, context):
	update.message.reply_text("You can:\n/getall to get all food items\n/setexpiry to manually set an expiry date")

def error(update, context):
	update.message.reply_text("Error, try again")
	logger.warning('Caused error "%s"', context.error)

def main():
    updater = Updater(token='1115783483:AAE2pJLsDCIc0x4HosJmrFKuUI0uw_yePtI', use_context = True)
    dp = updater.dispatcher

    conv_handler= ConversationHandler(
    	entry_points=[CommandHandler('setexpiry', setExpiry)],
    	states = {
    		CHECK: [MessageHandler(Filters.regex("^\d+(\/\d+)*$"), enterCheck)]
    		},

		fallbacks = [CommandHandler('estimate', estimate),
					CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('getall', getAllItems))

    dp.add_handler(conv_handler)

    dp.add_handler(MessageHandler(Filters.command, listCommands))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
