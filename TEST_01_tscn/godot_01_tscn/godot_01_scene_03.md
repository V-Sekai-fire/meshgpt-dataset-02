# The scene tree

The scene tree is made up of… nodes! The heading of each node consists of its name, parent and (most of the time) a type. For example: [node name="PlayerCamera" type="Camera" parent="Player/Head"]

Other valid keywords include:

        instance

        instance_placeholder

        owner

        index (sets the order of appearance in the tree; if absent, inherited nodes will take precedence over plain ones)

        groups

The first node in the file, which is also the scene root, must not have a parent="Path/To/Node" entry in its heading. All scene files should have exactly one scene root. If it doesn't, Godot will fail to import the file. The parent path of other nodes should be absolute, but shouldn't contain the scene root's name. If the node is a direct child of the scene root, the path should be ".". Here is an example scene tree (but without any node content):

[node name="Player" type="Node3D"]                    ; The scene root
[node name="Arm" type="Node3D" parent="."]            ; Parented to the scene root
[node name="Hand" type="Node3D" parent="Arm"]         ; Child of "Arm"
[node name="Finger" type="Node3D" parent="Arm/Hand"]  ; Child of "Hand"
