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

   
    new_color = color_choice[randint(0, color_choice.len - 1)]

    round_msg = render_template('round', color = new_color)

    session.attributes['list_of_colors'] = [new_color]  

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': str, 'second': str, 'third': str, 'fourth': str, 'fifth': str})

def answer(first, second, third, fourth, fifth):

    current_colors = session.attributes['list_of_colors']
    match = false
    user_answers = [first, second, third, fourth, fifth]
    index = 0
    for color in current_colors:
        if color != user_answers[index]:
            match = false
            break
        else:
            index += 1
            match = true

    if match:

        new_color = color_choice[randint(0, color_choice.len - 1)]
        msg = render_template('round', color = new_color)
        current_colors.append(new_color)
        session.attributes['list_of_colors'] = current_colors

    else:

        msg = render_template('lose', current_colors )

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)