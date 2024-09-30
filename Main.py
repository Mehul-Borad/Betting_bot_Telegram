import numpy as np
import webbrowser
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import telebot
#
# pd_scores = pd.read_csv('new_scores.txt', sep=' ', header = None, names=['Player', 'score'], index_col=0)
# pd_scores.plot.bar()
# plt.show()
# print(pd_scores)

print('Testing...')

chat_id = '-450115928'
token = ''
# google drive link for scores.txt
scorces_link = 'https://drive.google.com/file/d/1IBxw4b7SrQU7u0UL3XIvq6BzGV_6unki/view?usp=sharing'
Names = {
'Mehul':'Mehul',
'C' : "C_Abhiram",
'Nagaruru':'N_Revanth',
'Katakam': 'K_Aashrith',
    'Mani':'Y_Mani_Sainath',
    'Sai':'Sai_Saketh'
}


# def message(text):
# webbrowser.open('https://api.telegram.org/bot'+token+'/sendMessage?chat_id=-'+chat_id+'&text=' + text.replace(' ', '+'))
#     r= requests.get(url='https://api.telegram.org/bot'+token+'/sendMessage',params={'chat_id':chat_id,'text':text})
#     pass
'''
def run():
    scores = open('scores.txt', 'r+')
    np_scores = []
    scores.seek(0)
    i=0
    for line in scores.readlines():
        line = line.replace('\n','').split()
        np_scores.append(line)
        i+=1
        pass
    print(np_scores)
    scores.seek(0)

    np_scores = np.array([[player, int(score)] for [player,score] in np_scores])
    bets =[]
    np_bets = []

    for i in np_scores:
        bets.append([int(input('bet of ' + i[0] + ' = ')),input('team ').upper() ,bool(int(input('double or nothing ? ')))])
        if bets[-1][2]:
            bets[-1][0] *= 2
        pass
    pot_money = sum([i for [i,n,b] in bets])
    print('pot money = ' + str(pot_money))
    for i in range(len(bets)):
        np_bets.append([np_scores[i,0],bets[i][0],bets[i][1],int(np_scores[i,1]), bets[i][2]])
        pass

    print('players = '+ str(np_bets))
    team_won = input('winning team = ').upper()

    winning_pot_money = 0
    winning = []
    losing = []
    for i in np_bets:
        if i[2] == team_won:
            winning_pot_money += i[1]
            winning.append(i)
            pass
        else:
            losing.append(i)
        pass
    print(winning_pot_money, winning)

    # scores.truncate(0)
    new_scores = open('new_scores.txt','r+')
    new_scores.seek(0)
    lines_new_scores = []
    for line in new_scores.readlines():
        lines_new_scores.append(line.replace('\n',''))
        pass
    new_scores.seek(0)
    new_scores.truncate(0)

    final_scores = []
    for l,i in enumerate(np_bets):
        if i in winning:
            if not i[4]:
                final_score = int(round(((round(i[1]*20/(winning_pot_money))/20)*(pot_money) + i[3] - i[1])/5)*5)
                scores.write(i[0] + ' ' + str(final_score) + '\n')
                new_scores.write(lines_new_scores[l] + ' ' + str(final_score) + '\n')
                final_scores.append(final_score)
            else:
                final_score = int(round((i[1] + i[3])/5)*5)
                scores.write(i[0] + ' ' + str(final_score) + '\n')
                new_scores.write(lines_new_scores[l] + ' ' + str(final_score) + '\n')
                final_scores.append(final_score)
        elif i in losing:
            final_score = int(round((i[3]-i[1])/5)*5)
            scores.write(i[0] + ' ' + str(final_score) + '\n')
            new_scores.write(lines_new_scores[l] + ' ' + str(final_score) + '\n')
            final_scores.append(final_score)
            pass
        pass

    sort_scores()
    new_scores.close()
    scores.close()
    pass
'''
def sort_scores():
    pd_scores = pd.read_csv('scores.txt', sep=' ', header = None, names=['players', 'score'])
    pd_scores = pd_scores.sort_values(by=['score'], ascending=False)
    np.savetxt('scores.txt', pd_scores.to_numpy(), fmt= '%s %d')

# def message_file_as_text(file):
#     file = open(file, 'r')
#     message(file.read())
#     file.seek(0)
#     file.close()
#     pass


# def message_file(file_link):
#     r = requests.get(url='https://api.telegram.org/bot'+token+'/sendDocument',params={'chat_id': chat_id, 'document': file_link})
#     print(r.iter_content())
#     pass

def run_array(bets, team_won):
    final_scores = []
    pot_money = 0
    winning_pot_money = 0
    for player in bets.iterrows():
        player = player[1]
        if player['team'] != team_won:
            if player['DoN']:
                pot_money += player['bet']*2
                pass
            else:
                pot_money += player['bet']
                pass
            pass
        else:
            if player['DoN']:
                pot_money += player['bet']*2
                winning_pot_money += player['bet']*2
                pass
            else:
                pot_money += player['bet']
                winning_pot_money += player['bet']
                pass
            pass
        pass
    for player in bets.iterrows():
        name = player[0]
        player = player[1]
        if player['team'] == team_won:
            if player['DoN']:
                final_scores.append([name,player['score']+player['bet']*2])
                pass
            else:
                final_scores.append([name,player['score']+round(((round((player['bet']*20.0/winning_pot_money))/20.0)*(pot_money-winning_pot_money))/5)*5])
                pass
            pass
        else:
            if player['DoN']:
                final_scores.append([name,player['score']-player['bet']*2])
                pass
            else:
                final_scores.append([name,player['score']-player['bet']])
                pass
            pass
        pass
    return final_scores


def main(winning_team):
    pd_bets = pd.read_csv('bets.txt',sep=' ',names=['players','bet','DoN', 'team'], index_col=0)
    for player in pd_bets.iterrows():
        pd_bets['DoN'][player[0]] = True if pd_bets['DoN'][player[0]] == 1 else False
    pd_score = pd.read_csv('scores.txt',sep=' ',names=['players','score'],index_col=0)
    pd_total = pd_bets.join(pd_score)
    new_scores = run_array(pd_total, winning_team)
    print(np.array(new_scores))
    np.savetxt('scores.txt', np.array(new_scores), fmt='%s %s')
    pd_bets = pd.read_csv('bets.txt',sep=' ',names=['players','bet','DoN', 'team'])
    pd_bets['bet'] = 0
    np.savetxt('bets.txt', pd_bets.to_numpy(), fmt='%s %d %d %s')
    sort_scores()

# run()
# sort_scores()
# main('a')

chat_id = '-450115928'
token = '1311434235:AAFSm-jrE1PFC1sEY2w8v-7BkqE2FCFnyvE'
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['score', 'scores'])
def send_score(message):
    score = open('scores.txt', 'r')
    bot.reply_to(message, score.read())
    score.close()
    print(message)
    pass
@bot.message_handler(commands=['bets'])
def send_score(message):
    score = open('bets.txt', 'r')
    bot.reply_to(message, score.read())
    score.close()
    print(message)
    pass
@bot.message_handler(commands=['bet'])
def bet(message):
    Text = message.text.replace('/bet','')
    text = Text.strip().split(' ')
    try:
        text = [text[0],int(text[1]),int(text[2]),text[3].upper()]
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

@bot.message_handler(commands=['run'])
def run(message):
    if message.from_user.first_name == 'Mehul' or 'C':
        try:
            main(message.text.replace('/run','').strip().upper())
            bot.reply_to(message,'running sucess '+'text /score for the new score!!')
            pass
        except:
            bot.reply_to(message,'wrong format')
            pass
        pass
    else:
        bot.reply_to(message,'Unauthorised')

bot.polling()
