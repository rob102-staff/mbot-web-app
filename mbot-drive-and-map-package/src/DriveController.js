import React from 'react';
import { useState, useEffect } from 'react';
import roslib from 'roslib';
import './DriveController.css';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

function generateDriveMessage(button, speed) {
    let driveMessage = new roslib.Message({
        linear: {
            x: 0,
            y: 0,
            z: 0
        },
        angular: {
            x: 0,
            y: 0,
            z: 0
        }
    });
    switch (button) {
        case "forward":
            driveMessage.linear.x = speed;
            break;
        case "down":
            driveMessage.linear.x = -speed;
            break;
        case "left":
            driveMessage.angular.z = speed;
            break;
        case "right":
            driveMessage.angular.z = -speed;
            break;
        default:
            break;
    }
    return driveMessage;
};

/**
 * 
 * @param {*} props
 * @param {string} props.driveTopicName - ROS topic name for drive commands. Default is /cmd_vel
 * @param {function(string)} props.onButtonPress - Callback function for button press. Default is to send drive commands to ROS.
 *  The callback function should take a string argument, which is the button name. (forward, down, left, right)
 * @param {function(string)} props.onButtonRelease - Callback function for button release. Default is to send drive commands to ROS
 * The callback function should take a string argument, which is the button name. (forward, down, left, right)
 * @param {number} props.defaultSpeed - Default speed for drive commands. Default is 0.5
 * 
 * @returns Drive Controller component 
 */
function DriveController(props) {

    let onButtonPress;
    let onButtonRelease;
    let ros;
    let rosDriveTopic;
    useEffect(() => {
        ros = new roslib.Ros({
            url: 'ws://localhost:9090'
        })
        rosDriveTopic  = new roslib.Topic({
            ros: ros,
            name: props.driveTopicName ? props.driveTopicName : '/cmd_vel',
            messageType: 'geometry_msgs/Twist'
        });
    }, []);
    
    if (props.onButtonPress === undefined) {
        onButtonPress = (button) => { 
            let driveMessage = generateDriveMessage(button, 0.5);
            rosDriveTopic.publish(driveMessage);
        };
    } else {
        onButtonPress = props.onButtonPress;
    }
    if (props.onButtonRelease === undefined) {
        onButtonRelease = (button) => { 
            let driveMessage = generateDriveMessage(button, 0);
            rosDriveTopic.publish(driveMessage);
        };
    } else {
        onButtonRelease = props.onButtonRelease;
    }

    return (
        <div className="drive-controller">
            <div className="drive-controller-row">
                <button className="drive-controller-button"
                    onMouseDown={() => onButtonPress("forward")}
                    onMouseUp={() => onButtonRelease("forward")}>
                    <ArrowBackIcon className="drive-controller-arrow" style={{ transform: "rotate(90deg)" }} />
                </button>
            </div>
            <div className="drive-controller-row">
                <button className="drive-controller-button"
                    onMouseDown={() => onButtonPress("left")}
                    onMouseUp={() => onButtonRelease("left")}>
                    <ArrowBackIcon className="drive-controller-arrow" style={{ transform: "rotate(0deg)" }} />
                </button>
                <button className="drive-controller-button"
                    onMouseDown={() => onButtonPress("down")}
                    onMouseUp={() => onButtonRelease("down")}>
                    <ArrowBackIcon className="drive-controller-arrow" style={{ transform: "rotate(-90deg)" }} />
                </button>
                <button className="drive-controller-button"
                    onMouseDown={() => onButtonPress("right")}
                    onMouseUp={() => onButtonRelease("right")}>
                    <ArrowBackIcon className="drive-controller-arrow" style={{ transform: "rotate(180deg)" }} />
                </button>
            </div>
        </div>
    );

}

export default DriveController;