grasp_prompt = '''
Help assist with selecting a robotic grasp for a given object and/or task.

You may receive the following information:
1) A user query about an object and/or task
2) An image of the object and scene

Reason about the semantic, spatial, and physical information in the image and user query to select a grasp.
If there is no user query, try to intuit the most relevant object and/or task from the image.
If there is no image, try to intuit the most relevant object and/or task from the user query.
If there is no image or user query, do not return any grasp.

For many objects and tasks, there are multiple possible grasps with various affordances.
I.E. capabilities, properties, and constraints related to a particular grasp.
Many objects have particular sub-parts that are more suitable for grasping, potentially for a given task/affordance.
When providing a grasp, please provide the following information:
1) A description of the grasp, including where/how the gripper should be placed, based upon reasoning about the object and/or task, affordances, and properties.
2) A concise object phrase, consisting of at most four words describing where on the object should be grasped and a color or otherwise salient feature. 
Provide this in in a separate newline so that it can be easily extracted.
The object phrase should be a noun phrase, not a verb phrase. For example, "red top of the box" or "blue cup handle". Do not use any other punctuation in the object phrase.

User Query: {user_query}
Response Format:
1) Reasoning and Grasp Description: <reasoning about the object and/or task, affordances, and properties>
2) Object Phrase: \n
<grasp phrase>

'''