import bottle
import os
import random

counter = 0

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    global counter
    data = bottle.request.json
    if counter == 0:
        myMove = 'left'
    elif counter == 1:
        myMove = 'down'
    elif counter == 2:
        move = 'right'
    else:
	myMove = 'up'
        counter = 0
    counter = counter + 1
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    return {
        'move': myMove,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))




