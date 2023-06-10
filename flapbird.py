import curses
import random

def main(stdscr):
    # Game settings
    bird = '^'
    pipe = '|'
    gap_size = 5
    bird_x = 5
    bird_y = 10
    score = 0

    # Initialize the screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.nodelay(1)  # Set the window input to non-blocking
    w.timeout(200)  # Slower game speed

    # Create the pipes
    pipes = []
    for i in range(20, 100, 20):
        upper = random.randint(2, sh-2-gap_size)
        lower = upper + gap_size
        pipes.append((i, upper, lower))

    game_over = False

    while not game_over:
        # Display the bird
        w.clear()
        w.addstr(bird_y, bird_x, bird)

        # Display the pipes
        for pipe in pipes:
            x, upper, lower = pipe
            for y in range(0, upper):
                w.addstr(y, x, '|')
            for y in range(lower, sh-1):
                w.addstr(y, x, '|')

        # Display the score
        w.addstr(0, 0, f"Score: {score}")

        w.refresh()

        # Game logic
        key = w.getch()

        # Quit game
        if key == ord('q'):
            break

        # Bird movement
        if key == ord(' '):
            bird_y -= 2
        else:
            bird_y += 1

        # Check collision
        if bird_y >= sh-1 or bird_y < 1:
            game_over = True
        for pipe in pipes:
            x, upper, lower = pipe
            if bird_x == x and (bird_y < upper or bird_y > lower):
                game_over = True

        # Move pipes
        new_pipes = []
        for pipe in pipes:
            x, upper, lower = pipe
            if x > 0:
                new_pipes.append((x-1, upper, lower))
            else:
                score += 1
                upper = random.randint(2, sh-2-gap_size)
                lower = upper + gap_size
                new_pipes.append((sw-1, upper, lower))
        pipes = new_pipes

    # Display game over
    while True:
        w.clear()
        w.addstr(sh//2, sw//2, "Game Over!")
        w.addstr(sh//2 + 1, sw//2, f"Final Score: {score}")
        w.refresh()

        key = w.getch()
        # Quit game
        if key == ord('q'):
            break

if __name__ == '__main__':
    curses.wrapper(main)
