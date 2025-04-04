from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict

class ObjectProperties(BaseModel):
    mass_kg: float = Field(..., description="Estimated mass of the object in kilograms.")
    material: str = Field(..., description="Material composition of the object.")
    friction_coefficient: float = Field(..., description="Coefficient of friction between the object and the surface.")
    stiffness_Nm: float = Field(..., description="Estimated stiffness of the object in Newton-meters.")

class EnvironmentProperties(BaseModel):
    surface_material: str = Field(..., description="Material composition of the surface the object is interacting with.")
    surface_friction_coefficient: float = Field(..., description="Coefficient of friction for the surface.")
    gravity_m_s2: float = Field(..., description="Acceleration due to gravity in meters per second squared.")

class MotionDirection(BaseModel):
    x: Literal["-1", "0", "1"] = Field(..., description="Direction along the x-axis (-1: negative, 0: none, 1: positive).")
    y: Literal["-1", "0", "1"] = Field(..., description="Direction along the y-axis (-1: negative, 0: none, 1: positive).")
    z: Literal["-1", "0", "1"] = Field(..., description="Direction along the z-axis (-1: negative, 0: none, 1: positive).")

class MotionPlan(BaseModel):
    motion_description: str = Field(..., description="Thorough description of the planned motion.")
    direction: MotionDirection
    goal_position: List[float] = Field(..., min_items=3, max_items=3, description="Target position displacement in meters (x, y, z).")
    goal_force: List[float] = Field(..., min_items=3, max_items=3, description="Required force to achieve motion in Newtons (fx, fy, fz).")
    task_duration: float = Field(..., description="Estimated time to complete the task in seconds.")
    grasp_force: float = Field(..., description="Estimated force required for grasping in Newtons.")

class MotionResistance(BaseModel):
    cause: str = Field(..., description="Cause of motion resistance (e.g., table friction, air resistance).")
    expected_effect: str = Field(..., description="Effect of this resistance on the motion (e.g., reduces forward motion).")

class StabilityConsideration(BaseModel):
    risk: str = Field(..., description="Potential risk to motion execution (e.g., object slipping, misalignment).")
    mitigation: str = Field(..., description="Strategy to mitigate this risk (e.g., increase grip force).")

class ForceEstimationStep(BaseModel):
    axis: str = Field(..., description="Axis of motion being considered (e.g., x, y, z) corresponding to the labeled axis in the provided image")
    motion_type: str = Field(..., description="Type of motion being considered (e.g., linear, rotational).")
    motion_resistances: MotionResistance = Field(..., description="List of motion resistances affecting execution.")
    stability_considerations: StabilityConsideration = Field(..., description="List of stability risks and mitigation strategies.")
    force_type: str = Field(..., description="Type of force being considered (e.g., gravitational, static friction, dynamic friction).")
    reasoning: str = Field(..., description="Reasoning about forces in order to accomplish the task on the given axis")
    formula: str = Field(..., description="Mathematical formula used for the estimation.")
    computed_value_N: float = Field(..., description="Computed force value in Newtons.")

class PhysicalReasoning(BaseModel):
    force_estimation_x: ForceEstimationStep
    force_estimation_y: ForceEstimationStep
    force_estimation_z: ForceEstimationStep
    force_estimation_grasp: ForceEstimationStep


class MotionForcePlan(BaseModel):
    task_description: str = Field(..., description="Thorough motion description of the task aligned with the labeled axes. Describe the explicit color of the labeled axis from the provided image and how it matches the motion. Describe the type of motion being considered (e.g., linear, rotational) and note that motion may resolve along multiple axes.")
    object_properties: ObjectProperties
    environment_properties: EnvironmentProperties
    physical_reasoning: PhysicalReasoning
    motion_plan: MotionPlan

# class ExpectedDynamics(BaseModel):
#     motion_type: str = Field(..., description="Type of motion expected (e.g., linear, rotational, some combination).")
#     motion_resistances: List[MotionResistance] = Field(..., description="List of motion resistances affecting execution.")
#     stability_considerations: List[StabilityConsideration] = Field(..., description="List of stability risks and mitigation strategies.")
#     # force_calculations: List[ForceEstimationStep] = Field(..., description="List of force estimations used in planning.")
#     grasping_considerations: List[str] = Field(..., description="Considerations for grasping force stability and compliance.")
