/******************************************************************************
 * @file    Map.hpp
 * @author  Azip Sauhabah, 716358
 * @author  Azip Sauhabah, 737215
 * @date    Mayo 2020
 * @coms    Videojuegos - OutRun
 ******************************************************************************/

#ifndef OUTRUN_MAP_HPP
#define OUTRUN_MAP_HPP

#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#include <SFML/Graphics.hpp>
#include <string>
#include <vector>
#include "Menu.hpp"
#include "Enemy.hpp"

#define PRE_POS 2
#define FORK_RADIUS 10.0f

const int RECTANGLE = PRE_POS * 2 + 1; // the number of lines that form a rectangle

/**
 * Mapa que contiene la textura del paisaje (bg) y la textura de los objetos que se irán mostrando a lo
 * largo del mapa (objects). Además cada objeto tendrá un coeficiente que indicará el porcentaje total del objeto con
 * el que se puede chocar empezando desde el centro [0, 1]. Esto es útil para objetos cuya base es menor a la copa.
 * El suelo está formado por un número limitado de rectángulos horizontales (lines) que tendrán dibujado el trozo de
 * carretera que les corresponda y objetos en los laterales.
 * Dependiendo de la posición de la cámara (posX, posY) el primer rectángulo visible será uno u otro y los objetos se
 * verán más grandes si están más cerca de la pantalla o más pequeños si están más lejos.
 */
class Map {
    /**
     * Información de un objeto correspondiente a objects[spriteNum] si spriteNum != -1, con un offset en x.
     * Si repetitive es true el objeto se repetirá hasta el borde de la pantalla.
     */
    struct SpriteInfo {
        int spriteNum;
        float offset, spriteMinX, spriteMaxX, spriteToSideX; // spriteToSideX is the space from spriteMinX to another minX side
        bool repetitive;

        /**
         * Inicializa el sprite.
         */
        SpriteInfo();
    };

    /**
     * Rectángulo horizontal cuyo centro está ubicado en las coordenadas (x, y, z), es decir, puede tener elevación (z).
     * En el centro del rectángulo estará la carretera que puede tener una curvatura dependiendo del coeficiente de
     * curvatura (curve) que tenga.
     * Además, puede contener un objeto en cada lateral de la carretera (spriteLeft, spriteRight).
     */
    struct Line {
        float x, y, z; // 3d center of line
        float X{}, Y{}, W{}; // screen coord (X: road center, Y: road top, W: road width / 2)
        float curve, clip{}, scale{};
        bool mainColor;
        SpriteInfo spriteLeft, spriteRight;
        float bgX; // background position
        float offsetX, yOffsetX;

        /**
         * Inicializa el rectángulo.
         */
        explicit Line();

        /**
         * Establece las coordenadas en la pantalla que corresponen al rectángulo y su escala. Esta función debe ser
         * llamada para actualizar el rectángulo si se ha variado la posición del mapa y.
         * @param camX
         * @param camY
         * @param camZ
         * @param camD
         * @param width
         * @param height
         * @param rW
         * @param zOffset
         */
        void
        project(float camX, float camY, float camZ, float camD, float width, float height, float rW, float zOffset);

        enum HitCoeffType {
            HIT_CENTER,
            HIT_LEFT,
            HIT_RIGHT,
            HIT_SIDES // Example arc
        };

        /**
         * Dibuja el objeto en la pantalla. Esta función debe ser llamada después de project().
         * @param w
         * @param objs
         * @param hitCoeff
         * @param hitCoeffType
         * @param scaleCoeff
         * @param object
         * @param left indica si el objeto está a la izquierda de la pantalla
         */
        void drawSprite(sf::RenderTexture &w, const std::vector<sf::Texture> &objs, const std::vector<float> &hitCoeff,
                        const std::vector<HitCoeffType> &hitCoeffType, const std::vector<float> &scaleCoeff,
                        SpriteInfo &object, bool left) const;
    };

    // Circles info for forks (with different centers):
    // Circle 1: y = -sqrt(r² - x²) + r
    // Circle 2: y = sqrt(r² - (x - a)²) + b
    const float aOffsetX = sqrt(2.0f) * FORK_RADIUS; // a value for C1
    const float bOffsetX = FORK_RADIUS - sqrt(2.0f) * FORK_RADIUS; // b value for C1
    const float xChange = static_cast<const float>(FORK_RADIUS * sin(0.75f * M_PI)); // x increment

    // Background
    sf::Texture bg;

    // Objects
    std::vector<sf::Texture> objects;
    std::vector<float> hitCoeffs;
    std::vector<Line::HitCoeffType> hitCoeffTypes;
    std::vector<float> scaleCoeffs;
    std::vector<Line> lines;

    // Colors
    sf::Color roadColor[2], grassColor[2], rumbleColor, dashColor;

    // Camera
    float posX, posY;

    // Next map
    Map *next, *nextRight;

    bool initMap;
    bool goalMap;

    int maxTime;

    /**
     * Devuelve Line n
     * @param n
     * @return
     */
    Line *getLine(int n);

    /**
     * Devuelve Line n
     * @param n
     * @return
     */
    Line getLine(int n) const;

    /**
     * Devuelve Line anterior a n
     * @param n
     * @return
     */
    Line *getPreviousLine(int n);

    /**
     * Devuelve Line anterior a n
     * @param n
     * @return
     */
    Line getPreviousLine(int n) const;

    /**
     * Añade un rectángulo al mapa. Actualiza z para una nueva línea.
     * @param x
     * @param y
     * @param z
     * @param curve
     * @param mainColor
     * @param spriteLeft
     * @param spriteRight
     * @param bgX
     * @param offsetX es > 0 si hay una bifurcación
     * @param offsetInc
     */
    void addLine(float x, float y, float &z, float prevY, float curve, bool mainColor, const SpriteInfo &spriteLeft,
                 const SpriteInfo &spriteRight, float &bgX, float &offsetX, float offsetInc = 0.0f);

    /**
     * Añade rectángulos desde las instrucciones al mapa desde (x, y, z). Actualiza z para una nueva línea.
     * @param x
     * @param y
     * @param z
     * @param bgX
     * @param instructions
     */
    void addLines(float x, float y, float &z, float &bgX, const std::vector<std::vector<std::string>> &instructions);

    /**
     * Carga los objetos en el mapa y devuelve un vector con los índices de los objetos.
     * @param path
     * @param objectNames
     * @param objectIndexes
     */
    void
    loadObjects(const std::string &path, const std::vector<std::string> &objectNames, std::vector<int> &objectIndexes);

public:
    // Crea un mapa con un paisaje dado el nombre del fichero de la imagen y con unos objetos dados los nombres de los
    // ficheros de las imágenes. El contenido del mapa debe encontrarse en la ruta path. Si random es true se crea el
    // mapa de manera aleatoria, en cambio si random es false se crea el mapa a partir del fichero map.info, que se
    // describe a continuación:
    //      - Se pueden incluir comentarios en cualquier parte, comenzando por /* y terminando por */
    //      - En primer lugar se deben indicar los dos colores de la carretera, los dos del suelo, el del arcén (rumble)
    //        y el de las rayas discontinuas (dash), en RGB y separados por espacios.
    //      - En segundo lugar se indica el recorrido con objetos, curvas y elevaciones.
    //      - Se pueden incluir fragmentos aleatorios de la iguiente manera:
    //          RANDOM n o_1 o_2 ... o_x
    //        Donde n indica el número de fragmentos y o_i indica el índice del objeto que puede contener(#.png). Por
    //        defecto no hay objeto.
    //      - Finalmente para indicar el final del mapa se debe incluir END.
    //      - Ejemplo de fichero:
    //
    //          /* Mapa 1 */
    //
    //          107 107 107  /* Road RGB color 1 */
    //          105 105 105  /* Road RGB color 2 */
    //           16 200  16  /* Grass RGB color 1 */
    //            0 154   0  /* Grass RGB color 2 */
    //          255 255 255  /* Rumble RGB color */
    //          255 255 255  /* Dash RGB color */
    //
    //          /*
    //           * ROAD:
    //           *   1º Opcional: +   ;Indica que es un objeto repetido infinitamente hacia la izquierda. Por defecto no se repite.
    //           *   2º Opcional: #   ;Indica el índice del objeto colocado a la izquierda de la carretera (#.png). Por defecto no hay objeto.
    //           *   3º Opcional: #.# ;Indica el offset desde el borde de la carretera hasta el objeto. Por defecto es 0.0.
    //           *   4º Obligado: -   ;Representa la carretera
    //           *   5º Opcional: +   ;Indica que es un objeto repetido infinitamente hacia la derecha. Por defecto no se repite.
    //           *   6º Opcional: #   ;Indica el índice del objeto colocado a la derecha de la carretera (#.png). Por defecto no hay objeto.
    //           *   7º Opcional: #.# ;Indica el offset desde el borde de la carretera hasta el objeto. Por defecto es 0.0.
    //           */
    //          ROAD           -
    //          ROAD     5     -
    //          CURVE 0.5  /* Curva con índice comprendido entre -0.9 y 0.9, negativo si es hacia la izquierda y positivo si es hacia la derecha */
    //          ROAD           -   5
    //          ROAD     5 0.0 -   5 2.0
    //          STRAIGHT  /* Recta */
    //          ROAD   + 5     -
    //          CLIMB 1.0  /* Subida con índice comprendido entre 0.0 y MAX_FLOAT */
    //          ROAD           - + 5 -1.0
    //          FLAT  /* Llano, sin subidas ni bajadas */
    //          ROAD       -
    //          ROAD       -
    //          RANDOM 10 5 4  /* Añade 10 fragmentos aleatorios que pueden contenrr los objetos 5 y 4 */
    //          ROAD       -
    //          ROAD       -
    //          ROAD       -
    //          DROP 1.0  /* Bajada con índice comprendido entre 0.0 y MAX_FLOAT */
    //          ROAD       -
    //          ROAD       -
    //          END  /* Obligatorio */
    //
    /**
     * @param c
     * @param path
     * @param bgName
     * @param objectNames
     * @param random
     * @param time
     */
    Map(Config &c, const std::string &path, const std::string &bgName,
        const std::vector<std::string> &objectNames, bool random, int time);

    /**
     * Crea un mapa recto y llano con la configuración de map y partiendo de los objetos comunes de mapCommon para
     * la animación inicial. Devuelve la posición del abanderado y del semáforo.
     * @param map
     * @param flagger
     * @param semaphore
     */
    Map(const Map &map, int &flagger, int &semaphore);

    /**
     * Crea un mapa recto y llano con la configuración de map y partiendo de los objetos comunes de mapCommon para
     * la animación final. Devuelve la posición del abanderado y del final de la animación.
     * @param flagger
     * @param goalEnd
     */
    Map(int &flagger, int &goalEnd);

    /**
     * Copia los colores y el fondo de map.
     * @param map
     */
    void setColors(const Map &map);

    /**
     * Incrementa el índice del sprite en la línea line si existe.
     * @param line
     * @param right spriteRight o spriteLeft
     * @param increment
     */
    void incrementSpriteIndex(int line, bool right, int increment = 1);

    /**
     * Añade un mapa a continuación del actual.
     * @param map
     */
    void addNextMap(Map *map);

    /**
     * Añade una bifurcación del mapa actual a los mapas asignados.
     * @param left
     * @param right
     */
    void addFork(Map *left, Map *right);

    /**
     * Añade el offset al mapa.
     * @param yOffset
     */
    void setOffset(float yOffset);

    /**
     * Establece la posición de la cámara.
     * @param pX, donde pX = 0 es el medio de la carretera
     * @param pY, donde pY >= 0 AND pY <= MAXLINES
     */
    void updateView(float pX, float pY);

    /**
     * Devuelve la coordenada X de la cámara.
     * @return
     */
    float getCamX() const;

    /**
     * Devuelve la coordenada Y de la cámara.
     * @return
     */
    float getCamY() const;

    /**
     * Dibuja el fragmento del mapa actual dada la posición de la cámara establecida con la función updateView() y los
     * vehículos en él.
     * @param c
     * @param vehicles
     */
    void draw(Config &c, std::vector<Enemy> &vehicles);

    /**
     * Devuelve true si la posición del vehículo corresponde a algún objeto del fragmento del mapa actual o se ha salido
     * de los límites del mapa. En caso de que sea true, también devuelve la posición Y de la colisión.
     * @param c
     * @param prevY
     * @param currentY
     * @param currentX
     * @param minX
     * @param maxX
     * @param crashPos
     * @return
     */
    bool hasCrashed(const Config &c, float prevY, float currentY, float currentX, float minX, float maxX,
                    float &crashPos) const;

    /**
     * Devuelve true si currentX está fuera de la carretera.
     * @param currentX
     * @param currentY
     * @return
     */
    bool hasGotOut(float currentX, float currentY) const;

    /**
     * Devuelve el coeficiente de curvatura correspondiente al rectángulo currentY. El coeficiente es positivo si la
     * curva es hacia la derecha, negativo si es hacia la izquierda y 0 si es una recta.
     * @param currentY
     * @return coeff pertenece [-0.9, 0.9]
     */
    float getCurveCoefficient(float currentY) const;

    /**
     * Devuelve la elevación correspondiente al rectángulo currentY en base al rectángulo previo.
     * @param currentY
     * @return
     */
    Vehicle::Elevation getElevation(float currentY) const;

    /**
     * Devuelve cierto si se ha alcanzado el final del mapa.
     * @return
     */
    bool isOver() const;

    /**
     * Devuelve la longitud máxima del mapa.
     * @return
     */
    float getMaxY() const;

    /**
     * Devuelve el offset de la carretera en x .
     * @return
     */
    float getOffsetX() const;

    /**
     * Devuelve true si está en una bifurcación.
     * @param currentY
     * @return
     */
    bool inFork(float currentY) const;

    /**
     * Devuelve el siguiente mapa o NULL si es el final.
     * @return
     */
    Map *getNext() const;

    /**
     * Devuelve true si es el mapa inicial con la animación.
     * @return
     */
    bool isInitMap() const;

    /**
     * Devuelve true si es el mapa final con la animación.
     * @return
     */
    bool isGoalMap() const;

    /**
     * Devuelve el tiempo máximo del mapa.
     * @return
     */
    int getTime() const;
};


#endif //OUTRUN_MAP_HPP
