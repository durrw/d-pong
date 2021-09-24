from cmu_graphics import *
PADDLE_SPEED = 8


#ui components
def create_player(x, y, color):
    paddle_group = Group()
    paddle_width = 50
    paddle_height = 10
    paddle = Rect(
        x,y,paddle_width, paddle_height,
        fill=color)
    left_end = Circle(x, y + paddle_height/2, paddle_height/2, fill=color)
    right_end = Circle(x + paddle_width, y + paddle_height/2, paddle_height/2, fill=color)
    paddle_group.add(paddle)
    paddle_group.add(left_end)
    paddle_group.add(right_end)
    
    return paddle_group

def create_ball():
    ball_group = Group()
    ball_group.add(Rect(200, 200, 10, 10, fill='white'))
    return ball_group

def start_round():
    # Setup the game for each ball
    gong.play()
    game.ball.centerX = 200
    game.ball.centerY = 200
    game.player_1.centerX = 200
    game.player_2.centerX = 200
    game.ball_dx = 0
    game.ball_dy = 5
    game.round += 1
    show_score()
    # alternates ball y value on even rounds
    if game.round % 2 == 0:
        game.ball_dy *= -1

#game handling
def start_game():
    print("starting game")
    game.welcome.visible = False
    game.ball.visible = True
    game.is_playing = True
    start_round()

#event handling

def move_player(player, amount_to_move):
    player.centerX += amount_to_move
    
    if player.centerX < 20:
        player.centerX = 20
    if player.centerX > 380:
        player.centerX = 380

def check_hit(group_a, group_b):
    hit = False
    for shape_a in group_a.children:
        for shape_b in group_b.children:
            if shape_a.hitsShape(shape_b):
                hit = True
                break
            break
    return hit

def check_ball():
    # score for player 2
    someone_scored = False
    
    if game.ball.centerY < 9:
        game.player_2_score += 1
        someone_scored = True
        
    if game.ball.centerY > 391:
        game.player_1_score += 1
        someone_scored = True
    
    if someone_scored:
        print("PLAYER 1:", game.player_1_score)
        print("PLAYER 2:", game.player_2_score)
        score.value = f"{game.player_1_score} / {game.player_2_score}"
        start_round()
        
    #as long as someone didnt score, bounce the ball back
    if check_hit(game.ball, game.player_1):
        print("player 1 got to the ball")
        game.ball_dy *= -1
        dx = game.ball.centerX - game.player_1.centerX
        dx /= 5
        game.ball_dx = dx
        
    if check_hit(game.ball, game.player_2):
        print("player 2 got to the ball")
        game.ball_dy *= -1
        dx = game.ball.centerX - game.player_2.centerX
        dx /= 5
        game.ball_dx = dx
        
    # bounce of side walls
    if game.ball.centerX < 5:
        print('bounce off left wall')
        game.ball_dx *= -1
        
    if game.ball.centerX > 395:
        print('bounce off right wall')
        game.ball_dx *= -1

# ball movement
def move_ball():
    #print('move ball called')
    game.ball.centerY += game.ball_dy
    game.ball.centerX += game.ball_dx
    



def onStep():
    #print(game.game_step)
    if game.is_playing:
        game.game_step += 1
        move_ball()
        check_ball()
    

def onKeyPress(key):
    
    if key == 'space':
        start_game()
    if key == 's':
        game.ball_dy *= 3
        
        
def onKeyHold(keys):
    if 'a' in keys:
        move_player(game.player_1, -PADDLE_SPEED)
    if 'd' in keys:
        move_player(game.player_1, PADDLE_SPEED)
    if 'left' in keys:
        move_player(game.player_2, -PADDLE_SPEED)
    if 'right' in keys:
        move_player(game.player_2, PADDLE_SPEED)
#user interaction
def welcome():
        # messages
    messages = Group()
    messages.add(Label("D's Pong",200,200,size=25, fill='white', font='monospace', bold=True))
    messages.add(Label('For player 1 use A and D',200,250,size=12, fill='white', font='monospace', bold=True))
    messages.add(Label('For player 2 use Left and Right arrow keys',200,265,size=12, fill='white', font='monospace', bold=True))
    messages.add(Label('Good Luck!',200,280,size=12, fill='white', font='monospace', bold=True))
    messages.add(Label('Press space to start',200,300,size=12, fill='white', font='monospace', bold=True))
    
    return messages


class Game():
    def __init__(self):
        self.player_1 = create_player(175,0, "red")
        self.player_2 = create_player(175,390, "cyan")
        
        self.player_1_score = 0
        self.player_2_score = 0
    
        self.welcome = welcome()

        self.ball = create_ball()
        self.ball.visible = False
        self.is_playing = False
        self.game_step = 0
        self.ball_dy = 0
        self.ball_dx = 0
        self.round = 0

# init
app.background=('black')
gong = Sound("https://soundbible.com/mp3/Bell%20Sound%20Ring-SoundBible.com-181681426.mp3")

game = Game()


score = Label('0 / 0', 200, 200, bold=True, fill='white', size=50, opacity=50, font='monospace')
score.visible = False




def show_score():
    score.visible = True
 