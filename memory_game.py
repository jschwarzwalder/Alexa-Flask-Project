import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

color_choice = [ "red", "blue", "green", "yellow", "orange", "purple", "white", "black", "brown", "silver", "gold"]


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

   
    new_color = [color_choice[randint(0, color_choice.len)]]

    round_msg = render_template('round', new_color)

    session.attributes['colors'] = [new_color]  

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': str, 'second': str, 'third': str, 'fourth': str, 'fifth': str})

def answer(first, second, third, fourth, fifth):

    current_colors = session.attributes['colors']

    if [first, second, third] == winning_numbers:

        new_color = color_choice[randint(0, color_choice.len)]
        msg = render_template('round', new_color)
        current_colors.append(new_color)
        session.attributes['colors'] = colors[::] 

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)