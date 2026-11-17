User Story
As an application developer, I want to tell whether a specified duration has elapsed since a given time, so that my application can trigger actions when a time limit expires.
Acceptance Criteria
Functional Requirements
1.	Given a 10 minute time limit starting at 3:00pm, when the microservice checks the timer at 3:08pm, then it reports the time limit has not expired.
2.	Given a 10 minute time limit starting at 3:00pm, when the microservice checks the timer at 3:11pm, then it reports the time limit has expired.
Quality Attributes & Non-Functional Requirements
Quality Attribute: Reliability
Given an invalid time submission, when the microservice processes it, then it returns an error and is ready to process new requests.

User Story
As a developer, I want to turn a number of minutes into hours and minutes so that the UI is easy to understand.
Acceptance Criteria
Functional Requirements
1.	Given the Time/Duration microservice is running, when I send 135 minutes, then it returns “2 hours and 15 minutes”.
2.	Given the microservice is running, when I send 45 minutes, then it returns “45 minutes”.
Quality Attributes & Nonfunctional Acceptance Criteria
Quality Attribute: Usability
Given 10 test values, including 60 and 61 minutes, when I send each one, then the result is written in full words with “hour” and “minute”.

User Story

As an application developer, I want to calculate the duration between two specified times so that my application can determine how much time has passed between two separate events.
Acceptance Criteria

Functional requirements
1.	Given the time duration microservice is running, when I send a start time of 2:00 PM and an end time of 3:30 PM, then it returns 1 hour 30 minutes.
2.	Given the time duration microservice is running, when I send a start time of 9:15 AM and an end time of 10:00 AM, then it returns 45 minutes.
3.	Given the time duration microservice is running, when I send a start time of 11:00 PM and an end time of 1:00 AM on the next day, then it returns 2 hours.
Quality attributes & Non-functional requirements
Quality Attribute: Performance
Given a valid request, when the microservice calculates a duration, then it returns the result within 1 second.
