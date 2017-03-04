import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

SNAKE = 1
FOOD = 3
directions = ['up', 'down', 'left', 'right']

def checkUp(kurt, grid):
	head = kurt['coords'][0]
	body = kurt['coords']
	print(body)
	futureMove = [head[0], head[1]-1]
	for coord in body:
		if futureMove == coord:
			return False
	if futureMove[1] < 0:
		return False
	return True

def checkLeft(kurt, grid):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0]-1, head[1]]
	for coord in body:
		if futureMove == coord:
			return False
	if futureMove[0] < 0:
		return False
	return True

def checkRight(kurt, grid):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0]+1, head[1]]
	for coord in body:
		if futureMove == coord:
			return False
	if futureMove[0] > 19:
		return False
	return True

def checkDown(kurt, grid):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0], head[1]+1]
	for coord in body:
		if futureMove == coord:
			return False
	if futureMove[1] > 19:
		return False
	return True

def noKill(kurt, grid):
	legal = []
	if checkUp(kurt, grid):
		legal.append('up')
	if checkLeft(kurt, grid):
		legal.append('left')
	if checkRight(kurt, grid):
		legal.append('right')
	if checkDown(kurt, grid):
		legal.append('down')
	print(legal)
	if legal:
		return legal
	return 'down'
def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    ourID = data['you']
    for snek in data['snakes']:
        if snek['id'] == ourID:
            kurt = snek
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] = SNAKE

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return kurt, grid

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
    data = bottle.request.json
    kurt, grid = init(data)
    legalMoves = noKill(kurt, grid)
    # TODO: Do things with data
    return {
        'move': random.choice(legalMoves),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))




