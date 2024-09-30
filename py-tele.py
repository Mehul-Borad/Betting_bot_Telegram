import telebot
import pandas as pd
import numpy as np

Names = {
'Mehul':'Mehul',
'C' : "C_Abhiram",
'Nagaruru':'N_Revanth',
'Katakam': 'K_Aashrith',
    'Mani':'Y_Mani_Sainath',
    'Sai':'Sai_Saketh'
}

chat_id = '-450115928'
token = ''
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['score', 'scores'])
def send_score(message):
    score = open('scores.txt', 'r')
    bot.reply_to(message, score.read())
    score.close()
    print(message)
    pass
@bot.message_handler(commands=['bet'])
def bet(message):
    Text = message.text.replace('/bet','')
    text = Text.strip().split(' ')
    try:
        text = [Names[str(message.from_user.first_name)],int(text[0]),int(text[1]),text[2].upper()]
        pd_bets = pd.read_csv('bets.txt',sep = ' ',names=['players', 'bet', 'DoN', 'team'], index_col=0)
        print(pd_bets)
        bet = int(pd_bets['bet'][text[0]])
        print(bet)
        if bet !=0:
            bot.reply_to(message, 'bet already given as {bet} by {player} on {team}'.format(bet = text[1], player = text[0], team = text[3]))
        else:
            pd_bets['bet'][text[0]] = text[1]
            pd_bets['DoN'][text[0]] = text[2]
            pd_bets['team'][text[0]] = text[3]
            print(pd_bets)
            pd_bets.reset_index(inplace=True)
            np.savetxt('bets.txt', pd_bets.to_numpy(), fmt = '%s %d %d %s')
            pd_bets.set_index('players')
            bot.reply_to(message, 'bet SET to {bet} by {player} on {team}'.format(bet = text[1], player = text[0], team = text[3]))
        pass

    except:
        bot.reply_to(message,'wrong format or name not entered correctly or not registered \nRegister by typing /score')

# @bot.message_handler(commands=['run'])
# def run(message):
#     if message.from_user.first_name == 'Mehul' or 'C':
#         main(message.text.replace('/run','').strip())

bot.polling()