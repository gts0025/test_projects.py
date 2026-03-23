import matplotlib.pyplot as plt



height = 0 # meters
speed = 0 # m/s
fuel_amount = 10  # liters
fuel_wheight = 0.1 #  kg/L
tank_wheight = 1  + 0.1*fuel_amount# kg 
fuel_residue = 0.1 # kg/kg
residue_amount = 0; # kg
burn_time = 0.7 # L/s
fuel_thrust = 100 # n/L
dt = 0.01 # s/step 
g = 9.8  # m/s**2
steps = 100 # simulation_steps
air_density = 0.1 # kg/m**3 pressure
air_viscosity = 0.001 # (m/s^2)/(m**2) sheering 
front_cross_section = 0.01 # m**2
side_cross_section = 0.2 + fuel_amount*0.1 # m**2



def set_initial():

    global height
    global speed
    global fuel_amount
    global fuel_residue
    global residue_amount
  


    height = 0 # meters
    speed = 0 # m/s
    fuel_amount = 10  # liters
    fuel_residue = 0.1 # kg/kg
    residue_amount = 0; # kg

  
    
   

def run(steps):

    global height
    global speed
    global fuel_amount
    global fuel_wheight
    global tank_wheight
    global fuel_residue
    global residue_amount
    global burn_time
    global fuel_thrust
    global dt
    global g
   

    height_graph = []
    time_graph = []
    max_height = 0
    init_fuel = fuel_amount
    for i in range(steps):
                 
            # rocket burn
        burned = min(burn_time*dt,fuel_amount)
      
        residue_amount += burned*fuel_wheight*fuel_residue
        fuel_amount -= burned
        m = tank_wheight + fuel_amount*fuel_wheight + residue_amount
       

        drag = air_density*front_cross_section*(speed*speed) + air_viscosity*side_cross_section*speed
        if speed < 0: 
            drag *= -1

        a = burned*fuel_thrust/m - g*dt - drag*dt 
        speed += a
        height += speed*dt

        
        
        if height + speed*dt < 0:
            speed *= -0.3
            height = 0
        height_graph.append(height)
        time_graph.append(i*dt)

        
            
        max_height = max(height, max_height)

        
    plt.plot(time_graph,height_graph,label = f"initial fuel: {init_fuel}")
    plt.legend()
   

plt.title("rocket lauch with different fuel amount")

set_initial()
dt = 0.01
fuel_amount = 10
run(round(80/dt))


set_initial()
dt = 0.01
fuel_amount = 5
run(round(80/dt))


set_initial()
dt = 0.01
fuel_amount = 2
run(round(80/dt))

set_initial()
dt = 0.01
fuel_amount = 1
run(round(80/dt))

set_initial()
dt = 0.01
fuel_amount = 0.5
run(round(80/dt))

set_initial()
dt = 0.01
fuel_amount = 0.2
run(round(80/dt))


set_initial()
dt = 0.01
fuel_amount = 0.1
run(round(80/dt))

plt.show()

