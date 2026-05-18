import asyncio
import pygame

async def main():
    pygame.init()

    import os
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    from data import tools, constants as c
    from data.states import main_menu, load_screen, level1

    pygame.display.set_caption(c.ORIGINAL_CAPTION)
    screen = pygame.display.set_mode(c.SCREEN_SIZE)

    from data import setup
    setup.SCREEN = screen
    setup.SCREEN_RECT = screen.get_rect()

    run_it = tools.Control(c.ORIGINAL_CAPTION)

    state_dict = {
        c.MAIN_MENU: main_menu.Menu(),
        c.LOAD_SCREEN: load_screen.LoadScreen(),
        c.TIME_OUT: load_screen.TimeOut(),
        c.GAME_OVER: load_screen.GameOver(),
        c.LEVEL1: level1.Level1()
    }

    run_it.setup_states(state_dict, c.MAIN_MENU)

    while not run_it.done:
        run_it.main()
        await asyncio.sleep(0)

asyncio.run(main())
