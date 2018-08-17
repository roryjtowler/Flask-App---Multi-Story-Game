from flask import Flask, render_template, request, redirect
import ast

app = Flask(__name__)

master_story_dict = {}

# generate a ID for new child story
def generateChildID():
    dict_length = str(len(master_story_dict) + 1)
    return dict_length

# add a story as a parent story and add as a child to its corresponding parent story
def addStory(currentID, sentence, grid_square_pos):
    childID = generateChildID()
    childDict = {"sentence": sentence, "childID": childID}
    master_story_dict[childID] = {"middle": childDict, "top": None, "right": None, "bottom": None, "left": None, "parentID": currentID }
    master_story_dict[currentID][grid_square_pos] = childDict

# render home screen template
@app.route ('/')
def home():
    master_story_dict.clear();
    return render_template('home.html')

# creates a story when invoked
@app.route('/createStory',methods = ['POST'])
def createStory():
    childID = generateChildID()
    grid_square_pos = request.form['grid_square_pos']
    currentID = request.form['id']
    sentence = request.form['sentence']

    ci = int(currentID)
    chiID = int(childID)

    # check to see if the input is empty and if form is from home screen
    if(sentence == "" and currentID == childID):
        return redirect("/")
    # check to see if any imput is empty
    elif(sentence == ""):
        return redirect("/" + currentID)
    # else proceed as normal
    else:
        addStory(currentID, sentence, grid_square_pos)
        return redirect("/" + currentID)

# render the template of the current story
@app.route('/<currentID>')
def renderTemplate(currentID):

        middle = findSentence(currentID, "middle")
        top = findSentence(currentID, "top")
        right = findSentence(currentID, "right")
        bottom = findSentence(currentID, "bottom")
        left = findSentence(currentID, "left")

        topID = findID(currentID, "top")
        rightID = findID(currentID, "right")
        bottomID = findID(currentID, "bottom")
        leftID = findID(currentID, "left")

        parentID = findParentID(currentID)

        return render_template("storyboard.html",

                parentID = parentID,
                currentID = currentID,
                starttext = middle,
                top = top,
                topID = topID,
                right = right,
                rightID = rightID,
                bottom = bottom,
                bottomID = bottomID,
                left = left,
                leftID = leftID
        )

# find a child sentence given its parentID and position
def findSentence(currentID, pos):
    storyToRender = master_story_dict.get(currentID)
    if(storyToRender.get(pos) != None):
        sentence = storyToRender.get(pos)
        return sentence.get("sentence")

# find a child ID given its parentID and position
def findID(currentID, pos):
    storyToRender = master_story_dict.get(currentID)
    if(storyToRender.get(pos) != None):
        ID = storyToRender.get(pos)
        return ID.get("childID")

# find the parentID of a child (used for going back)
def findParentID(currentID):
    storyToRender = master_story_dict.get(currentID)
    if(storyToRender.get("parentID") != None):
        parentID = storyToRender.get("parentID")
        return parentID

if(__name__) == '__main__':
    app.run(debug = True)
