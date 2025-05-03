import com.jogamp.opengl.*;
import com.jogamp.opengl.awt.GLCanvas;
import javax.swing.JFrame;

public class SimpleJOGL implements GLEventListener {

    public static void main(String[] args) {
        GLProfile profile = GLProfile.get(GLProfile.GL2);
        GLCapabilities capabilities = new GLCapabilities(profile);
        GLCanvas canvas = new GLCanvas(capabilities);

        JFrame frame = new JFrame("Simple JOGL");
        frame.setSize(600, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(canvas);
        frame.setVisible(true);

        canvas.addGLEventListener(new SimpleJOGL()); // This class is the GLEventListener
        canvas.requestFocusInWindow();
    }

    @Override
    public void init(GLAutoDrawable drawable) {
        GL2 gl = drawable.getGL().getGL2();
        gl.glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // Black background
    }

    @Override
    public void dispose(GLAutoDrawable drawable) {
        // Clean up resources if needed
    }

    @Override
    public void display(GLAutoDrawable drawable) {
        GL2 gl = drawable.getGL().getGL2();

        gl.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT);
        gl.glLoadIdentity();  // Reset the modelview matrix

        // Example: Draw a triangle
        gl.glBegin(GL.GL_TRIANGLES);
            gl.glColor3f(1.0f, 0.0f, 0.0f); // Red
            gl.glVertex3f(-0.5f, -0.5f, 0.0f);

            gl.glColor3f(0.0f, 1.0f, 0.0f); // Green
            gl.glVertex3f(0.5f, -0.5f, 0.0f);

            gl.glColor3f(0.0f, 0.0f, 1.0f); // Blue
            gl.glVertex3f(0.0f, 0.5f, 0.0f);
        gl.glEnd();

        gl.glFlush(); // Force execution of OpenGL commands
    }

    @Override
    public void reshape(GLAutoDrawable drawable, int x, int y, int width, int height) {
        GL2 gl = drawable.getGL().getGL2();

        if (height <= 0) height = 1;
        final float h = (float) width / (float) height;
        gl.glViewport(0, 0, width, height);
        gl.glMatrixMode(GL2.GL_PROJECTION);
        gl.glLoadIdentity();
        //Orthographic perspective.  The next call is the important one
        gl.glOrtho(-1, 1, -1, 1, -1, 1);
        gl.glMatrixMode(GL2.GL_MODELVIEW);
        gl.glLoadIdentity();
    }
}