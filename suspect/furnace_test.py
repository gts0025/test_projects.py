import pygame as pg
import menu_class
pg.init()
screen_size = [400, 400]
screen = pg.display.set_mode(screen_size)


# simple furnace game, where you need to smelt materials
# todo: 
#   main menu, where you can burn materials,
#   market whereyou can sell goods
#   state machine holding game variables like 
#   current cash, prices, coal, mineral, and bars, and furnace temperature
#   

#   some long term saving system
#   

# state machine
furnace_state = {
    "cash":10000,
    "mineral":10,
    "coal":1,
    "furnace-temp":1000,
    "furnace_insulation":0.998,
}

market_state = {
    "coal_price":10,
    "mineral_price":10,
    "coal_energy":100,
   
}



def sell_mineral(amount):
    if amount <= furnace_state["mineral"]:
        furnace_state["mineral"] -= amount
        furnace_state["cash"] += amount*market_state["mineral_price"]
        return True
    

def buy_coal(amount):
    if amount*market_state["coal_price"] <= furnace_state["cash"]:
        furnace_state["coal"] += amount
        furnace_state["cash"] -= amount*market_state["coal_price"]
        return True


buy_slider = menu_class.Slider("",[50,100,100,10]
    )

buy_button = menu_class.Button(
    "buy",[50,50,100,30]
    )


sell_button = menu_class.Button(
    "sell"
    )


sell_slider = menu_class.Slider(
    ""
    )

main_menu = menu_class.Menu(
    [
        sell_button,
        sell_slider,
        buy_slider,
        buy_button
    ]
)

def main_loop():
    run = 1
  
    while run:
        for Event in pg.event.get():
            if Event == pg.QUIT:
                run = 0
        if run:
            main_menu.run(run,screen)
            pg.display.flip()

main_loop()

    

    
