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


def choseMovement(robot: Robot, target: Position):
    if robot.sense_fires_around() == 0:
        moveNormally(robot, target)
    



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

    # Example: Check for nearby fires
    fire_count = robot.sense_fires_around()

    # Navigate to person and return to exit - mission ends automatically!
    while robot._people_saved < 1:
        choseMovement(robot, exit_pos if robot.is_carrying_person else person_pos)
