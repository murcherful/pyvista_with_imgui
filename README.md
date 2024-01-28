# Pyvista with Pyimgui

This is a demo showcasing the combination of [PyVista](https://docs.pyvista.org/version/stable/) and [pyimgui](https://pyimgui.readthedocs.io/en/latest/index.html) in multiple windows. 
This demo is written in Python only.
It is easy to apply it to your own work by adding custom GUI widgets with puimgui or modifying the rendering process of PyVista.

This demo achieves rendering 3D objects and controlling them with ImGui using only Python, making it easy for researchers to visualize their work with a convenient GUI framework.
If you find this demo useful, please consider starring the project.

### Getting Start
Create a Python environment using conda.

```
conda create -n pyvista-imgui python=3.8
```

Install the PyVista, pyimgui and PyAutoGUI.

```
pip install pyvista
pip install imgui[pygame]
pip install PyAutoGUI
```
Run the demo.
```
python test_pyvista_imgui.py
```
Then you should see a window.
![](/images/pyimgui.png)
Click the "Open" button, and you will see another window with a sphere.
![](/images/all.png)
You can change the radius of shpere with the silder in "Test Change Sphere" window.
The position and size of the PyVista window can be set through "Render Window Settings" window.

You need to check the documents of PyVista and pyimgui to add the custion gui or other operation with PyVista.
