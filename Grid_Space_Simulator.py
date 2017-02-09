#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created by Chukwunyere Igbokwe on February 09, 2017 by 3:27 AM

import networkx as nx
import pygame as pg


class GridSpaceSimulator:
    def __init__(self,width=600,height=600):
        self.width = width
        self.height = height
        self.cell_size = (20,20)
        self.screen = pg.display.set_mode((self.width,self.height ))
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.G = self._2d_grid()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.obstacle_weight = 1000
        self.start_cell = None
        self.goal_cell = None
        self.barrier_cell = None
        self.barriers = []
        #Flags
        self.start_flag = False
        self.goal_flag = False
        self.obstacle_flag = False
        self.solved = False
        #colours
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)


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
        # User clicks the mouse. Get the position
        self.mouse = pg.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = self.mouse[0] // self.cell_size[0] - 1
        row = self.mouse[1] // self.cell_size[1] - 1
        return (row, column)

    def _set_barrier_weights(self):
        barrier_node = self._get_target()
        for i in self.G.edges(barrier_node):
            self.G.edge[i[0]][i[1]]['weight'] = self.obstacle_weight

    def _draw_cell(self,colour):
        self.mouse = pg.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = self.mouse[0] // self.cell_size[0] - 1
        row = self.mouse[1] // self.cell_size[1] - 1
        p_column = (column + 1) * self.cell_size[0]
        p_row = (row + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, colour, (p_column, p_row, self.cell_size[0], self.cell_size[1]))
        return (row, column)

    def _clear_cell(self,cell):
        p_column = (cell[0] + 1) * self.cell_size[0]
        p_row = (cell[1] + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, self.BLACK, (p_row, p_column, self.cell_size[0], self.cell_size[1]))

    def _draw_path(self,cell):
        p_column = (cell[0] + 1) * self.cell_size[0]
        p_row = (cell[1] + 1) * self.cell_size[0]
        pg.draw.rect(self.screen, self.WHITE, (p_row, p_column, self.cell_size[0], self.cell_size[1]))

    def run(self):
        board = self.initBoard(self.screen)
        done = False
        while not done:
            self.clock.tick(self.fps)
            pg.display.update()
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                self.screen.blit(board, (0, 0))
                pg.display.flip()
                if event.type == pg.QUIT:
                    done = True

                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.start_flag == False and event.button == 1 and self.solved == False:
                    self.start_cell = self._draw_cell(self.RED)
                    print 'start cell ', self.start_cell
                    self.start_flag = True
                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.goal_flag == False and event.button == 1 and self.solved == False:
                    self.goal_cell = self._get_target()

                    if self.goal_cell == self.start_cell:
                        print "Nope"
                        self.goal_cell == None
                    else:
                        self.goal_cell = self._draw_cell(self.GREEN)
                        print 'goal cell ', self.goal_cell
                        self.goal_flag = True

                elif event.type == pg.MOUSEBUTTONDOWN and pg.Rect(20, 20, self.width - self.cell_size[0] * 2, self.height - self.cell_size[1] * 2).collidepoint(
                        pos) and self.start_flag == True and self.goal_flag == True and event.button == 1 and self.solved == False:
                    self.barrier_cell = self._get_target()
                    if self.barrier_cell == self.start_cell or self.barrier_cell == self.goal_cell:
                        self.barrier_cell = None
                    else:
                        self.barrier_cell = self._draw_cell(self.BLUE)
                        print 'barrier cell ', self.barrier_cell
                        # print type(barrier_cell)
                        self.barriers.append(self.barrier_cell)
                        # obstacle_flag = True

                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.start_flag == True and self.goal_flag == True and self.solved == False:
                    obstacle_flag = True
                    for i in self.barriers:
                        self._set_barrier_weights(i)
                    check = nx.has_path(self.G, self.start_cell, self.goal_cell)
                    print self.G.edges(data=True)
                    # print check
                    if check:
                        path = nx.astar_path(self.G, self.start_cell, self.goal_cell)
                        if set(path).intersection(self.barriers) == set():

                            # print path
                            for i in path:
                                if i == path[0] or i == path[-1]:
                                    pass
                                else:
                                    self._draw_path(i)
                        else:
                            print "No path found"
                    else:
                        print "No path found"

                    self.start_flag = False
                    self.goal_flag = False
                    self.obstacle_flag = False
                    self.solved = True

                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.solved == True:
                    to_be_cleared = self.barriers + path
                    for i in to_be_cleared:
                        self._clear_cell(i)
                    self.start_cell = self.goal_cell = self.barrier_cell = None
                    self.barriers = []
                    self.solved = False
                    path = None

                elif event.type == pg.KEYDOWN and event.key == pg.K_r and self.solved == True:
                    to_be_cleared = self.barriers + path[1:-1]
                    for i in to_be_cleared:
                        self._clear_cell(i)
                    self.barriers = None
                    self.barriers = []
                    self.start_flag = self.goal_flag = True
                    self.solved = False
                    path = None
        pg.quit()


x = GridSpaceSimulator()
x.run()
