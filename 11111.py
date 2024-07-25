import json
import numpy as np
from mayavi import mlab

with open('[175_kino_Anim_UPhalf][Kino]Scene.json', 'r') as f:
    data = json.load(f)

skeleton_data = data['skeleton']
translation_data = data['translation']


def build_skeleton(skeleton_data):
    skeleton = []

    def build_hierarchy(parent_node, children_data):
        for key, value in children_data.items():
            if isinstance(value, dict):
                if len(value) != 0:
                    for v, _ in value.items():
                        parent_node.append((key, v))
                    build_hierarchy(parent_node, value)
            else:
                parent_node.append((key, value))

    build_hierarchy(skeleton, skeleton_data)
    return skeleton



hierarchy = build_skeleton(skeleton_data)
print(hierarchy)

skeleton_related_parts = [
    "Hips", "Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End",
    "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
    "RightShoulder", "RightArm", "RightForeArm", "RightHand",
    "LeftUpLeg", "LeftFoot", "LeftToeBase", "LeftToe_End", "LeftLeg",
    "RightUpLeg", "RightFoot", "RightToeBase", "RightToe_End", "RightLeg"
]

# Dictionary mapping skeleton parts to their associated colors
skeleton_related_color = {
    "LeftArm": {
        "color": (1, 0, 0),  # Red for Left Arm
        "parts": [
            "Spine2", "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
        ],
    },
    "RightArm": {
        "color": (0, 1, 0),  # Green for Right Arm
        "parts": [
            "Spine2", "RightShoulder", "RightArm", "RightForeArm", "RightHand",
        ],
    },
    "LeftLeg": {
        "color": (0, 0, 1),  # Blue for Left Leg
        "parts": [
            "Hips", "LeftUpLeg", "LeftFoot", "LeftToeBase", "LeftToe_End", "LeftLeg",
        ],
    },
    "RightLeg": {
        "color": (0, 1, 1),  # Cyan for Right Leg
        "parts": [
            "Hips", "RightUpLeg", "RightFoot", "RightToeBase", "RightToe_End", "RightLeg",
        ],
    },
    "Body": {
        "color": (1, 0.5, 0),  # Orange for Body Trunk
        "parts": [
            "Hips", "Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End",
        ],
    }
}


# Function to get color based on from_ske and to_ske
def get_color(from_ske, to_ske, skeleton_related_color):
    for key, value in skeleton_related_color.items():
        if from_ske in value["parts"] and to_ske in value["parts"]:
            return value["color"]
    return (0.5, 0.5, 0.5)



def draw_3d_skeleton(positions, hierarchy, frame_idx, skeleton_related_color):
    for from_ske, to_ske in hierarchy:
        if from_ske in skeleton_related_parts and to_ske in skeleton_related_parts:
            start_pos = positions[from_ske]
            end_pos = positions[to_ske]
            color = get_color(from_ske, to_ske, skeleton_related_color)

            width = 10.0 if from_ske in ['Spine', 'Spine1'] else 3.0

            mlab.plot3d([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]],
                        [start_pos[2], end_pos[2]],
                        color=color, line_width=width,tube_radius=None)

            mlab.points3d(start_pos[0], start_pos[1], start_pos[2],
                          color=(1, 1, 0.5), mode='sphere', scale_factor=5)


num_frames = len(translation_data['Hips'])
for frame_idx in range(0, 10):
    mlab.clf()
    positions = {joint: np.array(translation_data[joint][frame_idx]) for joint in translation_data}
    draw_3d_skeleton(positions, hierarchy, frame_idx, skeleton_related_color)

    view = mlab.view(azimuth=0, elevation=0, distance=400, focalpoint=(0,90,0))
    mlab.savefig(f"output/xz_view_{frame_idx}.png")

mlab.show()


# Create some data
import numpy as np

x, y = np.mgrid[-10:10:200j, -10:10:200j]
z = 100 * np.sin(x * y) / (x * y)

# Visualize it with mlab.surf
from mayavi import mlab
mlab.figure(bgcolor=(1, 1, 1))
surf = mlab.surf(z, colormap='cool')



# We need to force update of the figure now that we have changed the LUT.
mlab.draw()
mlab.view(40, 85)

mlab.show()