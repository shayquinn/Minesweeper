uniform mat4 modelview_mat;
uniform mat4 projection_mat;
attribute vec2 pos;
attribute vec2 tex_coord;
varying vec2 v_tex_coord;

void main() {
    v_tex_coord = tex_coord;
    gl_Position = projection_mat * modelview_mat * vec4(pos, 0.0, 1.0);
}