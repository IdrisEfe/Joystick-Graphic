import joygraph
import pygame
import time

def applyDeadZone(value: float, deadzone: float) -> float:
    return 0 if abs(value) < deadzone else value

def rampInput(targetValue: float, currentValue: float) -> float:
    return (targetValue - currentValue) * rampRate

DEAD_ZONE = 0.05
SPEED_FACTOR = 0.7
rampRate = 0.07

if __name__ == "__main__":

    currentForward = 0
    currentRotation = 0

    jg = joygraph.JoyGraph()
    js = jg.create_joystick(0)

    print(f"Joystick name: {js.get_name()}")
    print(f"Joystick index: {js.get_joystick_index()}")

    labels = ["Leader Left", "Follower Left", "Leader Right", "Follower Right"]
    g = jg.create_graph(labels, min_raw_value=-2, max_raw_value=2, factor=SPEED_FACTOR)

    target = [0.0, 0.0, 0.0, 0.0]
    current = [0.0, 0.0, 0.0, 0.0]

    try:
        while True:
            pygame.event.pump()
            rawRotation = js.get_axis(0)
            rawForward = -js.get_axis(1)

            targetForward = applyDeadZone(rawForward, DEAD_ZONE)
            targetRotation = applyDeadZone(rawRotation, DEAD_ZONE)

            targetForward *= SPEED_FACTOR
            targetRotation *= SPEED_FACTOR

            currentForward += rampInput(targetForward, currentForward)
            currentRotation += rampInput(targetRotation, currentRotation)

            #TARGET
            TargetLeft = targetForward + targetRotation
            TargetRight = targetForward - targetRotation

            LeftLeader_targetSpeed = TargetLeft
            LeftFollower_targetSpeed = TargetLeft

            RightLeader_targetSpeed = -TargetRight
            RightFollower_targetSpeed = -TargetRight
            #################

            #OUTPUT (CURRENT)
            leftOutput = currentForward + currentRotation
            rightOutput = currentForward - currentRotation

            leftLeader_speed = leftOutput
            leftFollower_speed = leftOutput

            rightLeader_speed = -rightOutput
            rightFollower_speed = -rightOutput
            #################

            target[0], target[1], target[2], target[3] = LeftLeader_targetSpeed, LeftFollower_targetSpeed, RightLeader_targetSpeed, RightFollower_targetSpeed
            current[0], current[1], current[2], current[3] = leftLeader_speed, leftFollower_speed, rightLeader_speed, rightFollower_speed

            g.update_chart(real_values=current, target_values=target)
            print(f"x: {rawRotation:.2f}, y: {rawForward:.2f}, targetLeftLeader: {LeftLeader_targetSpeed:.2f}, targetLeftFollower: {LeftFollower_targetSpeed:.2f}, targetRightLeader: {RightLeader_targetSpeed:.2f}, targetRightFollower: {RightFollower_targetSpeed:.2f}")
            time.sleep(0.01)


    except KeyboardInterrupt:
        print("Program has ended.")
    finally:
        pygame.quit()
