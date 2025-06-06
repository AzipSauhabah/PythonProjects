/******************************************************************************
 * @file    main.cpp
 * @author  Azip Sauhabah
 * @author  Azip Sauhabah
 * @date    March 2025
 * @coms    Videojuegos - OutRun
 ******************************************************************************/

#include <SFML/Graphics.hpp>
#include "Menu.hpp"
#include "Game.hpp"

using namespace sf;
using namespace std;

int main() {

    Config c;
    State state = ANIMATION;

    while (c.window.isOpen() && state != EXIT) {
        Game engine(c);

        sleep(milliseconds(500));
        if (state == START)
            state = startMenu(c);

        while (c.window.isOpen() && state != START) {
            switch (state) {
                case ANIMATION: {
                    state = introAnimation(c);
                    break;
                }
                case MUSIC: {
                    sleep(milliseconds(500));
                    state = selectMusicSoundtrack(c);
                    break;
                }
                case OPTIONS: {
                    sleep(milliseconds(500));
                    bool inGame = engine.isInGame();
                    state = optionsMenu(c, inGame);
                    engine.checkDifficulty(c);
                    break;
                }
                case GAME: {
                    state = engine.play(c);
                    break;
                }
                case RANKING: {
                    unsigned long scorePlayer = engine.getScore();
                    int minutes = int(engine.getMinutesTrip());
                    int secs = int(engine.getSecsTrip());
                    int cents_Second = int(engine.getCents_SecondTrip());
                    state = rankingMenu(c, scorePlayer, minutes, secs, cents_Second);
                    break;
                }
                default: {
                    c.window.close();
                    break;
                }
            }
        }
    }
}
