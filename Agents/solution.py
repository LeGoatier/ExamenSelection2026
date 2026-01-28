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
from typing import List, Dict


def choseMovement(robot: Robot, target: Position, safe_positions: List[Position], fire_positions: List[Position]):
    horizontal_steps = target.x - robot._position.x
    vertical_steps = target.y - robot._position.y
    
    if robot.sense_fires_around() == 0:
        addSafePositions(robot.position, safe_positions)
        moveNormally(robot, target)
        return
    else:
        #1 regarder si on peut move à une safe position quand même
        if horizontal_steps > 0:
            target_horizontal = Position(robot.position.x + 1, robot.position.y)
            if target_horizontal in safe_positions:
                robot.move(Direction.RIGHT)
                return
        elif horizontal_steps < 0:
            target_horizontal = Position(robot.position.x - 1, robot.position.y)
            if target_horizontal in safe_positions:
                robot.move(Direction.LEFT)
                return
        
        if vertical_steps > 0:
            target_vertical = Position(robot.position.x, robot.position.y + 1)
            if target_vertical in safe_positions:
                robot.move(Direction.BACKWARD)
                return
        elif vertical_steps < 0:
            target_vertical = Position(robot.position.x, robot.position.y - 1)
            if target_vertical in safe_positions:
                robot.move(Direction.FORWARD)
                return
            


        #2 faire la danse éventuellement

        #3 Scanner et ajuster les safe positions et les fire positions
        # Si on se rend ici c'est qu'on sait qu'il y a un feu mais on ne sait pas il se trouve où
        print("Scanning fires")
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



def moveNormally(robot: Robot, target: Position):
    horizontal_steps = target.x - robot._position.x
    vertical_steps = target.y - robot._position.y
    if horizontal_steps > 0:
        robot.move(Direction.RIGHT)
    elif horizontal_steps < 0:
        robot.move(Direction.LEFT)
    elif vertical_steps > 0:
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
    
    attemps = 0
    # Navigate to person and return to exit - mission ends automatically!
    while robot._people_saved < 1 and attemps < 50:
        choseMovement(robot, exit_pos if robot.is_carrying_person else person_pos, safe_positions, fire_positions)
        attemps +=1
