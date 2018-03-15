# Vigil
Simple Alerts system

### Architecture
The main unit of Vigil is the 'Alert Channel'. It is the Alert Channel which is actvated by external systems that want to register an alert. The Alert Channel also holds the information about the current state of the alert (title, message, priority etc.).  
Each Alert Channel can be associated with one or more 'Alert Actions'. These are activities undertaken when the incoming alert is received, or is ongoing.   
