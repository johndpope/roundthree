from flask import Flask, request, redirect
import twilio.twiml
from Node import Node
import datetime
import time
 
app = Flask(__name__)
start_node = None
vitals_introduction_node = None
loc_node = None
hr_node = None
rr_node = None
pupil_node = None
skin_node = None
vitals_nodes = [vitals_introduction_node, loc_node, hr_node, rr_node, pupil_node, skin_node]
curr_nodes = {}



@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    global curr_nodes
    resp = twilio.twiml.Response()
    if (request.form['From'] in curr_nodes):
        answer = request.form['Body'].lower()
        if (answer in ["y", "n"]):
            if(not curr_nodes[request.form['From']].is_end_node()):
                curr_nodes[request.form['From']] = curr_nodes[request.form['From']].get_next_node(answer)
        if (curr_nodes[request.form['From']] in vitals_nodes):
            curr_nodes[request.form['From']] = curr_nodes[request.form['From']].get_next_node("next")
    else:
        curr_nodes[request.form['From']] = start_node
        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
        print(start_time)
    resp.message(curr_nodes[request.form['From']].get_message())

    return str(resp)
 
if __name__ == "__main__":

    start_node = Node("Welcome to Cavalry. If you have not done so already, please call emergency services. Are you able to safely assist your patient? (y/n)")
    leave_node = Node("Please get to a place where you feel safe and do not attempt to administer care.")
    # conscious_node = Node("Is your patient visibily conscious? (y/n)")

    air_node = Node("Look in your patient's mouth. Are there any obstructions? If there are, remove it if possible. Is the airway now open? (y/n)")
    heimlich_node = Node("Perform the Heimlich maneuver: Get behind your patient. Place your fist with your thumb in and facing their belly button. Grasping your fist with your other hand, make quick, upward and inward thrusts with your fist. Has the object been dislodged? (y/n)")
    breathing_node = Node("Is your patient breathing? (y/n)")
    mtm_node = Node("If you have the ability to do so safely, administer rescue breaths at a rate of two breaths per minute.")
    circulation_node = Node("Does your patient have a pulse? (y/n)")
    cpr_node = Node("Administer hands-only CPR at a rate of 100 beats per minute. This is approximately the beat to the hit song \"Staying Alive\"")
    dense_bleed_node = Node("Does your patient have a dense bleed? Check for large pools of blood. (y/n)")
    stop_bleed_node = Node("Apply pressure to the wound with a bulky dressing.")
    vitals_introduction_node = Node("Do you wish to take a set of vitals (recommended)? (y/n)")
    wait_node = Node("Wait for emergency medical services to arrive.")

    # vitals_instructions_node = Node("Select the vital you wish to input.\n1 Level of Consciousness\n2 Heart Rate\n3 Respitory Rate\n4 Pupil Dilation\n5 Skin Condition")
    loc_node = Node("Which best describes your patient?\nAO4 A+Ox4\nV Responsive to Verbal Input\nP Responsive to Painful Stimulus\nU Unresponsive")
    hr_node = Node("Please enter your patient's approximate heart rate in beats per minute.")
    rr_node = Node("Please enter your patient's approximate breathing rate in breaths per minute.")
    pupil_node = Node("Check your patient's pupils, if possible. Put \"PERRL\" if your patient's Pupils are Equal, Round, and Responsive to Light. Otherwise, put \"Other\".")
    skin_node = Node("Asses your patient's skin condition. Enter \"PWD\" if it is Pink, Warm, and Dry. Otherwise, put \"Other\".")
    vitals_purgatory_node = Node("You have taken a full set of vitals. Do you wish to take another (recommended every 5-10 minutes)? (y/n)")


    start_node.add_response("y", air_node)
    start_node.add_response("n", leave_node)
    leave_node.set_is_end_node(True)

    air_node.add_response("y", breathing_node)
    air_node.add_response("n", heimlich_node)
    heimlich_node.add_response("y", breathing_node)
    heimlich_node.add_response("n", cpr_node)
    cpr_node.set_is_end_node(True)
    breathing_node.add_response("y", circulation_node)
    breathing_node.add_response("n", mtm_node)
    circulation_node.add_response("y", dense_bleed_node)
    circulation_node.add_response("n", cpr_node)
    dense_bleed_node.add_response("y", stop_bleed_node)
    dense_bleed_node.add_response("n", vitals_introduction_node)
    stop_bleed_node.set_is_end_node(True)
    vitals_introduction_node.add_response("y", loc_node)
    vitals_introduction_node.add_response("n", wait_node)

    loc_node.add_response("next", hr_node)
    hr_node.add_response("next", rr_node)
    rr_node.add_response("next", pupil_node)
    pupil_node.add_response("next", skin_node)
    skin_node.add_response("next", vitals_purgatory_node)
    vitals_purgatory_node.add_response("y", loc_node)
    vitals_purgatory_node.add_response("n", wait_node)
    wait_node.set_is_end_node(True)

    app.run(debug=True, host='0.0.0.0')
