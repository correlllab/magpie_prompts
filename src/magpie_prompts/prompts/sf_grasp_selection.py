grasp_prompt = '''
Help assist with selecting a robotic grasp for a given object and/or task.

You may receive the following information:
1) A user query about an object and/or task
2) An image of the object and scene
3) A grasp phrase describing what part/feature of the object to grasp

Reason about the semantic, spatial, and physical information in the image and user query to select a grasp and generate an (y, x) point in the image for the gripper to grasp.
If there is no user query or grasp phrase, try to intuit the most relevant object and/or task from the image and still generate an (y, x) point.
If there is no image, try to intuit the most relevant object and/or task from the user query, but do not generate an (y, x) point.
If there is no image or user query, do not return any grasp.

For many objects and tasks, there are multiple possible grasps with various affordances.
I.E. capabilities, properties, and constraints related to a particular grasp.
Many objects have particular sub-parts that are more suitable for grasping, potentially for a given task/affordance.
When providing a grasp, please provide the following information:
1) A description of the grasp, including where/how the gripper should be placed, based upon reasoning about the object and/or task, affordances, and properties.
2) A concise object phrase, consisting of at most four words describing where on the object should be grasped and a color or otherwise salient feature. 
The object phrase should be a noun phrase, not a verb phrase. For example, "red top of the box" or "blue cup handle". Do not use any other punctuation in the object phrase.

The answer should follow the python dictionary format: {"task": "<reasoning about the object and/or task, affordances, and properties>", "grasp_phrase": "<object phrase>", "point": , "label": }. 
The points are in [y, x] format normalized to 0-1000. Print only the python dictionary output, do not include any other text.
The robot gripper may already be near the grasp point, to make it easier to pick a point.
'''

grasp_axis = '''
Help assist with selecting a robotic grasp for a given object and/or task.

You may receive the following information:
1) A user query about an object and/or task
2) An image of the object and scene
3) A grasp phrase describing what part/feature of the object to grasp

Reason about the semantic, spatial, and physical information in the image and user query to select a grasp and generate two (y, x) points in the image to constitute the principal axis about which the gripper should grasp.
In robotic grasping, the gripper will close its fingers perpendicular to the principal axis. 
In effect, you can determine the principal axis of grasping intuitively; based off object geometry and semantically and visually obtained information.
For example, to grasp a banana, the principal axis runs lengthwise, so you would provide two (y, x) points each at the ends of the banana. 
The robot gripper would then grasp at the midline perpendicular to the principal axis, which is in line with how a human would grasp the banana.
If there is no user query or grasp phrase, try to intuit the most relevant object and/or task from the image and still generate  the two (y, x) points of the principal axis.
If there is no image, try to intuit the most relevant object and/or task from the user query, but do not generate the (y, x) points.
If there is no image or user query, do not return any grasp.

For many objects and tasks, there are multiple possible grasps with various affordances.
I.E. capabilities, properties, and constraints related to a particular grasp.
Many objects have particular sub-parts that are more suitable for grasping, potentially for a given task/affordance.
When providing a grasp, please provide the following information:
1) A description of the grasp, including where/how the gripper should be placed, based upon reasoning about the object and/or task, affordances, and properties.
2) A concise object phrase, consisting of at most four words describing where on the object should be grasped and a color or otherwise salient feature. 
The object phrase should be a noun phrase, not a verb phrase. For example, "red top of the box" or "blue cup handle". Do not use any other punctuation in the object phrase.

Rules:
The answer should follow the python dictionary format: {"task": "<reasoning about the object and/or task, affordances, and properties>", "grasp_phrase": "<object phrase>", "points": [(y1, x1), (y2, x2)], "label": }. 
The points are in [y, x] format normalized to 0-1000. Print only the python dictionary output, do not include any other text.
The robot gripper may already be near the grasp principal axis, to make it easier to select the points of the principal axis.
Make sure that the generated points are actually on the object in the image, not floating off in space.
'''

antipodal_grasp = '''
Help assist with selecting a robotic grasp for a given object and/or task.

You may receive the following information:
1) A user query about an object and/or task
2) An image of the object and scene
3) A grasp phrase describing what part/feature of the object to grasp

Reason about the semantic, spatial, and physical information in the image and user query to select a grasp and generate two (y, x) points in the image to constitute an antipodal grasp about the object.
In robotic grasping, an antipodal grasp is a type of grasp where the gripper's fingers are positioned on opposite sides of the object, allowing for a secure grip. 
This is akin to how a human would grasp an object with two fingers, pinching it from either side.
In effect, you can determine an antipodal grasp intuitively; based off object geometry and semantically and visually obtained information.
For example, to grasp a banana, you would provide two (y, x) points, one on each side of the banana, both located centrally along the length of the banana.
The robot gripper would then grasp at the midline perpendicular to the banana's length, which is in line with how a human would grasp the banana.
If there is no user query or grasp phrase, try to intuit the most relevant object and/or task from the image and still generate  the two (y, x) points of the antipodal.
If there is no image, try to intuit the most relevant object and/or task from the user query, but do not generate the (y, x) points.
If there is no image or user query, do not return any grasp.

For many objects and tasks, there are multiple possible grasps with various affordances.
I.E. capabilities, properties, and constraints related to a particular grasp.
Many objects have particular sub-parts that are more suitable for grasping, potentially for a given task/affordance.
When providing a grasp, please provide the following information:
1) A description of the grasp, including where/how the gripper should be placed, based upon reasoning about the object and/or task, affordances, and properties.
2) A concise object phrase, consisting of at most four words describing where on the object should be grasped and a color or otherwise salient feature. 
The object phrase should be a noun phrase, not a verb phrase. For example, "red top of the box" or "blue cup handle". Do not use any other punctuation in the object phrase.

Rules:
The answer should follow the python dictionary format: {"task": "<reasoning about the object and/or task, affordances, and properties>", "grasp_phrase": "<object phrase>", "points": [(y1, x1), (y2, x2)], "label": }. 
The points are in [y, x] format normalized to 0-1000. Print only the python dictionary output, do not include any other text.
The robot gripper may already be near the grasp principal axis, to make it easier to select the points of the principal axis.
Make sure that the generated points are actually on the object in the image, not floating off in space.
'''