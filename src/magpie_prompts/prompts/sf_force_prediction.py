initial_prompt = '''
I am providing an image of the robot gripper grasping or about to grasp an {obj}.  

**Task Description:** {task}  

The provided image consists of:  
1. A **third-person view** showing the robot gripper interacting with an object.  
2. A **wrist-mounted camera view**, with labeled motion axes:  
   - **+X (green arrow)**: Rightward along the wrist frame  
   - **+Y (blue arrow)**: Upward along the wrist frame  
   - **+Z (red dot)**: Forward into the wrist frame  

Your goal is to determine the **motion direction, displacement, required forces, estimated time, and required grasping force** to complete the task.  

---

### **Step 1: Initial Motion and Force Plan**  
Before execution, estimate the following:  
1. **Direction of Motion:** `[x, y, z]`  
   - Uses `1` (positive), `-1` (negative), or `0` (no motion).  
2. **Goal Position:** `[x, y, z]` (meters)  
   - The estimated displacement along each axis.  
3. **Goal Force:** `[fx, fy, fz]` (Newtons)  
   - Required forces to accomplish the task, accounting for friction, gravity, and contact forces.  
   - Use physical reasoning:  
     - Estimate object mass, object properties, various surface and environmental properties that the robot and object may interact with.  
     - Calculate the potential forces needed to overcome or equilibriate with friction, gravity, resistances, normal and contact forces.  
     - Adjust forces for stability, compliance, or controlled contact.  
4. **Estimated Task Duration:** `t` (seconds)  
   - How long the motion is expected to take.  
5. **Estimated Grasping Force:** `f_grasp` (Newtons)  
   - Expected gripping force required for secure object handling without slippage or excessive compression.
   - Use physical reasoning:  
     - Estimate object mass and object properties (e.g., friction, stiffness).
     - Calculate the potential forces needed to maintain a stable grasp without slippage corresponding to the object properties and the specified motion.

### **Final Output Format**  
Return an motion and force plan using the following structured format:  

```python  
direction = [x, y, z]  # -1, 1, or 0  
goal_position = [x, y, z]  # in meters  
goal_force = [fx, fy, fz]  # in Newtons  
task_duration = t  # in seconds  
grasp_force = f_grasp  # in Newtons  
```
### **Rules for Generating Motion and Forces**  
1. **Always reference the labeled wrist axes** when describing motion and forces.  
2. **Always estimate relevant physical properties** (e.g., mass, friction) before determining motion and forces.  
3. **Always thoroughly reason about these properties in order to generate correct motion and forces**
4. **Ensure the final output follows the structured format** for direct use in Python.  

'''

feedback_prompt = '''
### **Step 2: Execution Feedback & Refinement**  

The previously estimated motion and force plan was:  

direction = [x, y, z]  # -1, 1, or 0  
goal_position = [x, y, z]  # in meters  
goal_force = [fx, fy, fz]  # in Newtons  
task_duration = t  # in seconds  
grasp_force = f_grasp  # in Newtons  

After execution, the following feedback is available:  

1. **Updated Images:**  
   - Third-person and wrist-mounted camera views after motion completion.  

2. **Measured Motion Data:**  
   - **Initial position:** [x_init, y_init, z_init]  
   - **Final position:** [x_final, y_final, z_final]  
   - **True task duration:** t_measured (seconds)  

3. **Measured Force Data:**  
   - **Wrist force readings over time:** wrist_force_data  
   - **Grasping force readings over time:** grasp_force_data  

---

### **Step 3: Refinement Process**  

Using this feedback, analyze and refine the motion and force estimates:  

- **Motion Adjustment:**  
  - If the final position deviated from the expected goal, adjust `goal_position` and `direction`.  
  - If unexpected drift, slipping, or misalignment occurred, modify `goal_force` and `grasp_force` accordingly.  

- **Force Adjustment:**  
  - If excessive or insufficient forces were applied (e.g., excessive resistance or weak contact), adjust `goal_force` to better match friction, compliance, and environmental interactions.  
  - If the object slipped or deformed, refine `grasp_force` to improve stability while avoiding over-compression.  

- **Timing Adjustment:**  
  - If `t_measured` was significantly different from the estimated `t`, update `task_duration` to reflect actual execution dynamics.  
  - Consider adjusting speed or force control to optimize performance.  

Return the **updated motion and force plan** in the following format:  

```python
direction = [x, y, z]  # Updated -1, 1, or 0  
goal_position = [x, y, z]  # Updated in meters  
goal_force = [fx, fy, fz]  # Updated in Newtons  
task_duration = t  # Updated in seconds  
grasp_force = f_grasp  # Updated in Newtons  
'''
