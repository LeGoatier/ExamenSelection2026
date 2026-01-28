"""
Robot Rescue Challenge - Solution Template

Implement your solution in the `solve` function below.
Your goal is to rescue the person trapped in the building as quickly as possible.

Available Robot methods:
    - robot.move(Direction) -> bool: Move in a direction (FORWARD, BACKWARD, LEFT, RIGHT)
    - robot.sense_fires_around() -> int: Get count of fires in adjacent cells (only cardinal directions, no diagonals) (does not cost time)
    - robot.scan_fires() -> Set[Position]: Get fire positions in cells around the robot (costs 10 seconds)
    - robot.position -> Position: Current robot position
    - robot.is_carrying_person -> bool: Whether robot is carrying someone
    - robot.get_grid_dimensions() -> Tuple[int, int]: Get (width, height)
    - robot.get_exit_position() -> Position: Get exit position
    - robot.get_person_position() -> Position: Get the person's position (known location)

Movement costs:
    - Each move: 1 second
    - Scan: 10 seconds

Rules:
    - There is exactly one person to rescue
    - The person's location is known from the start
    - Stepping on fire destroys the robot (mission fails immediately)
    - Robot starts at the exit position
    - Person is picked up automatically when robot reaches their cell
    - Mission ends automatically when robot returns to exit with the person

Objective: Navigate to the person, pick them up, and return to the exit as quickly as possible!
"""

from robot import Robot, Direction, Position
from typing import List, Set


def choseMovement(robot: Robot, target: Position, safe_positions: List[Position], fire_positions: List[Position], moves_to_person: List[Direction], explored_positions: Set[Position]):
    horizontal_steps = target.x - robot._position.x
    vertical_steps = target.y - robot._position.y
    explored_positions.add(robot.position)

    fires_sensed = robot.sense_fires_around()

    right_position = Position(robot.position.x + 1, robot.position.y)
    left_position = Position(robot.position.x - 1, robot.position.y)
    down_position = Position(robot.position.x, robot.position.y + 1)
    up_position = Position(robot.position.x, robot.position.y - 1)
    
    orthogonal_positions = {right_position, left_position, down_position, up_position}
    valid_orthogonal_positions = list(filter(lambda pos: pos.x >= 0 and pos.y >= 0 and pos.x <= robot.get_grid_dimensions()[0] and pos.y <= robot.get_grid_dimensions()[1], orthogonal_positions))
    unknown_orthogonal_positions = list(filter(lambda pos: (pos not in safe_positions and pos not in fire_positions), valid_orthogonal_positions))
    
    # Détection avec fires sensed pour mettre à jour les feux qu'on connait
    if fires_sensed == 0:
        addSafePositions(robot.position, safe_positions)
    else:
        #On doit calculer les feux qu'on sait déjà qui se trouvent autour de nous
        known_fires = 0
        for pos in orthogonal_positions:
            if pos in fire_positions:
                known_fires += 1
        if known_fires == fires_sensed:
            for pos in orthogonal_positions:
                if pos not in fires_sensed:
                    safe_positions.append(pos)
        # Le module suivant ne semble pas fonctionner mais j'ai pas le temps de figure out pourquoi
        if len(unknown_orthogonal_positions) == fires_sensed - known_fires:
            fire_positions.append(unknown_orthogonal_positions)

    
    #1 Si on peut se déplacer dans une direction qu'on souhaite, on le fait (greedy)
    if horizontal_steps > 0:
        if right_position in safe_positions and right_position not in explored_positions:
            robot.move(Direction.RIGHT)
            moves_to_person.append(Direction.RIGHT)
            return
    elif horizontal_steps < 0:
        if left_position in safe_positions and left_position not in explored_positions:
            robot.move(Direction.LEFT)
            moves_to_person.append(Direction.LEFT)
            return
    
    if vertical_steps > 0:
        if down_position in safe_positions and down_position not in explored_positions:
            robot.move(Direction.BACKWARD)
            moves_to_person.append(Direction.BACKWARD)
            return
    elif vertical_steps < 0:
        if up_position in safe_positions and up_position not in explored_positions:
            robot.move(Direction.FORWARD)
            moves_to_person.append(Direction.FORWARD)
            return
        


    #2 faire la danse éventuellement
    #si on est ici, c'est que aucun des déplacements qu'on voulait faire n'a fonctionné
    # On va donc regarder pour faire un déplacement qu'on est capable de faire peu importe
    if(horizontal_steps == 0):
        if left_position in safe_positions and left_position not in explored_positions:
            robot.move(Direction.LEFT)
            moves_to_person.append(Direction.LEFT)
            return
        elif right_position in safe_positions and right_position not in explored_positions:
            robot.move(Direction.RIGHT)
            moves_to_person.append(Direction.RIGHT)
            return
        
    if(vertical_steps == 0):
        if up_position in safe_positions and up_position not in explored_positions:
            robot.move(Direction.FORWARD)
            moves_to_person.append(Direction.FORWARD)
            return
        elif down_position in safe_positions and down_position not in explored_positions:
            robot.move(Direction.BACKWARD)
            moves_to_person.append(Direction.BACKWARD)
            return

    #3 Scanner et ajuster les safe positions et les fire positions
    # Si on se rend ici c'est qu'on sait qu'il y a un feu mais on ne sait pas il se trouve où
    fires = robot.scan_fires()
    fire_positions.append(fires)
    #On note aussi les cases adjacentes qui ne sont pas des feux
    p = robot.position
    adjacentPositions = [Position(p.x-1, p.y-1), Position(p.x, p.y-1), Position(p.x+1, p.y-1), Position(p.x-1, p.y), Position(p.x+1, p.y), Position(p.x-1, p.y+1), Position(p.x, p.y+1), Position(p.x+1, p.y+1)]
    for pos in adjacentPositions:
        if pos not in fires:
            safe_positions.append(pos)

    return


def addSafePositions(pos: Position, safePos: List[Position]):
    safePos.append(Position(pos.x, pos.y+1))
    safePos.append(Position(pos.x, pos.y-1))
    safePos.append(Position(pos.x+1, pos.y))
    safePos.append(Position(pos.x-1, pos.y))

        
def inversePath(robot: Robot, moves: List[Direction]):
    while len(moves) > 0:
        dir = moves.pop()
        if(dir == Direction.RIGHT):
            robot.move(Direction.LEFT)
        elif(dir == Direction.LEFT):
            robot.move(Direction.RIGHT)
        elif(dir == Direction.FORWARD):
            robot.move(Direction.BACKWARD)
        else:
            robot.move(Direction.FORWARD)

def solve(robot: Robot) -> None:
    """
    Implement your rescue algorithm here.

    Args:
        robot: The robot instance to control

    Note:
        The mission ends automatically when you return to the exit with the person.
        If the robot steps on fire, the mission fails immediately.
    """
    # TODO: Implement your solution here

    # Example: Get grid info
    width, height = robot.get_grid_dimensions()
    exit_pos = robot.get_exit_position()
    person_pos = robot.get_person_position()

    safe_positions = [exit_pos, person_pos]
    fire_positions = []
    explored_positions = {exit_pos}
    moves_to_person = []
    
    attemps = 0
    # Navigate to person and return to exit - mission ends automatically!
    while not robot.is_carrying_person and attemps < 50:
        choseMovement(robot, person_pos, safe_positions, fire_positions, moves_to_person, explored_positions)
        attemps +=1

    inversePath(robot, moves_to_person)
