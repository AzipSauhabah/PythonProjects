/******************************************************************************
 * @file    KeywordMapper.hpp
 * @author  Azip Sauhabah, 716358
 * @author  Azip Sauhabah, 737215
 * @date    Mayo 2020
 * @coms    Videojuegos - OutRun
 ******************************************************************************/

#ifndef KEYWORD_MAPPER_H
#define KEYWORD_MAPPER_H

#include <iostream>
#include <SFML/Graphics.hpp>

const int KEYWORDS_MAPPED = 75;

struct KeywordMapper {
    // Maps of the keywords available in the game
    sf::Keyboard::Key mapperCodeKeyWord[KEYWORDS_MAPPED];
    std::string mapperIdKeyWord[KEYWORDS_MAPPED];

    /**
     * Constructor por defecto.
     */
    KeywordMapper();
};

#endif // KEYWORD_MAPPER_H
