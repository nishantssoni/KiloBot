from decouple import config
from utility_function import giveAns
import jiosaavn
# telegram packages
from telegram import Update, ForceReply, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# start
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!\
you can use /info /help /svn command \
/svn nameofsong',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    text = update.message.text
    update.message.reply_text('ask question on fb: https://www.facebook.com/nishantssoni01')


def info_command(update: Update, context: CallbackContext) -> None:
    """send a info of who ceated bot"""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'ok {user.mention_markdown_v2()}\! this bot is created by @nishantshekharsoni using https://github\.com/cyberboysumanjay/JioSaavnAPI'
        
    )

def svn_command(update: Update, context: CallbackContext) -> None:
    """Send song to the user """
    try:
        text = update.message.text[5:]
        elements = jiosaavn.search_for_song(text,True,True)

        for element in elements:
            # print(element.keys())
            song = element['song']
            artist = element['primary_artists']
            album = element['album']
            year = element['year']
            duration = int(element['duration'])
            release = element['release_date']
            link = element['media_url']



            r_text =  song +" ( "+ year + " ) " "\n\n" \
                    + "ARTIST  : " + artist+ '\n\n' \
                    + "ALBUM   : " + album + "\n\n" \
                    + "DURATION  : " + "{:.2f}".format((duration / 60)) + " min" + "\n\n" \
                    + "RELEASE DATE  : " + release[8:10] + "-" + release[5:7] + "-"+ release[0:4] + "\n\n" \
                    +  link
            
            update.message.reply_text(r_text)

    except:
        update.message.reply_text("put your query after /svn command")
    

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    query = update.message.text
    update.message.reply_text(giveAns(query))

def image(update: Update, context: CallbackContext) -> None:
    newFile = update.message.effective_attachment[-1].get_file()
    file_name = update.message.effective_attachment[-1]['file_unique_id']+ '.jpg'
    newFile.download('./image/'+file_name)
    update.message.reply_text("your image is downloaded in image folder!!!")



def main() -> None:
    api_key = config("API_KEY")
    updater = Updater(api_key)
    image_count = 0
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("info",info_command))
    dispatcher.add_handler(CommandHandler("svn",svn_command))
    

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, image))
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
