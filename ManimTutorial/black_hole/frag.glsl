#version 330

in vec3 xyz_coords;
out vec4 frag_color;

uniform vec2 iMouse;
uniform float iTime;

void main() {
    vec2 uv = xyz_coords.xy;

    float d = length(uv);
    d = smoothstep(1.0, 2.5, d);
    d = 0.1 / abs(sin(10 * d + iTime + 0.1 * uv.x / uv.y));

    vec3 color = vec3(d / 1.35, 2.0 * d / 5.0, 2.0 * d);
    frag_color = vec4(color, 1.0);
}
