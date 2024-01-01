#Pablo Alvarez - 2018

#Import modules

import math
import pygame


# Definition of colours

red_range = [[210,x,x] for x in range(210,0,-10)]
red = (238,72,72)
blue = (47, 77, 227)
background =(50, 50, 50)
yellow = (255,255,0)
green = (0,255,0)
global_rest_length = 0

# Definition of all the classes

class particle():
    def __init__(self, location, speed, aceleration, radius, fixed=False, force=[0, 0], mass=1):
        self.fixed = fixed
        self.location = location
        if self.fixed == True:
            self.speed = [0, 0]
        else:
            self.speed = speed
        if self.fixed == True:
            self.colour = red
            self.aceleration = [0, 0]
        else:
            self.aceleration = aceleration
            self.colour = blue
        self.force = force
        self.radius = radius
        self.mass = mass
        self._edges = []

    def displacement(self, time_frame):

        # Measure the displacement of a particle during a time frame
        if self.fixed == False:
            return ((self.speed[0] * time_frame) ** 2 + (self.speed[1] * time_frame) ** 2) ** 0.5
        else:
            return 0

    def update_location(self, time_frame):

        # Updates location of particles

        if self.fixed == False:
            self.location[0] += self.speed[0] * time_frame
            self.location[1] += self.speed[1] * time_frame
        else:
            pass

    def update_colour(self):

        # Updates color based on whether particle sif fixed or not
        if self.fixed == True:
            self.colour = red
        else:
            self.colour = blue

    def update_speed(self, time_frame):

        #Updates speeds according to acceleration, speed is reduced according to the damping value

        self.speed[0] += self.aceleration[0] * time_frame
        if self.speed[0] > 0:
            self.speed[0] -= damping * abs(self.speed[0])
        else:
            self.speed[0] += damping * abs(self.speed[0])
        self.speed[1] += self.aceleration[1] * time_frame
        if self.speed[1] > 0:
            self.speed[1] -= damping * abs(self.speed[1])
        else:
            self.speed[1] += damping * abs(self.speed[1])

    def update_aceleration(self):

        #Updates acceleration according to net force

        self.aceleration = [self.force[0] / self.mass, self.force[1] / self.mass]

    def draw(self, surface):

        #Draws particle in given canvas

        return pygame.draw.circle(surface, self.colour, map(int, self.location), self.radius, )

    def swap_fixed(self):

        # Change fix property.

        self.fixed = not self.fixed
        self.update_colour()

    def update_forces(self):

        # First a down force equal to mass*G is applied, after that the forces of all the edges connected with the
        # particle are calculated and included in the .force property.

        self.force = [0,self.mass*9.8]
        for i in self._edges:
            force_edge = i.calculate_force()
            if self == i.end:
                other_point = i.ini
            else:
                other_point = i.end
            if self.location[0] > other_point.location[0]:
                force_edge[0] = -abs(force_edge[0])
            else:
                force_edge[0] =  abs(force_edge[0])
            if self.location[1] > other_point.location[1]:
                force_edge[1] = -abs(force_edge[1])
            else:
                force_edge[1] =  abs(force_edge[1])
            if i.compression():
                force_edge[0],force_edge[1] = -force_edge[0], -force_edge[1]
            self.force[0]+= force_edge[0]
            self.force[1]+= force_edge[1]
    def remove_edge(self,edge_to_clean):

        # Clean a given edge from the ._edges property

        if edge_to_clean in self._edges:
            self._edges.remove(edge_to_clean)


class edge():

    def __init__(self, ini, end, rest_length=global_rest_length, stiffness = 5, colour = red):
        self.ini = ini
        self.end = end
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.colour = red
        ini._edges.append(self)
        end._edges.append(self)

    def calculate_force(self):

        # Calculate the change in length according to the rest length, the total force and the x,y components

        length = ((self.ini.location[0] -  self.end.location[0])**2 + (self.ini.location[1] -  self.end.location[1])**2)**0.5
        delta_x = (self.ini.location[1] -  self.end.location[1])
        delta_y = (self.ini.location[0] -  self.end.location[0])
        if delta_y != 0:
            angle = math.atan(delta_x/ delta_y)
        else:
            angle = 0
        delta_l =  length -  self.rest_length
        force = delta_l * self.stiffness
        force_components = [ force*math.cos(angle), force*math.sin(angle)]
        return force_components

    def strech_value(self):

        #Calculates the change in length

        length = ((self.ini.location[0] - self.end.location[0]) ** 2 + (
                    self.ini.location[1] - self.end.location[1]) ** 2) ** 0.5
        delta_l = length - self.rest_length

        return delta_l

    def compression(self):

        # Checks if edge is under tension or compression

        delta_l = self.strech_value()

        if delta_l >=0:
            return False
        else:
            return True

    def draw(self,screen):

        # Draw line in given canvas

        return pygame.draw.line(screen, self.colour, [self.ini.location[0], self.ini.location[1]],\
                                [self.end.location[0],self.end.location[1]])

    def update_colour(self):

        # Update color of edge  according the strech value

        value = self.strech_value()
        index = min(int(value/10), len(red_range)-1)
        self.colour = red_range[index]

    def distance_from_point_less_than(self, point, value):

        # Calculates distance between given point and edge, used to select edges with mouse

        def points_along(self, value):
            delta_x = (self.end.location[0] - self.ini.location[0])
            delta_y = (self.end.location[1] - self.ini.location[1])
            length = (delta_x**2 + delta_y**2)**0.5
            number = max(int(2*(length/value)),1)
            delta_x = (self.end.location[0] - self.ini.location[0]) / number
            delta_y = (self.end.location[1] - self.ini.location[1]) / number
            points = [self.ini.location]
            for i in range(number - 1):
                new_point = [points[-1][0] + delta_x, points[-1][1] + delta_y]
                points.append(new_point)
            points.append(self.end.location)
            return points
        def distance_two_points (p1,p2):
            return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

        points = points_along(self, value)
        flag = False
        for i in points:
            if distance_two_points(i, point) < value:
                flag = True
        return flag


# Initiate pygame classes
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
display_dimension = (1000, 1000)

display_half_width = int(display_dimension[0]/2)
display_half_height = int(display_dimension[1] / 2)


gameDisplay = pygame.display.set_mode((display_dimension[0], display_dimension[1]))
pygame.display.set_caption("Cable simulator")

font = pygame.font.SysFont(None,  20)

def message_to_screen(msg, colour):
    screen_text = font.render(msg, True, colour)
    gameDisplay.blit(screen_text, [0, 0])

# Create initial particles and edges

def create_particles(ini_point, end_point, number, particle_list, edge_list):

    # Create particles and edges between two points and appends them in the provided lists

    delta_x= (end_point[0] - ini_point[0])/number
    delta_y = (end_point[1] - ini_point[1])/number
    mass_val= 10.0/number
    points = [ini_point]
    for i in range(number-1):
        new_point  = [points[-1][0]+delta_x, points[-1][1] + delta_y]
        points.append(new_point)
    points.append(end_point)
    particles=[]
    for i in points:
        part = particle([int(i[0]), int(i[1])], [0,0], [0,0],8, mass= mass_val)
        particles.append(part)
    particles[0].swap_fixed()
    particles[-1].swap_fixed()
    for i in particles:
        particle_list.append(i)
    for i in range(len(particles)-1):
        edge_1 = edge( particles[i], particles[i+1])
        edge_list.append(edge_1)

def add_particles_line(ini_particle, end_particle, number, particle_list, edge_list):

    # Create new chain and connects the end to existing chane at the given particles

    ini_point = ini_particle
    end_point = end_particle.location
    delta_x= (end_point[0] - ini_point[0])/number
    delta_y = (end_point[1] - ini_point[1])/number
    mass_val= 10.0/number
    points = [ini_point]
    for i in range(number-1):
        new_point  = [points[-1][0]+delta_x, points[-1][1] + delta_y]
        points.append(new_point)
    particles=[]
    for i in points:
        part = particle([int(i[0]), int(i[1])], [0,0], [0,0],8, mass= mass_val)
        particles.append(part)
    particles[0].swap_fixed()
    for i in particles:
        particle_list.append(i)
    for i in range(len(particles)-1):
        edge_1 = edge( particles[i], particles[i+1])
        edge_list.append(edge_1)
    connection_edge = edge(particles[-1], end_particle )
    edge_list.append(connection_edge)

def chain_between_two_particles(ini_particle, end_particle, number, particle_list, edge_list):

    # Create new chain and connects the end to existing chane at the given particles

    ini_point = ini_particle.location
    end_point = end_particle.location
    delta_x = (end_point[0] - ini_point[0]) / number
    delta_y = (end_point[1] - ini_point[1]) / number
    points = [ini_point]
    for i in range(number - 1):
        new_point = [points[-1][0] + delta_x, points[-1][1] + delta_y]
        points.append(new_point)
    particles = []
    for i in points[1:]:
        part = particle([int(i[0]), int(i[1])], [0, 0], [0, 0], 8)
        particles.append(part)
    for i in particles:
        particle_list.append(i)
    for i in range(len(particles) - 1):
        edge_1 = edge(particles[i], particles[i + 1])
        edge_list.append(edge_1)
    connection_edge = edge(particles[-1], end_particle)
    connection_edge2 = edge(ini_particle, particles[0])
    edge_list.append(connection_edge2)
    edge_list.append(connection_edge)


particles=[]
edges=[]



# Main game logic

construction_mode =  False
pause = False
time_step =0.07
damping = 0.052
mouse_pos = [0, 0]
moving_particles = []
selected_edges = []
new_edge_nodes =[]

def game_loop():

    global particles, background, mouse_pos, moving_particles, construction_mode, red, blue, yellow, selected_edges,\
        edges, new_edge_nodes,pause, red_range



    while True:
        gameDisplay.fill(background)
        system_displacement = 0
        if not construction_mode:
            for i in range(len(particles)):
                if particles[i].fixed == False and particles[i] not in moving_particles and not pause:

                    # If not in construction mode or in pause, all the particles that are not fixed and are not selected
                    # are updated.

                    particles[i].update_forces()
                    particles[i].update_aceleration()
                    particles[i].update_speed(time_step)
                    system_displacement += particles[1].displacement(time_step)
                    particles[i].update_location(time_step)
                particles[i].draw(gameDisplay)
            for i in edges:
                if i not in selected_edges:
                    i.update_colour()
                i.draw(gameDisplay)
        if construction_mode:
            message_to_screen("Construction mode, click on the screen to add new cables. Finish by pressing space bar", red)
            for i in particles:
                i.draw(gameDisplay)
            for i in edges:
                i.draw(gameDisplay)
        if pause:
            message_to_screen("Simulation paused, resume by pressing enter", red)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and construction_mode==False:
                mouse_pos = pygame.mouse.get_pos()

                # Check mouse position and select particles and edges accordingly

                for i in particles:
                    if abs(i.location[0] - mouse_pos[0]) < i.radius and abs(i.location[1] - mouse_pos[1]) < i.radius:
                        i.colour = yellow
                        moving_particles.append(i)
                for edge_check in edges:
                    if edge_check.distance_from_point_less_than(mouse_pos, 5):
                        edge_check.colour = yellow
                        selected_edges.append(edge_check)

            if event.type == pygame.MOUSEBUTTONDOWN and construction_mode==True:

                #If in construction mode the mouse position is storage as the initial point for the new chain.
                #New chain is created

                mouse_pos= pygame.mouse.get_pos()
                appended = False
                for i in particles:
                    if abs(i.location[0] - mouse_pos[0]) < i.radius and abs(i.location[1] - mouse_pos[1]) < i.radius:
                        i.colour = green
                        appended = True
                        new_edge_nodes.append(i)
                if appended == False:
                    loc = [mouse_pos[0], mouse_pos[1]]
                    new_particle =  particle(loc,[0,0],[0,0],8)
                    new_particle.colour = green
                    new_particle.swap_fixed()
                    new_edge_nodes.append(new_particle)

                if len(new_edge_nodes)<2:
                    continue
                else:
                    try:
                        number_particles = int(input("Type number of divisions(minimum 2): "))
                    except:
                        number_particles = int(input("Type number of divisions(minimum 2): "))
                    chain_between_two_particles(new_edge_nodes[0],new_edge_nodes[1],number_particles,particles, edges)
                    if new_edge_nodes[0] not in particles:
                        particles.append(new_edge_nodes[0])
                    if new_edge_nodes[1] not in particles:
                        particles.append(new_edge_nodes[1])
                    new_edge_nodes = []

            last_post = mouse_pos
            if event.type == pygame.MOUSEMOTION:

                #Move selected particles following mouse movement

                event.pos
                movement = [last_post[0] - event.pos[0], last_post[1] - event.pos[1]]
                for part in moving_particles:
                    part.location[0] -= movement[0]
                    part.location[1] -= movement[1]
                mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                for i in moving_particles:
                    i.update_colour()
                for i in selected_edges:
                    i.update_colour()
                moving_particles = []
                selected_edges = []

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                #If right click change particles fixidity.

                for i in particles:
                    if abs(i.location[0] - mouse_pos[0]) < i.radius and abs(i.location[1] - mouse_pos[1]) < i.radius:
                        i.fixed = not i.fixed
                        i.update_colour()

            if event.type == pygame.KEYDOWN and event.key == 61:

                # Increase mass of selected particles

                for i in moving_particles:
                    i.mass = i.mass*1.5
                    i.radius += 1



            if event.type == pygame.KEYDOWN and event.key == 45:

                # Decrease mass of selected particles

                for i in moving_particles:
                    if i.mass>0.15:
                        i.mass = i.mass/1.5
                    if i.radius > 3:
                        i.radius -= 1


            if event.type == pygame.KEYDOWN and event.key == 61:

                # Increase stiffness of selected edges

                for i in selected_edges:
                    i.stiffness += 2


            if event.type == pygame.KEYDOWN and event.key == 45:

                # Decrease stiffness of selecetd edges

                for i in selected_edges:
                    i.stiffness = max(i.stiffness-2, 1)


            if event.type == pygame.KEYDOWN and event.key == 127:

                #Delete  selected edges and particles

                for i in moving_particles:
                    for u in i._edges:
                        if u in edges:
                            edges.remove(u)
                        for x in particles:
                            if x is not i:
                                x.remove_edge(u)
                    if i in particles:
                        particles.remove(i)
                for i in selected_edges:
                    for u in particles:
                        u.remove_edge(i)
                    if i in edges:
                        edges.remove(i)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    # Enter construction mode

                    new_edge_nodes = []
                    construction_mode  = not construction_mode
                    pause = False
                    if not construction_mode:
                        red = (238, 72, 72)
                        blue = (47, 77, 227)
                        background = (50, 50, 50)
                        yellow = (255, 255, 0)
                        red_range = [[210, x, x] for x in range(210, 0, -10)]
                    else:
                        red = (200, 200, 200)
                        blue = (80, 80, 80)
                        background = (20, 20, 20)
                        yellow = (255, 255, 0)
                        red_range = [[x, x, x] for x in range(255, 150, -10)]
                    for i in particles:
                        i.update_colour()
                    for i in edges:
                        i.update_colour()
            if event.type == pygame.KEYDOWN:

                # Enter pause mode

                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    pause = not pause
                    if pause:
                        background = (20,20,20)
                    else:
                        background = (50,50,50)
        pygame.display.update()
        clock.tick()



# Main loop will not start until enter key is pressed

while True:
    gameDisplay.fill(background)
    message_to_screen("Press enter to start simulation", red)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                game_loop()