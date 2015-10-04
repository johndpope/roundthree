from flask import Flask, request, redirect
import twilio.twiml
from Node import Node
 
app = Flask(__name__)
start_node = None
air_node = None
curr_node = {}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    global curr_node
    resp = twilio.twiml.Response()
    if (request.form['From'] in curr_node):
        answer = request.form['Body'].lower()
        print(answer)
        if ("y" in answer or "n" in answer):
            curr_node[request.form['From']] = curr_node[request.form['From']].get_next_node(answer)
    else:
        curr_node[request.form['From']] = start_node
    resp.message(curr_node[request.form['From']].get_message())

    return str(resp)
 
if __name__ == "__main__":

    start_node = Node("Welcome to Cavalry. If you have not done so already, please call emergency services. Are you safe and able to assist? (y/n)")
    air_node = Node("Look in your patient's mouth. Are there any obstructions? If there are, remove it if possible. Is the airway now open? (y/n)")
    heimlich_node = Node("Perform the Heimlich maneuver: Get behind your patient. Place your fist with your thumb in and facing their belly button. Grasping your fist with your other hand, make quick, upward and inward thrusts with your fist.")
    breathing_node = Node("Is your patient breathing? (y/n)")
    mtm_node = Node("If you have the ability to do so safely, administer rescue breaths at a rate of two breaths per minute.")
    circulation_node = Node("Does your patient have a pulse? (y/n)")
    cpr_node = Node("Administer hands-only CPR at a rate of 100 beats per minute. This is approximately the beat to the hit song \"Staying Alive\"")
    dense_bleed_node = Node("Does your patient have a dense bleed? Check for large pools of blood. (y/n)")


	# heimlich_node.add_response("y", """""")
	# heimlich_node.add_response("n", """h-o CPR""")
    start_node.add_response("y", air_node)
    start_node.add_response("n", air_node)
    air_node.add_response("y", breathing_node)
    air_node.add_response("n", heimlich_node)
    breathing_node.add_response("y", circulation_node)
    breathing_node.add_response("n", mtm_node)
    circulation_node.add_response("y", dense_bleed_node)
    circulation_node.add_response("n", cpr_node)

    app.run(debug=True, host='0.0.0.0')
