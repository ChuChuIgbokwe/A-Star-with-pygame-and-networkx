#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created by Chukwunyere Igbokwe on February 09, 2017 by 3:27 AM

import networkx as nx
import pygame as pg


class GridSpaceSimulator:
    def __init__(self,width=600,height=600):
        pg.init()
        self.width = width
        self.height = height
        self.cell_size = (20,20)
        self.screen = pg.display.set_mode((self.width,self.height ))
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.G = self._2d_grid()
        self.clock = pg.time.Clock()
        self.fps = 60
        pg.display.set_caption("Pathfinder")
        self.myfont = pg.font.SysFont('arial', 15)
        self.obstacle_weight = 1000
        self.start_cell = None
        self.goal_cell = None
        self.barrier_cell = None
        self.barriers = []
        self.path = None
        #Flags
        self.start_flag = False
        self.goal_flag = False
        self.obstacle_flag = False
        self.solved = False
        self.path_found = False
        #colours
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 175, 0)


    def initBoard(self,board):
        h_border = self.width - (self.cell_size[0] * 2)
        v_border = self.height - (self.cell_size[1] * 2)
        self.background.set_colorkey((255, 0, 255))
        self.background.fill((255, 0, 255), (20, 20, h_border, v_border))
        no_vertical_lines = ((self.width - 2 * self.cell_size[0]) / 20) + 1
        no_horizontal_lines = ((self.height - 2 * self.cell_size[1]) / 20) + 1
        for i in range(no_vertical_lines):
            self.background.fill((255, 0, 0), (20 + 20 * i, 20, 2, v_border))  # originally 242
        for i in range(no_horizontal_lines):
            self.background.fill((255, 0, 0), (20, 20 + 20 * i, h_border, 2))
        return self.background

    def _2d_grid(self):
        '''
        create 2D weighted grid graph
        :return:
        '''
        Graph = nx.Graph()
        no_vertical_lines = ((self.width - 2 * self.cell_size[0]) / 20) + 1
        no_horizontal_lines = ((self.height - 2 * self.cell_size[1]) / 20) + 1
        rows = range(no_vertical_lines - 1)
        columns = range(no_horizontal_lines - 1)
        Graph.add_nodes_from((i, j) for i in rows for j in columns)
        Graph.add_edges_from((((i, j), (i - 1, j)) for i in rows for j in columns if i > 0), weight=1)
        Graph.add_edges_from((((i, j), (i, j - 1)) for i in rows for j in columns if j > 0), weight=1)
        return Graph

    def _get_target(self):
        '''
        Get mouse position when clicked and convert it to grid coordinates
        :return:
        '''
        self.mouse = pg.mouse.get_pos() # User clicks the mouse. Get the position
        # Change the x/y screen coordinates to grid coordinates
        column = self.mouse[0] // self.cell_size[0] - 1
        row = self.mouse[1] // self.cell_size[1] - 1
        return (row, column)

    def _set_barrier_weights(self,cell):
        '''
        set the weight of all edges of an obstacle node to
        :param cell:
        :return:
        '''
        for i in self.G.edges(cell):
            self.G.edge[i[0]][i[1]]['weight'] = self.obstacle_weight

    def _dist(self,a, b):
        (x1, y1) = a
        (x2, y2) = b
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def _draw_cell(self,colour):
        '''
        Get mouse click, convert it to grid coordinates then fill it out with the appropriat colour
        :param colour:
        :return:
        '''
        self.mouse = pg.mouse.get_pos()
        column = self.mouse[0] // self.cell_size[0] - 1
        row = self.mouse[1] // self.cell_size[1] - 1
        p_column = (column + 1) * self.cell_size[0]
        p_row = (row + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, colour, (p_column, p_row, self.cell_size[0], self.cell_size[1]))
        return (row, column)

    def _clear_cell(self,cell):
        '''
        Clear out a filled grid. Used to reset the simulator
        :param cell:
        :return:
        '''
        p_column = (cell[0] + 1) * self.cell_size[0]
        p_row = (cell[1] + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, self.BLACK, (p_row, p_column, self.cell_size[0], self.cell_size[1]))

    def _draw_path(self,cell):
        '''
        Convert nodes to pixel coordinates and fill out the appropriate grid squares. ITht's Used for drawing the A star path on the simulator
        :param cell:
        :return:
        '''
        p_column = (cell[0] + 1) * self.cell_size[0]
        p_row = (cell[1] + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, self.WHITE, (p_row, p_column, self.cell_size[0], self.cell_size[1]))

    def _whipeout(self,cell):
        '''
        Convert nodes to pixel coordinates and fill out the appropriate grid squares. ITht's Used for drawing the A star path on the simulator
        :param cell:
        :return:
        '''
        p_column = (cell[0] + 1) * self.cell_size[0]
        p_row = (cell[1] + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, self.ORANGE, (p_row, p_column, self.cell_size[0], self.cell_size[1]))


    def _onscreen_instructions(self):
        if not self.start_flag and not self.solved:
            write1 = self.myfont.render("Place your start point", True, (255, 255, 255))
            self.screen.blit(write1, (10, 1))
        if self.start_flag and not self.goal_flag:
            write2 = self.myfont.render("Place your end point ", True, (255, 255, 255))
            self.screen.blit(write2, (10, 1))

        if self.start_flag and self.goal_flag:
            write3 = self.myfont.render("Add obstacles or press SPACEBAR to solve", 1, (255, 255, 255))
            self.screen.blit(write3, (10, 1))

        if self.solved:
            write4 = self.myfont.render("Press ENTER to restart simulator", 1, (255, 255, 255))
            self.screen.blit(write4, (10, 1))
            write5 = self.myfont.render("Press R to remove obstacles", 1, (255, 255, 255))
            self.screen.blit(write5, (1, self.height-self.cell_size[0]))

        if self.solved and  not self.path_found:
            write6 = self.myfont.render("No Path Found", 1, (255, 255, 255))
            self.screen.blit(write6, (450,1))
        if self.solved and self.path_found:
            write6 = self.myfont.render("Path Found", 1, (255, 255, 255))
            self.screen.blit(write6, (450, 1))
            write6 = self.myfont.render("Steps:{}".format(len(self.path)-1), 1, (255, 255, 255))
            self.screen.blit(write6, (450, self.height-self.cell_size[0]))

    def run(self):
        board = self.initBoard(self.screen)
        done = False
        while not done:
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                self.screen.blit(board, (0, 0))
                self._onscreen_instructions()

                if event.type == pg.QUIT:
                    done = True

                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.start_flag == False and event.button == 1 and self.solved == False:
                    self.start_cell = self._draw_cell(self.RED)
                    # print 'start cell ', self.start_cell
                    self.start_flag = True

                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.goal_flag == False and event.button == 1 and self.solved == False:

                    self.goal_cell = self._get_target()
                    if self.goal_cell == self.start_cell: #start cell cannot be goal cell
                        self.goal_cell == None
                    else:
                        self.goal_cell = self._draw_cell(self.GREEN)
                        # print 'goal cell ', self.goal_cell
                        self.goal_flag = True

                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.start_flag == True and self.goal_flag == True and event.button == 1 and self.solved == False:

                    self.barrier_cell = self._get_target()
                    if self.barrier_cell == self.start_cell or self.barrier_cell == self.goal_cell: #no obstacles in star or goal cell
                        self.barrier_cell = None
                    else:
                        self.barrier_cell = self._draw_cell(self.BLUE)
                        # print 'barrier cell ', self.barrier_cell
                        self.barriers.append(self.barrier_cell)

                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.start_flag == True and self.goal_flag == True and self.solved == False:
                    self.obstacle_flag = True
                    for i in self.barriers:
                        self._set_barrier_weights(i)
                    check = nx.has_path(self.G, self.start_cell, self.goal_cell) # check path exists
                    if check:
                        self.path = nx.astar_path(self.G, self.start_cell, self.goal_cell,heuristic=self._dist)
                        if set(self.path).intersection(self.barriers) == set():
                            self.path_found = True
                            print "A Star path = ", self.path
                            for i in self.path:
                                if i == self.path[0] or i == self.path[-1]: #Don't draw on start or goal
                                    pass
                                else:
                                    self._draw_path(i)
                        else:
                            print "NO PATH FOUND"
                            exempt = self.barriers + [self.start_cell] + [self.goal_cell]
                            for i in self.G.nodes():
                                if i not in exempt:
                                    self._whipeout(i)

                    else:
                        print "NO PATH FOUND"
                        exempt = self.barriers + [self.start_cell] + [self.goal_cell]
                        for i in self.G.nodes():
                            if i not in exempt:
                                self._whipeout(i)

                    self.start_flag = False
                    self.goal_flag = False
                    self.obstacle_flag = False
                    self.solved = True

                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.solved == True:
                    for i in self.G.nodes():
                        self._clear_cell(i)
                    self.start_cell = self.goal_cell = self.barrier_cell = None
                    self.barriers = []
                    self.solved = False
                    self.path = None
                    print 'SIMULATOR RESTARTED'

                elif event.type == pg.KEYDOWN and event.key == pg.K_r and self.solved == True:
                    exempt = [self.start_cell] + [self.goal_cell]
                    for i in self.G.nodes():
                        if i in exempt:
                            pass
                        else:
                            self._clear_cell(i)
                    self.barriers = None
                    self.barriers = []
                    self.start_flag = self.goal_flag = True
                    self.solved = False
                    self.path = None
                    print 'OBSTACLES REMOVED'
            pg.display.flip()
            self.clock.tick(self.fps)
        pg.quit()

x = GridSpaceSimulator()
x.run()
