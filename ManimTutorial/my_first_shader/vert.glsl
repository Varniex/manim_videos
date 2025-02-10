#version 330

in vec3 point;
out vec3 xyz_coords;

#INSERT emit_gl_Position.glsl

void main() {
    xyz_coords = point;
    emit_gl_Position(point);
}
