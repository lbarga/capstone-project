import heroes
from login import *
from treasure_hunt import *
from heroes import *
from timer import *
from captcha import *

# Implementar o rercuso de multi threads.
# Criar thread responsável pela atualização das telas.
# Criar thread que verifica se é necessário realizar o slider-captcha.

# Melhorar indentificação de login.
# Automatizar tentativas de login, quando conexão ficar ruim.

while True:
    solve_captcha()
    upgrade_current_screen()

    login_screen_button = in_login_screen()

    if login_screen_button.exist:
        login(login_screen_button)
    else:
        treasure_hunt_back_button = in_treasure_hunt_screen()
        heroes_upgrade_button = in_heroes_screen()

        if heroes.tired and not heroes.in_heroes:
            exit_treasure_hunt_screen()
            enter_in_heroes()

        if heroes_upgrade_button.exist and not heroes.in_character_section:
            set_characters_to_work()

        if treasure_hunt_back_button.exist and not heroes.tired:
            countdown()
            heroes.tired = True
        else:
            enter_in_treasure_hunt()