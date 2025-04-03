initial_prompt = '''
I am providing an image of the robot gripper grasping or about to grasp an {obj}.
Desired task and motion description: {task}
On the left is a third-person view of the workspace with the robot gripper and the {obj}.
On the right is a first-person view from the robot gripper wrist.
I have labeled the axes of motion and force sensing for the wrist as such:
+X (green arrow, to the right along the x-axis of the wrist image)
+Y (blue arrow, up the y-axis of the wrist image)
+Z (red dot, ceneted and into the wrist image)

Please tell me how the gripper should move, in a few ways.
For each response, provide your answer in the form of 3-element vector corresponding to the X, Y, Z axes.
1. Coarse motion (positive, negative, or nothing)
2. Fine motion (meters)
3. Required forces (Newtons)

Before providing your answer, please take a moment to study the image and consider the task.
Consider the mass, friction, stiffness and other such properties of the object and the workspace.
Consider the particular dynamics and forces at play in performing the described task.

Here is a more in-depth explanation of the requested responses:
1. Coarsely, if it should be negative, positive, or no motion, using the values -1, 1, or 0.
Describe how this motion is in line with the provided labeled axes.

2. Then, using the desired motion description, try to provide a more detailed and numerical answer.
If a distance is specified, try to resolve along the estimated axes of motion.
Or if a non-explicit goal, visual or otherwise, is specified, leverage physical, spatial, semantic, visual, or other cues to provide a more specific answer.
Use units of meters for this array.

3. Then, using the desired motion description and physical reasoning, estimate the translational forces required to accomplish the motion.
Use your physical knowledge of the object being manipulated, the material types of the surfaces interacting, and the types of motion to reason about forces required to accomplish the task.
Relevant quantities may be mass, gravity, static friction, velocity, or acceleration. 
Always estimate these quantities first, where relevant, before formulating motion or forces.

Final Output:
direction = [x, y, z] # -1, 1, or 0
goal_position = [x, y, z] # numerical value, in meters
goal_force = [fx, fy, fz] # numerical value, in Newtons

Rules:
1. Always take into consideration the image input and annotated motion axes in the image when generating motion and forces.
2. Always estimate physical quantities first, where relevant, before directly estimating motion or forces.
3. Always generate the final output, which is a series of three Python arrays describing direction, goal position, and goal force.
'''

initial_prompt = ''' 
I am providing an image of a robot gripper grasping or about to grasp an {obj}.  

### **Task and Motion Description:**  
{task}  

On the left is a **third-person view** of the workspace, showing the robot gripper and the {obj}.  
On the right is a **first-person (wrist) view** from the robot gripper.  

The wrist axes are labeled as follows:  
- **+X (green arrow):** Rightward along the wrist's x-axis  
- **+Y (blue arrow):** Upward along the wrist's y-axis  
- **+Z (red dot):** Into the image, along the wrist's z-axis  

---  

### **Objective**  
Your goal is to analyze the image, task description, and labeled axes to determine the correct motion and forces required to accomplish the task.  
Before providing an answer, take a moment to consider:  
- The **physical properties** of the object and workspace (e.g., mass, friction, stiffness).  
- The **type of interaction** required (e.g., pushing, lifting, sliding).  
- The **forces acting on the object**, including gravity, friction, and any constraints.  

---  

### **Final Output Format**  
Your response should contain **three structured outputs** in Python array format:  

1. **Direction of Motion** `[x, y, z]`  
   - Represents the general motion direction along the labeled wrist axes.  
   - Use `1` for positive motion, `-1` for negative motion, and `0` for no motion.  

2. **Goal Position** `[x, y, z]` (in meters)  
   - Specifies the estimated displacement needed to complete the task.  
   - If an explicit distance is given, resolve it along the wrist axes.  
   - If the task is goal-driven (e.g., making contact, aligning), estimate the required displacement accordingly.  

3. **Goal Force** `[fx, fy, fz]` (in Newtons)  
   - Represents the forces required along each axis to accomplish the motion.  
   - Use physical reasoning:  
     - Estimate object mass.  
     - Calculate forces needed to overcome friction, gravity, or resistances.  
     - Adjust forces for stability, compliance, or controlled contact.  

---  

### **Rules for Generating Motion and Forces**  
1. **Always reference the labeled wrist axes** when describing motion and forces.  
2. **Always estimate relevant physical properties** (e.g., mass, friction) before determining motion and forces.  
3. **Ensure the final output follows the structured format** for direct use in Python.  
'''

initial_prompt = """ 
You are analyzing a robotic manipulation task using an image and a task description. The image consists of:  
1. A **third-person view** showing the robot gripper interacting with an {obj}  
2. A **wrist-mounted camera view**, with labeled motion axes:  
   - **+X (green)**: Rightward relative to the wrist frame  
   - **+Y (blue)**: Upward relative to the wrist frame  
   - **+Z (red dot)**: Forward into the wrist frame  

#### **Task Overview**  
The robot is attempting to perform a specific manipulation task:  
**{task}**  

Your goal is to determine the **motion direction, displacement, and required forces** needed to complete the task.  

#### **Response Requirements**  

1. **Analyze the physical properties** of the object and environment:  
   - Object **mass, material, and expected resistance** (friction, stiffness).  
   - Interaction type: **sliding, lifting, pressing, rotating, or articulated motion.**  
   - Forces acting on the object: **gravity, contact resistance, and external constraints.**  

2. **Generate a structured motion and force response** using the labeled wrist axes:  
   - **Direction of Motion:** `[x, y, z]`  
     - Uses `1` (positive), `-1` (negative), or `0` (no motion).  
   - **Goal Position:** `[x, y, z]` (in meters)  
     - Estimates how far the gripper should move along each axis.  
   - **Goal Force:** `[fx, fy, fz]` (in Newtons)  
     - Computes forces needed to overcome friction, gravity, or resistances.  

#### **Rules for Output Generation**  
- **Always align motion and force predictions** with the labeled wrist axes.  
- **Always estimate relevant physical effects** before assigning values.  
- **Ensure the final output is in structured Python array format.**  

"""